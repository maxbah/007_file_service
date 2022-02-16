import json

from aiohttp import web
from src.file_service import RawFileService
from src.file_service import FileService
from src.file_service import SignedFileService
from src.file_service import EncryptedFileService


class Handler:

    def __init__(self, *args, **kwargs):
        self.file_service = RawFileService()

    async def ls(self, request, *args, **kwargs):
        list_dir = self.file_service.ls()
        return web.Response(text='\n'.join(list_dir))

    async def cd(self, request, *args, **kwargs):
        dir = request.query['dir']
        print("Directory:", dir)
        self.file_service.cd(dir)
        return web.Response(text=__name__)

    async def read(self, request, *args, **kwargs):
        filename = request.query['filename']
        print("Filename:", filename)
        data = self.file_service.read(filename)
        return web.Response(text=data)

    async def read_metadata(self, request, *args, **kwargs):
        filename = request.query['filename']
        print("Filename:", filename)
        create_date, modification_date, file_size = self.file_service.read_metadata(filename)
        return web.Response(text=json.dumps({"create_date": create_date,
                                             "modification_date": modification_date,
                                             "file_size": file_size}))

    async def write(self, request: web.Request, *args, **kwargs):
        data = b''
        while not request.content.at_eof():
            print("REQ CONT:", request.content.read())
            data += await request.content.read()
        print('DATA:', data)
        filename = self.file_service.create(data.decode())
        data = {'Create filename': filename}
        return web.Response(text=json.dumps(data))

    async def get_cwd(self, request, *args, **kwargs):
        pwd = self.file_service.get_cwd()
        return web.Response(text=pwd)

    async def remove(self, request, *args, **kwargs):
        filename = request.query['filename']
        res = self.file_service.remove(filename)
        return web.Response(text=res)


def create_app():
    app = web.Application()
    handler = Handler()
    app.add_routes([
        web.get('/ls', handler.ls),
        web.put('/cd', handler.cd),
        web.get('/pwd', handler.get_cwd),
        web.get('/read_meta', handler.read_metadata),
        web.get('/read', handler.read),
        web.get('/remove', handler.remove),
        web.post('/write', handler.write)

    ])
    return app
