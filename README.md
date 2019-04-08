aioli: async http api framework
=== 


The idea with Aioli is to provide developers with a sensible base structure and set of tools for 
building *performant*, *lightweight* and *scalable* HTTP/REST API packages that can
be easily deployed or distributed.

Furthermore, it makes use of the excellent [encode](https://github.com/encode) libraries and the *blazing fast* [uvloop](https://github.com/MagicStack/uvloop) implementation of the asyncio event loop.


[![image](https://img.shields.io/github/license/rbw/aioli.svg?style=flat-square)](https://raw.githubusercontent.com/rbw/aioli/master/LICENSE)
[![image](https://img.shields.io/pypi/v/aioli.svg?style=flat-square)](https://pypi.org/project/aioli)
[![image](https://img.shields.io/travis/rbw/aioli.svg?style=flat-square)](https://travis-ci.org/rbw/aioli)
[![image](https://img.shields.io/codecov/c/github/rbw/aioli.svg?style=flat-square)](https://codecov.io/gh/rbw/aioli)
[![image](https://img.shields.io/pypi/pyversions/aioli.svg?style=flat-square)](https://pypi.org/project/aioli/)


Features
---

- Delivers good performance and concurrency
- Scales horizontally
- Supports CORS and JWT out of the box
- Built-in ORM with support for PostgreSQL, MySQL and SQLite
- Provides intuitive tools for working with request and response data
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind


Limitations
---

- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)



Documentation
---

The documentation is available at [https://aioli.rtfd.io](https://aioli.rtfd.io). 


Examples
---

- [aioli-guestbook](https://github.com/rbw/aioli-guestbook) (CRUD guestbook example)


Project status
---

Aioli is currently under heavy development; Expect some breakage, as well as lacking documentation and tests.
That being said - I would very much appreciate people testing out the software, and perhaps even contribute with code.


Contributing
---

If you're interested in helping out in any way, let me know by creating an Issue or contact me by email.
Below are various tasks that needs completion in a first stable release. 

Check out the [Project page](https://github.com/rbw/aioli/projects/2) for planned or in progress tasks.

Author
---
Robert Wikman \<rbw@vault13.org\>
