# Backend Challenge

Install system dependencies
-------------
 - Install python3, see [instructions](https://docs.python-guide.org/starting/install3/osx/).

Running app
-------------
Run below command:


    $ python cron_parser.py \*/15 0 1,15 \* 1-5 /usr/bin/find


Your shell attaches meaning to `*` as well. You need to escape it when calling your script to prevent the shell from expanding it (`\*`).

To print help  run below command:


    $ python cron_parser.py -h