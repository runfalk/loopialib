Loopia API
==========
This is an unofficial pythonic implementation of `Loopia's API <https://www.loopia.se/api/>`_. The default implementation is XMLRPC-based and leaves a lot of error handling to the end user. This implementation wraps that API which manages responses for you.


Documentation
-------------
This is alpha state software, and I haven't bothered with documentation yet. The source is about 100 lines of code and shouldn't be hard to understand.


Development
-----------
I have only implemented DNS (Zone) related API calls so far. There isn't more on the roadmap as of now since that fits my use case. However, pull requests are always welcome to extend the existing functionality.


But, there is another project already!
--------------------------------------
Yes, `loopia by anderspetersson <https://github.com/anderspetersson/loopia-python-api>`_ and the similar `loopiadnssync by Peter Lindblom <https://github.com/plwebse/loopiadnssync>`_. The second does however use Loopia's DynDNS API. I know these implementations but rolled my own because I enjoy writing these kinds of libraries. Choose whichever you like.


Changelog
---------

Version 0.1.0
~~~~~~~~~~~~~
Released ...

- Initial release
