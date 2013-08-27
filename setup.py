# coding: utf-8
from setuptools import setup, find_packages
from fundscout import __author__
from fundscout import __author_email__
from fundscout import __description__
from fundscout import __name__
from fundscout import __version__


setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=open("README.md").read(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
    ],
    keywords='server',
    author=__author__,
    author_email=__author_email__,
    url='http://fundscout.rtfd.org',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sqlalchemy',
        'Ghost.py',
    ],
    extras_require=dict(
        test=['mock',
              'flask',
              ]
    ),
    entry_points={
        'console_scripts': [
            'fundscout = fundscout.commandline:client',
            'testserver = fundscout.tests.app:run_server',
        ]
    }
)
