from fastapi import FastAPI

from db.base import database
from endpoints import stats

description = '''
Stats API helps you do awesome stuff. 🚀
\nThe application is written in python using fastAPI and postgresql database.

### Stats

You will be able to:

* You can **read stats**.
* You can **create stats**.
* You can **delete all stats**.
'''

tags_metadata = [
    {
        "name": "stats",
        "description": "Operations with stats items.",
    },
]

app = FastAPI(
    title="Stats API",
    description=description,
    version="0.0.1",
    contact={
        "name": "ahillary",
        "url": "https://t.me/ahillary",
        "email": "riocrashahillary@gmail.com",
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json"
)
app.include_router(stats.router, prefix='/stats', tags=['stats'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
