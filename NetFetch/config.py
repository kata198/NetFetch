# Copyright (c) 2015 Tim Savannah GPLv3 + attribution clause. See LICENSE for more information.

try:
    from ConfigParser import ConfigParser, NoSectionError
except ImportError:
    from configparser import ConfigParser, NoSectionError



def getRedisConnectionParams(configFile):
    parser = ConfigParser()
    with open(configFile, 'r') as f:
        parser.readfp(f)

    theDict = {}
    try:
        items = parser.items('redis')
    except NoSectionError:
        return theDict

    for key, value in items:
        theDict[key] = value

    return theDict
