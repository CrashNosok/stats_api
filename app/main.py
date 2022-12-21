from fastapi import FastAPI

from db.base import database
from endpoints import stats

app = FastAPI(title='Stats project')
app.include_router(stats.router, prefix='/stats', tags=['stats'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
