# SMAT

_SMAT_ (**S**tring **ma**nipulation **t**ool) is a simple utility to modify batches of text lines. It can add, as well as remove prefixes and suffixes and is
intended for content that follow some sort of format, e.g. log files.

Suppose a log file looks like this

```log
INFO 14:30 : server starting
INFO 14:31 : all services up and running
TRACE 14:40 : New request: /index.html
ERROR 14:40 : Cannot load index.html - no such file
INFO 14:50 : Server shut down per user request
```

and you want to extract (for whatever reason) the timestamps when each log entry occurred. With smat, this can be achieved as follows:

`smat --drop-prefix "((INFO)|(TRACE)|(ERROR)) " --drop-suffix " : .*$" --input example.log`.

Under the hood smat uses Python regular expressions, leading to a very powerful specification of the patterns to remove.

In addition to its command-line interface, the various functions can also be used directly from other Python code.
