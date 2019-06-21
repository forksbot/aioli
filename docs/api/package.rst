.. _package-docs:

Package
=======


A *Package* is a namespaced and labelled group of components that can be imported into an :class:`~aioli.Application`.

There are two main components for building Web API Packages: :ref:`controller-docs` & :ref:`service-docs`

When developing an Aioli application, local *Packages* typically contain code that makes sense to modularize in the Application at hand.


.. automodule:: aioli
.. autoclass:: Package
   :members:

Example – Creating a Package with Controller and Service layers

.. code-block:: python

    from aioli import Package

    from .service import VisitService, VisitorService
    from .controller import HttpController
    from .config import ConfigSchema


    export = Package(
        name="aioli_guestbook",
        version="0.1.0",
        description="Example guestbook Package",
        controllers=[HttpController],
        services=[VisitService, VisitorService],
        config=ConfigSchema,
    )


