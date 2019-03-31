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

It's built on top of [aiohttp](https://github.com/aio-libs/aiohttp) and uses the *blazing fast* [uvloop](https://github.com/MagicStack/uvloop) implementation of the asyncio event loop.

Features and limitations:
- Delivers performance and concurrency
- Scales horizontally
- Supports CORS and JWT out of the box
- Has built-in support for [Postgres](https://www.postgresql.org) databases
- Provides intuitive tools for object serialization
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind
- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)

Also - Aioli comes with a REST API browser, try it out at [https://demo.aioli.dev](https://demo.aioli.dev).

Getting started
---

Read the documentation at [https://aioli.rtfd.io](https://aioli.rtfd.io),
or check out the [jet-guestbook](https://github.com/rbw/jet-guestbook) example.
 


Development
---
While Aioli does work, it's currently under heavy development; Expect some breakage, as well as lacking documentation and tests.
That being said - I would very much appreciate people testing out the software, and perhaps even contribute with code.

#### Tasks
If you're interested in helping out in any way, let me know by creating an Issue or contact me by email.
Below are various tasks that needs completion in a first stable release. 

##### Currently in progress
- [ ] [Admin UI/OpenAPI](https://github.com/rbw/aioli/projects/2#card-17017968)
- [ ] [API documentation](https://github.com/rbw/aioli/projects/2#card-17018073)
- [ ] [Unit Tests](https://github.com/rbw/aioli/projects/2#card-17018080)

##### Todo
- [ ] [CORS support](https://github.com/rbw/aioli/projects/2#card-17018027)
- [ ] [GraphQL support](https://github.com/rbw/aioli/projects/2#card-17018036)
- [ ] [Users package](https://github.com/rbw/aioli/projects/2#card-17018007)
- [ ] [Authentication package](https://github.com/rbw/aioli/projects/2#card-17018013)
- [ ] [Project Wiki](https://github.com/rbw/aioli/projects/2#card-17017985)
- [ ] [Command-line interface](https://github.com/rbw/aioli/projects/2#card-17017975)
- [ ] [Modular core](https://github.com/rbw/aioli/projects/2#card-18585354)

Author
---
Robert Wikman \<rbw@vault13.org\>
