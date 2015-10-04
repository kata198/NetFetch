# NetFetch
Networked file storage and retrieval with optional password protection using Redis.


Files are stored with a key of originating hostname and an absolute path to filename.

Files may be stored with a password, in which they are encrypted and the same password must be used to retrieve the data.


Storage
-------

Store files using *netFetchPut*.

	Usage: netFetchPut (options) [absolute filename]
		  Stores a given file in NetFetch, optionally password-protecting it as well.

		Options:

			--password                 Prompt for password on storing this file
			--password-file=fname      Read password from a given filename instead of tty. Implies --password.
			
			--no-preserve              Do not store owner/group/mode information

			--config=/path/x.cfg       Use provided config for redis. Default is to look in ~/.netfetch.cfg then /etc/netfetch.cfg

		Provided filename must be an absolute path.

	Example: netFetchPut /Data/myfile.db

Retrieval
---------

Retrieve files using *netFetchGet*

	Usage: netFetchGet (options) [hostname] [filename] [output filename]
		Downloads a file uploaded from hostname, given an absolute filename.
		If "output filename" is "--", output will be to stdout. 

		Options:

			--password                  Prompts for password. If file is encrypted, a password must be provided.
			--password-file=fname       Read password from a given filename instead of tty. Implies --password.
		  
			--no-preserve               Do not apply stored attributes (owner/group/mode)

			--config=/path/config.cfg   Use provided config for redis. Default is to look in ~/.netfetch.cfg then /etc/netfetch.cfg

		Provided filename must be an absolute path.

	Example: netFetchGet filestore01 /Data/myfile.db


Configuration
-------------

The Redis server on which to connect is specified by a config file. The applications will check first $HOME/.netfetch.cfg, then /etc/netfetch.cfg if a \-\-config=/path/to/netfetch.cfg is not provided.


Example Configuration:

	[redis]
	host=127.0.0.1
	port=6379
	db=1


API
---

Can be found  http://htmlpreview.github.io/?https://github.com/kata198/NetFetch/blob/master/doc/NetFetch.html .

