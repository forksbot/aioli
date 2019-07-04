from aioli.controller import route


async def test_vanilla(mock_request):
    """Not providing a schema should result in the request getting passed directly to handler"""

    @route('/', 'GET')
    async def vanilla_handler(_, request):
        assert id(req[1]) == id(request)
        return

    req = mock_request(args={'foo': 'bar'})
    await vanilla_handler(*req)

