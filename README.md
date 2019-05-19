aioli: async http api framework
=== 

[![image](https://img.shields.io/github/license/rbw/aioli.svg?style=flat-square)](https://raw.githubusercontent.com/rbw/aioli/master/LICENSE)
[![image](https://img.shields.io/pypi/v/aioli.svg?style=flat-square)](https://pypi.org/project/aioli)
[![image](https://img.shields.io/travis/rbw/aioli.svg?style=flat-square)](https://travis-ci.org/rbw/aioli)
[![image](https://img.shields.io/codecov/c/github/rbw/aioli.svg?style=flat-square)](https://codecov.io/gh/rbw/aioli)
[![image](https://img.shields.io/pypi/pyversions/aioli.svg?style=flat-square)](https://pypi.org/project/aioli/)

Aioli is a Framework for building Performant, Lightweight, Scalable and Portable WebSocket and RESTful HTTP API 
packages. It provides a sensible separation between requests/response handling, transformation, 
validation, application logic and data access layers. 
 

Features
---

- High performance and concurrency, lightweight
- Built-in WebSocket and Redis/PubSub support
- Horizontally scalable
- Built-in ORM with support for PostgreSQL and MySQL
- Intuitive tools for working with request and response data
- Created with [Docker](https://www.docker.com) and [Kubernetes](https://kubernetes.io) in mind

Limitations
---

- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be [asynchronous](https://docs.python.org/3/library/asyncio.html)


Package Index
--

The https://pkgs.aioli.dev website shows useful info about verified Packages', such as trust status,
install instructions, author and license data, as well as links to source code and more.

1. Install Aioli

`$ pip install aioli`

2. Create a new Github repository and clone it

`$ git clone <Github repository URL>`

3. Initialize the Package 
```
$ aioli pkg init <name>

** Add base structure
** Add .gitignore
** Add poetry config
** Add pytest.ini
** Add README.md
** Add LICENSE
** Add .travis.yml
```


Documentation
---

The documentation is available at [https://aioli.rtfd.io](https://aioli.rtfd.io). 


Examples
---

- [monsoon](https://github.com/rbw/monsoon) (Livestatus REST API)
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
