Fundscout
=========

**Disclaimer: Don't use this software, unless you know what you're doing**

Fundscout is a graphical application to help making future decisions based on your funds.

Motivation
----------

Most money managing applications are:

    * hosted on the web and therefore can leak private data to third parties
    * don't talk to your bank
    * aren't free software
    * won't let you control your data

That's why I want an application where I have control over my data.
Furthermore I want an application which presents the data in such a way,
that I can make informed decisions for future investments (however
large or small they might be).

Prerequites
-----------

    * Ghost.py (https://github.com/jeanphix/Ghost.py) > 0.1b2
    * PySide

Development Sandbox
-------------------

Create a virtualenv first and use python2.7:

    virtualenv ~/tools/python2.7
    
Install PySide in the virtualenv as outlined in the [pyside_setup guide](https://github.com/PySide/pyside-setup). Make sure you run the pyside_postinstall.py script after the installation if needed.

Run the usual buildout procedure:

    ~/tools/python2.7/bin/python bootstrap.py
    bin/buildout -N
    
Check if everything works as expected by running the tests.

    bin/test
