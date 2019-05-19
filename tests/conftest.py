# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def ctrl_default():
    class TestController(BaseHttpController):
        def on_request(self, request):
            return request

        def on_ready(self):
            return dict(ready=True)

        @route('/<test_id>', 'GET')
        async def test_one(self, test_id):
            return await json({"GET": True})

        @route('/', 'GET')
        async def test_many(self, query):
            return await json({"GET": True})

        @route('/<test_id>', 'PUT')
        async def test_put(self, body, test_id):
            return await json({"GET": True})

        @route('/<test_id>', 'DELETE')
        async def test_delete(self, test_id):
            return await json({"GET": True})

        @route('/', 'POST')
        async def test_add(self, body):
            return await json({"GET": True})

    return TestController


class MockRequest:
    def __init__(self, **kwargs):
        self.method = kwargs.pop('method', 'GET')
        self.match_info = kwargs.pop('match_info', {})
        self.json = kwargs.pop('json', {})
        self.args = kwargs.pop('args', {})


@pytest.fixture
def pkg_make():
    def _loaded(*args, **kwargs):
        pkg = Package(
            *args,
            **kwargs,
            name='test1-name',
            description='test1-description'
        )
        pkg.path = '/pkg-test-1'
        return pkg

    return _loaded


@pytest.fixture
def mock_request():
    def _loaded(**kwargs):
        return 'dummy', MockRequest(**kwargs)

    return _loaded


@pytest.fixture
def logger():
    import logging
    return logging.getLogger('jet-test')
