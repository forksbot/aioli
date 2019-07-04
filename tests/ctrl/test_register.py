import pytest


@pytest.fixture
def ctrl(ctrl_default):
    return ctrl_default()


@pytest.fixture
def pkg(pkg_make, ctrl_default):
    return pkg_make(controller=ctrl_default)


def test_route_consume(ctrl):
    """Pending routes should get consumed on iteration"""

    # Consume pending routes
    routes = list(ctrl.pending_routes)

    # Make sure we got routes back and all pending routes were consumed.
    assert len(routes) > 0
    assert list(ctrl.pending_routes) == []


def test_consumed_refs(ctrl):
    """Consumed route handlers should exist in Controller instance"""

    for handler, _route, schema in ctrl.pending_routes:
        # Get defined route handler
        routed_handler = getattr(ctrl, _route.name)

        # Ensure routed handler is defined
        assert id(routed_handler.__func__) == id(handler.__func__)


def test_register(ctrl, pkg):
    """Registering a controller should set pkg, path and log"""

    assert ctrl.pkg is None
    ctrl.register(pkg)
    assert ctrl.pkg
    assert ctrl.path
    assert ctrl.log

