from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from datetime import date, datetime

from repositories.stats import StatsRepository
from .depends import get_stats_repository
from models.stats import Stats, GetStatsParams, StatsOut, SortModel


router = APIRouter()


@router.get('/', response_model=list[StatsOut])
async def read_stats(
                    from_: date = Query(default=datetime.now().date(), alias='from'),
                    to: date = Query(default=datetime.now().date()),
                    sort_field: SortModel = SortModel.date,
                    limit: int = 100,
                    skip: int = 0,
                    stats_methods: StatsRepository = Depends(get_stats_repository)
                    ) -> list[StatsOut]:
    return await stats_methods.get_all(
        GetStatsParams(from_=from_, to=to), 
        sort_field=sort_field,
        limit=limit, 
        skip=skip)


@router.post('/', response_model=Stats)
async def create_stats(stats: Stats,
                       stats_methods: StatsRepository = Depends(get_stats_repository)
                       ) -> JSONResponse:
    await stats_methods.create(stats=stats)
    return JSONResponse(
        content={"message": "OK"},
        status_code=status.HTTP_200_OK
    )


@router.delete('/remove/')
async def remove_stats(stats_methods: StatsRepository = Depends(get_stats_repository)) -> JSONResponse:
    await stats_methods.remove_all()
    return JSONResponse(
        content={"message": "OK"},
        status_code=status.HTTP_200_OK
    )
