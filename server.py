import asyncio
from uvicorn import Server, Config
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import MONGO_HOST


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/logs/{collection_name}', response_class=HTMLResponse)
async def live(request: Request, collection_name: str, q: str = '', page: int = 1):
    limit = 1000
    if collection_name == 'dafaresult':
        limit = 200
    pages = await client[collection_name].count_documents({}) // 1000
    if q:
        result = [f"{i['message']}" async for i in client[collection_name].find({'message': {'$regex': f'{q}'}})]
    else:
        result = [f"{i['message']}" async for i in client[collection_name].find({}).skip(1000 * (page - 1)).limit(limit)]
    return templates.TemplateResponse('index.html', {'request': request,
                                                     'result': result,
                                                     'name': collection_name,
                                                     'pages': pages})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    config = Config(app=app, loop=loop, host='0.0.0.0', port=5001)
    server = Server(config)
    client = AsyncIOMotorClient(host=MONGO_HOST, io_loop=loop).logs
    loop.run_until_complete(server.serve())

