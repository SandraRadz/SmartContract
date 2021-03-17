import asyncio
import logging
import pathlib

from aiohttp import web

PROJECT_ROOT = pathlib.Path(__file__).parent.parent

BACKGROUND_QUEUE = asyncio.Queue()


async def process_contract(*, item):
    # TODO: contract processing
    print(item)


async def background_processor():
    while True:
        item = await BACKGROUND_QUEUE.get()

        if item is None:
            return

        if isinstance(item, Exception):
            raise item

        await process_contract(item=item)

        await asyncio.sleep(0)


async def start_background_tasks(app):
    app['dispatch'] = app.loop.create_task(background_processor())


async def cleanup_background_tasks(app):
    BACKGROUND_QUEUE.put_nowait(None)

    app['dispatch'].cancel()
    await app['dispatch']


async def health_check(_request):
    return web.json_response({'status': 'health'})


async def parse_request(*, request):
    # TODO: parsing request
    _body = await request.json()


async def create_contract(request):
    params = await parse_request(request=request)

    BACKGROUND_QUEUE.put_nowait(params)

    return web.json_response({'success': True})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    web_app = web.Application()
    web_app.add_routes([
        web.post('/contracts', create_contract),
        web.get('/healthCheck', health_check)
    ])

    web.run_app(web_app, host='localhost', port=1488)
