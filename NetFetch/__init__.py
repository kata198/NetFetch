# Copyright (c) 2015 Tim Savannah GPLv3 + attribution clause. See LICENSE for more information.
# 
#  This file contains the model and methods for using NetFetch

# vim: ts=4 sw=4 expandtab
import base64
import os

import socket

import IndexedRedis

from cryptography.fernet import Fernet
from hashlib import md5



__all__ = ('NoSuchNetFetchFile', 'NetFetchFile', 'InvalidPasswordException', 'setRedisConnectionParams')

def setRedisConnectionParams(redisParams):
    NetFetchFile.REDIS_CONNECTION_PARAMS = redisParams

class NoSuchNetFetchFile(Exception):
    '''
        Raised when a file attempted to be fetched does not exist
    '''
    pass

class InvalidPasswordException(Exception):
    '''
        Raised when an invalid password is provided, or some other password-related failure.

        Message contains exact reason.
    '''
    pass



class NetFetchFile(IndexedRedis.IndexedRedisModel):
    '''
        NetFetchFile - Represents a File stored in NetFetch.

            A file is keyed based on hostname and absolute filename. 

            May optionally have mode,owner,group filled-in.
            
            May be encrypted with a password, in which case "encrypted" is set to "1".
    '''

    FIELDS = [
        'filename',
        'hostname',
        'checksum',
        'encrypted',
        'mode',
        'owner',
        'group',
        'data',
    ]

    INDEXED_FIELDS = [
        'filename',
        'hostname'
    ]

    BASE64_FIELDS = [
         'data',
    ]

    KEY_NAME = 'NetFetchFile'

    ###################################
    ##      Data Access              ##
    ###################################

    def getData(self, password=None):
        '''
            getData - Fetch the data associated with this file, and potentially decrypt.

            @param password <str/None> - None if unencrypted, otherwise a password 4-32 chars.

            @return <bytes> - file data

            @raises InvalidPasswordException - The file was encrypted and a password was invalid, or the file was not encrypted and a password was provided, or the file was encrypted and no password was provided.
            @raises ValueError - If password is not 4-32 characters.
        '''
        if not password:
            if self.encrypted == '1':
                raise InvalidPasswordException('File is encrypted. Must provide password.')
            ret = self.data
        else:
            if self.encrypted == '0':
                raise InvalidPasswordException('File is not encrypted and password was provided.')
            try:
                fernetKey = NetFetchFile._getFernetKey(password)
                fernet = Fernet(fernetKey)
                ret = fernet.decrypt(self.data)
            except ValueError:
                raise
            except Exception as e:
                raise e
                # Invalid password because did not match fernet structure
                raise InvalidPasswordException('Invalid Password.')

        checksum = NetFetchFile.calculateChecksum(ret)

        if checksum != self.checksum:
            # Invalid password because either "encrypted" field was tampered-with, 
            #   or a password matched the fernet structure but was not a match.
            raise InvalidPasswordException('Invalid Password.')

        return ret


    def setData(self, data):
        '''
            setData - Store data on this object and calculates checksum. If a password is required, must also call encryptData. Does not save object.

            @param data <bytes> - Data to store
        '''
        self.data = data
        self.checksum = NetFetchFile.calculateChecksum(data)


    def encryptData(self, password):
        '''
            encryptData - Encrypts data on this object and sets 'encrypted' flag.  Does not save object.

            @param password <str> 4-32 characters of password, used to encrypt.

            @raises - ValueError if password does not meet requirements
        '''
        fernetKey = NetFetchFile._getFernetKey(password)

        fernet = Fernet(fernetKey)
        self.data = fernet.encrypt(self.data)
        self.encrypted = '1'



    ###################################
    ##        Retrieval Methods      ##
    ###################################


    @classmethod
    def exists(cls, hostname, filename):
        '''
            exists - Check if a hostname/filename pair exists

            @param hostname <str> - Hostname field
            @param filename <str> - Filename field

            @return <bool> - If a file is stored under the hostname/filename key pair
        '''
        return bool(cls.objects.filter(filename=filename, hostname=hostname).count() > 0)

    @classmethod
    def downloadToLocal(cls, hostname, filename, password=None, localFilename=None, retainPermissions=True):
        '''
            downloadToLocal - Download file to a local filename

            @param hostname <str> - Hostname that file was stored on
            @param filename <str> - Filename to fetch
            @param password <str/None> - Try this password on potentially encrpyted file.
            @param localFilename <str/None> - If defined, saves at this location. Otherwise, saves at #filename
            @param retainPermissions <bool> Default True - If True, tries to retain owner/group/mode. If owner/group, you must be root. Silently fails if can't apply.

            @raises NoSuchNetFetchFile - If no hostname/filename match exists
            @raises InvalidPasswordException - If password was invalid, see getData for all conditions.
        '''
        if not localFilename:
            localFilename = filename
        
        obj = cls.objects.filter(hostname=hostname, filename=filename).all()
        if not obj:
            raise NoSuchNetFetchFile('No file matching hostname="%s" filename="%s"' %(hostname, filename))

        obj = obj[0]
        data = obj.getData(password)
        with open(localFilename, 'wb') as f:
            f.write(data)

        if retainPermissions is True:
            if obj.mode:
                try:
                    os.chmod(localFilename, obj.mode)
                except:
                    pass
            if obj.owner or obj.group:
                owner = obj.owner
                group = obj.group
                if not owner or not group:
                    currentInfo = os.stat(localFilename)
                    if not owner:
                        owner = currentInfo.st_uid
                    elif not group:
                        group = currentInfo.st_gid
                                    
                    try:
                        os.chown(localFilename, int(owner), int(group))
                    except:
                        pass
            
    @classmethod
    def downloadToStr(cls, hostname, filename, password=None):
        '''
            downloadToStr - Download a hostname/filename pair and return as a string

            @param hostname <str> - Hostname that file was stored on
            @param filename <str> - Filename to fetch
            @param password <str/None> - Try this password on potentially encrpyted file.

            @return <bytes> - Data that has been downloaded

            @raises NoSuchNetFetchFile - If no hostname/filename match exists
            @raises InvalidPasswordException - If password was invalid, see getData for all conditions.
        '''
        obj = cls.objects.filter(hostname=hostname, filename=filename).all()
        if not obj:
            raise NoSuchNetFetchFile('No file matching hostname="%s" filename="%s"' %(hostname, filename))

        obj = obj[0]
        data = obj.getData(password)
        return data

    ###################################
    ##        Creation Methods       ##
    ###################################

    @classmethod
    def create(cls, filename, data, mode='', owner='', group='', password=None, hostnameOverride=None):
        '''
            create - Create and save NetFetchFile object

            @param filename <str> - filename to use for storage
            @param data     <bytes> - Data to str
            @param mode     <str>  - String or int of base-8 encoded chmod value. os.stat(x).st_mode returns this.
            @param owner    <str>  - Username owner
            @param group    <str>  - Associated group
            @param password <str/None>  - If provided, 4-32 characters to encrypt. If not provided, file will not be encrypted.
            @param hostnameOverride <None/Str> - Override hostname with this value. Default is to use current hostname.

            @return - Saved NetFetchFile object

            @raises KeyError if a hostname/filename pair already exists. use createOrUpdate to conditionally update it.
            @raises ValueError  if provided password does not meet criteria
        '''
        hostname = hostnameOverride or socket.gethostname()
        if cls.exists(hostname, filename):
            raise KeyError('A file already exists with hostname="%s" and filename="%s!\n' %(hostname, filename))
        obj = cls( \
                filename=filename,
                hostname=hostname,
                mode=mode,
                owner=owner,
                group=group,
        )

        obj.setData(data)

        if password:
            obj.encryptData(password)
        else:
            obj.encrypted = '0'

        obj.save()
        return obj

    @classmethod
    def createOrUpdate(cls, filename, data, mode='', owner='', group='', password=None, hostnameOverride=None):
        '''
            createOrUpdate - Create and save NetFetchFile object, or update an existing one.

            @param filename <str> - filename to use for storage
            @param data     <bytes> - Data to str
            @param mode     <str>  - String or int of base-8 encoded chmod value. os.stat(x).st_mode returns this.
            @param owner    <str>  - Username owner
            @param group    <str>  - Associated group
            @param password <str/None>  - If provided, 4-32 characters to encrypt. If not provided, file will not be encrypted.
            @param hostnameOverride <None/Str> - Override hostname with this value. Default is to use current hostname.

            @return - Saved NetFetchFile object

            @raises ValueError  if provided password does not meet criteria
        '''
        hostname = hostnameOverride or socket.gethostname()
        existing = cls.objects.filter(filename=filename, hostname=hostname).all()
        if existing:
            existing = existing[0]
            if mode not in (None, ''):
                existing.mode = mode
            if owner not in (None, ''):
                existing.owner = owner
            if group not in (None, ''):
                existing.group = group

            existing.setData(data)
            if password:
                existing.encryptData(password)
            else:
                existing.encrypted = '0'

            existing.save()
            return existing
        else:
            return cls.create(filename, data, mode, owner, group, password)
                    
    @classmethod
    def createOrUpdateFromFile(cls, filename, password=None, hostnameOverride=None, savePermissions=True):
        '''
            createOrUpdateFromFile - Create and save NetFetchFile object, or update an existing one, provided with a filename.

            @param filename <str> - filename to use for storage
            @param password <str/None>  - If provided, 4-32 characters to encrypt. If not provided, file will not be encrypted.
            @param hostnameOverride <None/Str> - Override hostname with this value. Default is to use current hostname.
            @param savePermissions <bool> Default True - If True, will store owner/group/mode of file.

            @return - Saved NetFetchFile object

            @raises ValueError  if provided password does not meet criteria
        '''
        if not filename:
            raise ValueError('No filename provided')
        if filename[0] != '/':
            raise ValueError('Given filename, "%s" must be absolute."' %(filename,))
        if not os.path.exists(filename):
            raise ValueError('Given filename, "%s" does not exist.' %(filename,))
        if not os.path.isfile(filename):
            raise ValueError('Given filename, "%s" is not a regular file.' %(filename,))

        with open(filename, 'rb') as f:
            data = f.read()

        if savePermissions is True:
            statData = os.stat(filename)
            (mode, owner, group) = (statData.st_mode, statData.st_uid, statData.st_gid)
        else:
            (mode, owner, group) = (None, None, None)

        return cls.createOrUpdate(filename, data, mode, owner, group, password, hostnameOverride)


    ###################################
    ##        Internal Methods       ##
    ###################################

    @staticmethod
    def _getFernetKey(password):
        '''
            _getFernetKey - Internal. Get a Fernet Key for encryption based off provided password.

            @param password <str> - 4 to 32 characters that represent a password.

            @return - A base64-encoded key that was padded to be 32-characters before encoding.

            @raises Value
        '''
        if len(password) < 4:
            raise ValueError('Password must be at least four characters.')
        if len(password) > 32:
            raise ValueError('Password cannot be longer than 32 characters')
        fernetKey = base64.b64encode(str(password + ('a' * (32 - len(password)))).encode('utf-8') )

        return fernetKey

    @staticmethod
    def calculateChecksum(data):
        '''
            calculateChecksum - Calculates a checksum from given data

            @param data <bytes> - Data to check
        '''
        return md5(data).hexdigest()

