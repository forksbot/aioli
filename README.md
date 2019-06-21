Aioli: Non-blocking Web API Framework
=== 

[![image](https://img.shields.io/github/license/rbw/aioli.svg?style=flat-square)](https://raw.githubusercontent.com/rbw/aioli/master/LICENSE)
[![image](https://img.shields.io/pypi/v/aioli.svg?style=flat-square)](https://pypi.org/project/aioli)
[![image](https://img.shields.io/travis/rbw/aioli.svg?style=flat-square)](https://travis-ci.org/rbw/aioli)
[![image](https://img.shields.io/codecov/c/github/rbw/aioli.svg?style=flat-square)](https://codecov.io/gh/rbw/aioli)
[![image](https://img.shields.io/pypi/pyversions/aioli.svg?style=flat-square)](https://pypi.org/project/aioli/)



Aioli is a Framework for building RESTful HTTP and WebSocket API packages, with a sensible separation between request/response handling (transformation, validation, etc), application logic and data access layers.

Furthermore, it makes use of [asyncio](https://docs.python.org/3/library/asyncio.html), is lightweight and provides good performance and concurrency.

Want to know more? Check out the [docs](https://docs.aioli.dev) or the [aioli-framework/aioli-guestbook-example](https://github.com/aioli-framework/aioli-guestbook-example) for a RESTful HTTP API example Package.


Features
---

- High performance and concurrency, lightweight
- Horizontally scalable
- Simple component system with high composability
- Intuitive tools for working with request and response data
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind
- Licensed under MIT

Limitations
---

- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)


Documentation
---

The documentation is available at [https://docs.aioli.dev](https://docs.aioli.dev). 


Packages
---

Shortly, the https://pkgs.aioli.dev website will show useful info about 1st and verified 3rd-party Packages; trust status, install instructions, author and license data, as well as links to source code and more.

Currently, 1st-party extension-type Packages can be found at [github.com/aioli-framework](https://github.com/aioli-framework).


Project status
---

Aioli is currently under heavy development; Expect some breakage, as well as lacking documentation and tests.


Author
---
Robert Wikman \<rbw@vault13.org\>
