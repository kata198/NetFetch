NetFetch
========

Networked file storage and retrieval with optional password protection and compression using Redis.


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


			\-\-compress(=mode)          Compress the file data for storage (and decompress after fetch).

									   Default compression mode is lzma.

									   Use just --compress for this default mode.

									   You can specify an alternate mode by appending =MODE after --compress.

									   Supported modes are: 'lzma' (aka xz)   'gzip'   'bzip2'



	Provided filename is treated as an absolute path. You can use a relative path, but it will be expanded

	  to absolute for storage. Upon fetch, you can use the same relative path, so long as it resolves

	  to the same absolute location. It is safest to just specify an absolute path yourself.


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


	Provided filename is treated as an absolute path. You can use a relative path, but it will be expanded

	  to absolute for storage. Upon fetch, you can use the same relative path, so long as it resolves

	  to the same absolute location. It is safest to just specify an absolute path yourself.


	Example: netFetchGet filestore01 /Data/myfile.db

**Delete**

Delete files using *netFetchDelete*

	Usage: netFetchDelete (options) [hostname] [filename]

	  Deletes a NetFetch file off of provided hostname.



		Options:


		  --config=/path/config.cfg   Use provided config for redis. Default is to look in ~/.netfetch.cfg then /etc/netfetch.cfg



		Provided filename is treated as an absolute path. You can use a relative path, but it will be expanded

		  to absolute for storage. Upon fetch, you can use the same relative path, so long as it resolves

		  to the same absolute location. It is safest to just specify an absolute path yourself.


	 Example: netFetchDelete filestore01 /Data/myfile.db


Configuration
-------------

The Redis server on which to connect is specified by a config file. The applications will check first $HOME/.netfetch.cfg, then /etc/netfetch.cfg if a \-\-config=/path/to/netfetch.cfg is not provided.


Example Configuration:

	[redis]

	host=127.0.0.1

	port=6379

	db=1


Compression
-----------

Starting with version 3.0, NetFetch supports compression. This is provided during netFetchPut by the "--compress" flag.

The default compression mode is lzma ( aka "lz" ). To use a different compression mode, specify "--compress=MODE" where MODE is one of lzma/xz , gzip/gz , bzip2/bz2 .

Compression only need be specified on Put, Get will automatically detect which mode and decompress the results.

Backwards Incompatible Changes
------------------------------

Version 3.0 requires IndexedRedis > 5.0.0 and < 7.0.0. If you must use a version less-than 5.0.0, use version 2.0.3.

The data format used by 3.0 is compatible with version 2.0 data format, but has dropped support for 1.x format. Everything henceforth should be forward-compatible with all future versions.


Version 2.0 updated the storage format to a much more efficient form (directly stores instead of base64\-encoding/decoding). This makes everything much faster and take up less space, but is incompatible with versions prior to 2.0. To fetch/put a file using the old format, use "\-\-old\-format" with netFetchGet/netFetchPut.


To Migrate, fetch any files using "\-\-old\-format", and then store them back without that flag. There is not an automatic util, because of encryption.

Version 2.0 also depends on IndexedRedis of at least version 2.9.0


API
---

Can be found  http://htmlpreview.github.io/?https://github.com/kata198/NetFetch/blob/master/doc/NetFetch.html .

