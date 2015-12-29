NetFetch
========

Networked file storage and retrieval with optional password protection using Redis.


Files are stored with a key of originating hostname and an absolute path to filename.


Files may be stored with a password, in which they are encrypted and the same password must be used to retrieve the data.


**Storage**


Store files using *netFetchPut*.

	Usage: netFetchPut (options) [absolute filename]

		  Stores a given file in NetFetch, optionally password\-protecting it as well.


		Options:


			\-\-password                 Prompt for password on storing this file


			\-\-password\-file=fname      Read password from a given filename instead of tty. Implies \-\-password.

			

			\-\-no\-preserve              Do not store owner/group/mode information


			\-\-config=/path/x.txt       Use provided config for redis. Default is to look in /etc/netfetch.cfg


			\-\-old\-format                Use Version 1.0 format (base64\-encoded) instead of directly encoded. This is much slower, but added because 1.0 data format is incompatible with the new format.


		Provided filename must be an absolute path.


	Example: netFetchPut /Data/myfile.db


**Retrieval**

Retrieve files using *netFetchGet*

	Usage: netFetchGet (options) [hostname] [filename] [output filename]

		Downloads a file uploaded from hostname, given an absolute filename.

		If "output filename" is "\-\-", output will be to stdout. 


		Options:


			\-\-password                  Prompts for password. If file is encrypted, a password must be provided.


			\-\-password\-file=fname       Read password from a given filename instead of tty. Implies \-\-password.

		  

			\-\-no\-preserve               Do not apply stored attributes (owner/group/mode)


			\-\-config=/path/config.cfg   Use provided config for redis. Default is to look in /etc/netfetch.cfg


			\-\-old\-format                Use Version 1.0 format (base64\-encoded) instead of directly encoded. This is much slower, but added because 1.0 data format is incompatible with the new format.


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

Backwards Incompatible Changes
------------------------------

Version 2.0 updated the storage format to a much more efficient form (directly stores instead of base64\-encoding/decoding). This makes everything much faster and take up less space, but is incompatible with versions prior to 2.0. To fetch/put a file using the old format, use "\-\-old\-format" with netFetchGet/netFetchPut.


To Migrate, fetch any files using "\-\-old\-format", and then store them back without that flag. There is not an automatic util, because of encryption.

Version 2.0 also depends on IndexedRedis of at least version 2.9.0


API
---

Can be found  http://htmlpreview.github.io/?https://github.com/kata198/NetFetch/blob/master/doc/NetFetch.html .

