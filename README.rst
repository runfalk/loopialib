Loopia API
==========
This is an unofficial pythonic implementation of
`Loopia's API <https://www.loopia.se/api/>`_. The default implementation is
XMLRPC-based and leaves a lot of error handling to the end user. This
implementation wraps that API which manages responses for you.


Documentation
-------------
This is alpha state software, and I haven't bothered with documentation yet.


Development
-----------
I have only implemented the features I need personally. As I need more features
I will add them. Pull requests are welcome.


But, there is another project already!
--------------------------------------
Yes, `loopia by anderspetersson <https://github.com/anderspetersson/loopia-python-api>`_
and the similar `loopiadnssync by Peter Lindblom <https://github.com/plwebse/loopiadnssync>`_.
The second does however use Loopia's DynDNS API. I know these implementations
but rolled my own because I enjoy writing these kinds of libraries. Choose
whichever you like.


Changelog
---------

Version 0.2.0
~~~~~~~~~~~~~
Released 21 August 2017

- Added helper ``split_domain`` for separating domain and sub-domain
- Added support for ``getDomain``
- Added support for ``getDomains``
- Fixed a problem where errors would not get raised on some types of API calls


Version 0.1.0
~~~~~~~~~~~~~
Released 2nd November 2016

- Initial release
