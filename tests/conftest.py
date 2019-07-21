import pytest


class MockRequest:
    def __init__(self, **kwargs):
        self.method = kwargs.pop("method", "GET")
        self.match_info = kwargs.pop("match_info", {})
        self.json = kwargs.pop("json", {})
        self.args = kwargs.pop("args", {})


@pytest.fixture
def pkg_make():
    def _loaded(*args, **kwargs):
        pkg = Package(
            *args,
            **kwargs,
            name="test1-name",
            description="test1-description"
        )
        pkg.path = "/pkg-test-1"
        return pkg

    return _loaded


@pytest.fixture
def mock_request():
    def _loaded(**kwargs):
        return "dummy", MockRequest(**kwargs)

    return _loaded


@pytest.fixture
def logger():
    import logging
    return logging.getLogger("jet-test")
