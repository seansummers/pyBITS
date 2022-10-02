TODO
====
Uploads
-------
 * UploadReply, anyone?
 * make session management and file management pluggable
 * work on the download server (are there extensions/optimizations beyond stanard HTTP/1.1?)
 * get `Fragment` size negotiation working. The first Fragment seems to always be 168000. 413 doesn't work.

Downloads
---------
 * `HEAD` must return file size
 * `GET` must support Content-Range and Content-Length
 * 180 bytes of other Headers max

 Bugs
 ----
  * nothing setting the timestamp is ever sent by Microsoft BITS clients
  * `Content-Name` has never been seen, either
