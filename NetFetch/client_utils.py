# Copyright (c) 2015 Tim Savannah GPLv3 + attribution clause. See LICENSE for more information.

import os
import sys

def readPasswordFromFilename(passwordFilename):
    '''
        readPasswordFromFilename - Handles reading password from a given file

        @param passwordFilename <str> - Path to filename file

        Exists on failure

        @return <str>  - String of  password
    '''
    if not os.path.exists(passwordFilename):
        sys.stderr.write('Cannot find password file: "%s"\n' %(passwordFilename,))
        sys.exit(1)

    try:
        with open(passwordFilename, 'rt') as f:
            password = f.readline()
        if password[-1] == '\n':
            password = password[:-1]
        if password[-1] == '\r':
            password = password[:-1]
    except Exception as e:
        sys.stderr.write('Error reading from password input file, "%s": %s\n' %(passwordFilename, str(e)))
        sys.exit(1)
    if not password:
        sys.stderr.write('Provided password file, "%s" is blank or has empty first line.' %(passwordFilename,))
        sys.exit(1)

    return password


def findDefaultConfigFilename():
    '''
        findDefaultConfigFilename - Searches ~/.netconfig.cfg and /etc/netconfig.cfg in that order, and returns the first that exists, or None

        @return  <str/None> - Path  to config to use or None if neither exists.
    '''
    if 'HOME' in os.environ and os.path.isdir(os.environ['HOME']):
        cfgPath = "%s/.netfetch.cfg" %(os.environ['HOME'],)
        if os.path.isfile(cfgPath):
            return cfgPath
    if os.path.isfile('/etc/netfetch.cfg'):
        return '/etc/netfetch.cfg'

    return None
