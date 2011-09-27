#!/usr/bin/env python

"""Setup script for 'exyapps'"""

from distutils.core import setup

description = "Extensions of Yet Another Python Parser System"
long_description = \
"""
EXYAPPS is an easy to use parser generator that is written in Python and
generates Python code.  It is intended to be simple, very easy to use,
and produce human-readable parsers.

It is not the fastest or most powerful parser.  Exyapps is designed
to be used when regular expressions are not enough and other parser
systems are too much: situations where you might otherwise write your
own recursive descent parser.

Exyapps is derived from YAPPS, with various extensions:
- Handle stacked input ("include files")
- augmented ignore-able patterns (can parse multi-line C comments correctly)
- better error reporting
- read input incrementally
- the generated parser does not require any runtime library

"""

setup (
    name = "exyapps",
    version = "3.0dev",
    description = description,
    long_description = long_description,
    url="https://svn.stsci.edu/trac/ssb/etal/wiki/exyapps",
    maintainer="Mark Sienkiewicz",
    maintainer_email='no_spam@see_url',
    # bug: replace this and put acknowledgements of these guys in the docs
    # url = "http://theory.stanford.edu/~amitp/yapps/",
    # author = "Amit J. Patel",
    # author_email = "amitp@cs.stanford.edu",
    # maintainer = "Matthias Urlichs",
    # maintainer_email = "smurf@debian.org",
    license = 'MIT',
    platforms = ['POSIX'],
    keywords = ['parsing'],
    packages = ['exyapps'],
    scripts = ['scripts/exyapps'],
    # if we ever start using distribute
    # zip_safe = False,
    )
