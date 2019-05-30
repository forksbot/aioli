Aioli: Non-blocking HTTP API Framework and Toolkit
=== 

[![image](https://img.shields.io/github/license/rbw/aioli.svg?style=flat-square)](https://raw.githubusercontent.com/rbw/aioli/master/LICENSE)
[![image](https://img.shields.io/pypi/v/aioli.svg?style=flat-square)](https://pypi.org/project/aioli)
[![image](https://img.shields.io/travis/rbw/aioli.svg?style=flat-square)](https://travis-ci.org/rbw/aioli)
[![image](https://img.shields.io/codecov/c/github/rbw/aioli.svg?style=flat-square)](https://codecov.io/gh/rbw/aioli)
[![image](https://img.shields.io/pypi/pyversions/aioli.svg?style=flat-square)](https://pypi.org/project/aioli/)

Aioli is a Framework and Toolkit for building, shipping and running performant and highly composable WebSocket and RESTful HTTP APIs using Python 3 Asyncio. 
It provides a sensible separation between request/response handling (transformation, validation, etc), application logic and data access layers.

Features
---

- High performance and concurrency, lightweight
- Horizontally scalable
- Built-in ORM with support for PostgreSQL and MySQL
- Intuitive tools for working with request and response data
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind

Limitations
---

- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)


Documentation
---

The documentation is available at [https://docs.aioli.dev](https://docs.aioli.dev). 


Package Index
--

Shortly, the [https://pkgs.aioli.dev](https://pkgs.aioli.dev) website will show useful info about verified packages; Trust status,
install instructions, author and license data, as well as links to source code and more.


Examples
---

- [Aioli Guestbook Example](https://github.com/aioli-framework/aioli-guestbook-example): Comprehensive RESTful HTTP API.
- [Monsoon](https://github.com/rbw/monsoon): RESTful HTTP API and WebSocket relay for Livestatus.


Project status
---

Aioli is currently under heavy development; Expect some breakage, as well as lacking documentation and tests.


Contributing
---

If you're interested in helping out in any way, let me know by creating an Issue or contact me by email.
Below are various tasks that needs completion in a first stable release. 

Check out the [Project page](https://github.com/rbw/aioli/projects/2) for planned or in progress tasks.

Author
---
Robert Wikman \<rbw@vault13.org\>
