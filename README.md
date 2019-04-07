aioli: async http api framework
=== 

[![image](https://img.shields.io/github/license/rbw/aioli.svg?style=flat-square)](https://raw.githubusercontent.com/rbw/aioli/master/LICENSE)
[![image](https://img.shields.io/pypi/v/aioli.svg?style=flat-square)](https://pypi.org/project/aioli)
[![image](https://img.shields.io/travis/rbw/aioli.svg?style=flat-square)](https://travis-ci.org/rbw/aioli)
[![image](https://img.shields.io/codecov/c/github/rbw/aioli.svg?style=flat-square)](https://codecov.io/gh/rbw/aioli)
[![image](https://img.shields.io/pypi/pyversions/aioli.svg?style=flat-square)](https://pypi.org/project/aioli/)


The idea with Aioli is to provide developers with a sensible base structure and set of tools for 
building *performant*, *lightweight* and *scalable* HTTP API packages that can
be easily deployed or distributed.

Aioli makes use of the excellent [encode](https://github.com/encode) libraries and the *blazing fast* [uvloop](https://github.com/MagicStack/uvloop) implementation of the asyncio event loop.

Features and limitations:
- Delivers good performance and concurrency
- Scales horizontally
- Supports CORS and JWT out of the box
- Built-in ORM with support for Postgres, Mysql and SQLite
- Provides intuitive tools for object serialization
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind
- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)

Furthermore, Aioli comes with a REST API browser, try it out at [https://demo.aioli.dev](https://demo.aioli.dev).

Getting started
---

Head over to the documentation at [https://aioli.rtfd.io](https://aioli.rtfd.io),
or check out the [guestbook](https://github.com/rbw/aioli-guestbook) example.
 


Development
---
While Aioli does work, it's currently under heavy development; Expect some breakage, as well as lacking documentation and tests.
That being said - I would very much appreciate people testing out the software, and perhaps even contribute with code.

#### Tasks
If you're interested in helping out in any way, let me know by creating an Issue or contact me by email.
Below are various tasks that needs completion in a first stable release. 

##### Currently in progress
- [ ] [Admin UI/OpenAPI](https://github.com/rbw/aioli/projects/2#card-19607055)
- [ ] [API documentation](https://github.com/rbw/aioli/projects/2#card-19606997)
- [ ] [Unit Tests](https://github.com/rbw/aioli/projects/2#card-19607051)
- [ ] [CORS support](https://github.com/rbw/aioli/projects/2#card-19607029)

##### Todo
- [ ] [WebSocket support](https://github.com/rbw/aioli/projects/2#card-19607124)
- [ ] [Users package](https://github.com/rbw/aioli/projects/2#card-19607040)
- [ ] [Authentication package](https://github.com/rbw/aioli/projects/2#card-19607036)
- [ ] [Project Wiki](https://github.com/rbw/aioli/projects/2#card-19607041)
- [ ] [GraphQL support](https://github.com/rbw/aioli/projects/2#card-19607100)
- [ ] [Command-line interface](https://github.com/rbw/aioli/projects/2#card-19607045)

Author
---
Robert Wikman \<rbw@vault13.org\>
