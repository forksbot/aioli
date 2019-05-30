Usage
=====

Packages are created using the :class:`aioli.Package` class, referencing one or more components.


**API**

.. automodule:: aioli
.. autoclass:: Package
   :members:


.. important::

    The Package's __init__.py file must have a ``__version__`` variable set to be successfully registered with the :class:`aioli.Application`.

**Example**

.. code-block:: python

    from aioli import Package
    from aioli_guestbook import service
    from .service import VisitService, VisitorService
    from .model import VisitModel, VisitorModel
    from .controller import Controller

    __version__ = '0.1.0'

    export = Package(
        controller=Controller,
        services=[VisitService, VisitorService],
        models=[VisitModel, VisitorModel],
        name='guestbook',
        description='Example guestbook package'
    )
