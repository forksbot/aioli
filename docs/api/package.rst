Package
=======


The :class:`~aioli.Package` class is used for defining a Package and making its components eligible for use.


.. automodule:: aioli
.. autoclass:: Package
   :members:

*Example*

.. code-block:: python

    from aioli import Package
    from aioli_guestbook import service
    from .service import VisitService, VisitorService
    from .database import VisitModel, VisitorModel
    from .controller import GuestbookHttpController

    export = Package(
        controllers=[GuestbookHttpController],
        services=[VisitService, VisitorService],
        models=[VisitModel, VisitorModel],
        name="aioli-guestbook",
        version="0.1.0",
        description="Example guestbook package"
    )
