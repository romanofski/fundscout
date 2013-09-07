import ConfigParser as configparser
import fundscout.importer.config
import re
import ghost


def lex_config(fp):
    """Lexes the given configuration and creates Ghost browser
    statements.

    >>> import StringIO
    >>> len(lex_config(StringIO.StringIO('invalid')))
    0
    >>> result = lex_config(StringIO.StringIO('open http://foobar'))
    >>> len(result)
    1
    >>> result[0].url
    'http://foobar'
    >>> result = lex_config(StringIO.StringIO('click h1 span a'))
    >>> len(result)
    1
    >>> result[0].selector
    'h1 span a'
    >>> len(lex_config(StringIO.StringIO('open "http://foobar"\\nclick "selector"')))
    2
   """
    result = []
    data = []
    klass = None
    for line in fp:
        try:
            command, data = line.strip().split(' ', 1)
        except ValueError:
            continue
        klass = getattr(fundscout.importer.config, command, None)
        if klass is not None:
            result.append(klass(data))

    return result


def configure_and_run(configuration):
    """Reads the configuration to download the CSV from an Account.

    The configuration follows the conventions of the ConfigParser
    module.

    Example:

        [fundscout]
        accounts = FirstAccount

        [FirstAccount]
        steps = open http://localhost:5000
                click "h1 span a"
                fill "form" "inputname:value, inputname2:value"
                expect "span p"
                debug /tmp/foo.png

    """
    config = configparser.SafeConfigParser()
    config.read(configuration)
    try:
        accounts = config.get('fundscout', 'accounts')
        for name in accounts.split('\n'):
            steps = lex_config(config.get(name, 'steps'))
            browser = ghost.Ghost()
            for s in steps:
                s(browser)
    except configparser.NoOptionError, err:
        print err


class BaseStatement(object):

    def __init__(self, tokens):
        self.prepare(tokens)

    def prepare(self, tokens):
        NotImplementedError("Implemented in sub classes")

    def __call__(self, browser):
        pass


class open(BaseStatement):
    """ opens a URL """

    def prepare(self, url):
        self.url = url

    def __call__(self, browser):
        return browser.open(self.url)


class fill(BaseStatement):
    """ fills a form with given mapping.

    >>> obj = fill('"h2 span a" key:value, key2:value2, key3:value')
    >>> obj.selector
    'h2 span a'
    >>> obj.data['key']
    'value'
    >>> obj.data['key2']
    'value2'
    """

    def prepare(self, line):
        _, self.selector, self.data = re.split('"', line)
        self.data = dict([x.strip().split(':') for x in self.data.split(',')])

    def __call__(self, browser):
        browser.fill(self.selector, self.data)
        return browser.fire_on(self.selector, 'submit', expect_loading=True)


class click(BaseStatement):
    """ Clicks a link based on a selector."""

    def prepare(self, selector):
        self.selector = selector

    def __call__(self, browser):
        return browser.click(self.selector)


class debug(BaseStatement):
    """capture the viewport"""

    def prepare(self, path):
        self.filepath = path

    def __call__(self, browser):
        return browser.capture_to(self.filepath)


class expect(BaseStatement):
    """Raise an AssertionError if the given CSS3 selector does not
       match.
    """

    def prepare(self, selector):
        self.selector = selector.strip('"')

    def __call__(self, browser):
        assert browser.exists(self.selector)
