#!/usr/bin/env python
# Copyright (c) 2015 Tim Savannah GPLv3 + attribution clause. See LICENSE for more information.
# 
#  Installation for NetFetch
#vim: set ts=4 sw=4 expandtab

import os
import sys
try:
    from setuptools import setup
except:
    # NOTE! IF YOU SEE ERROR LIKE "install_requires" not found, comment that line below, or install setuptools.
    from distutils.core import setup




summary = 'Networked file storage and retrieval with optional password protection using Redis'

if __name__ == '__main__':
    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)
    try:
        with open('README.rst', 'r') as f:
            long_description = f.read()
    except:
        sys.stderr.write('Failed to find README.rst for full description! Falling back to summary.\n')
        long_description = summary

    setup(name='NetFetch',
            version='1.0',
            packages=['NetFetch'],
            scripts=['netFetchPut', 'netFetchGet'],
            author='Tim Savannah',
            author_email='kata198@gmail.com',
            maintainer='Tim Savannah',
            url='https://github.com/kata198/NetFetch',
            maintainer_email='kata198@gmail.com',
            description=summary,
            long_description=long_description,
            license='GPLv3',
            requires=['IndexedRedis', 'cryptography'],
            install_requires=['IndexedRedis', 'cryptography'],
            keywords=['NetFetch', 'redis', 'file', 'storage', 'retrieval', 'put', 'get',' network', 'password', 'encrypt', 'netFetchPut', 'netFetchGet', 'server'],
            classifiers=['Development Status :: 3 - Alpha',
                         'Programming Language :: Python',
                         'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                         'Environment :: Console',
                         'Topic :: System :: Networking',
                         'Topic :: System :: Archiving',
                         'Topic :: Database',
                         'Topic :: Software Development :: Libraries :: Python Modules',
                         'Topic :: Utilities',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.6',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.3',
                          'Programming Language :: Python :: 3.4',
            ]
    )

    sys.stdout.write('\n\n')
    sys.stdout.write('*' * 40)
    sys.stdout.write('\n')
    sys.stdout.write('INSTALLATION COMPLETE!\nMake sure to create your configuration file! See example.cfg.\nYou can put it in /etc/netfetch.cfg, $HOME/.netfetch.cfg, or provide it on every call with --config=/path/to/netfetch.cfg\n')
    sys.stdout.write('*' * 40)
    sys.stdout.write('\n')



