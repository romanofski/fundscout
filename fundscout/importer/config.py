import ConfigParser as configparser
import fundscout.importer.config
import ghost


def lex_config(fp):
    """Lexes the given configuration and creates Ghost browser
    statements.

    >>> import StringIO
    >>> len(lex_config(StringIO.StringIO('invalid')))
    0
    >>> result = lex_config(StringIO.StringIO('open "http://foobar"'))
    >>> len(result)
    1
    >>> result[0].url
    'http://foobar'
    >>> len(lex_config(StringIO.StringIO('open "http://foobar"\\nclick "selector"')))
    2
   """
    result = []
    data = []
    klass = None
    for line in fp:
        commands = line.strip().split(' ')
        token = commands[0]
        klass = getattr(fundscout.importer.config, token, None)
        if klass is not None:
            result.append(klass(commands[1:]))

    return result


def configure_and_run(configuration):
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

    def prepare(self, tokens):
        self.url = tokens[0].strip('"')

    def __call__(self, browser):
        return browser.open(self.url)


class fill(BaseStatement):
    """ fills a form with given mapping.

    >>> obj = fill(['form select', 'key:value,', ' frob:value'])
    >>> obj.selector
    'form select'
    >>> obj.data['frob']
    'value'
    >>> obj.data['key']
    'value'
    """

    def prepare(self, tokens):
        self.selector = tokens[0]
        self.data = {}
        for t in tokens[1:]:
            self.data.update(dict([t.strip(',').strip().split(':')]))

    def __call__(self, browser):
        browser.fill(self.selector, self.data)
        return browser.fire_on(self.selector, 'submit', expect_loading=True)


class click(BaseStatement):
    """ Clicks a link based on a selector."""

    def prepare(self, tokens):
        self.urls = tokens

    def __call__(self, browser):
        pass


class debug(BaseStatement):
    """capture the viewport"""

    def prepare(self, tokens):
        self.filepath = tokens[0]

    def __call__(self, browser):
        browser.capture_to(self.filepath)
