from fastapi import APIRouter, Depends, status

from repositories.stats import StatsRepository
from .depends import get_stats_repository
from models.stats import Stats, TimePeriod, StatsOut, SortModel


router = APIRouter()


@router.get(
    '/',
    response_model=list[StatsOut],
    tags=['stats'],
    status_code=status.HTTP_200_OK,
    summary='Returns a sorted list of stats objects',
)
async def read_stats(
                    time_period: TimePeriod = Depends(),
                    sort_field: SortModel = SortModel.date,
                    limit: int = 100,
                    skip: int = 0,
                    stats_methods: StatsRepository = Depends(get_stats_repository)
                    ) -> list[StatsOut]:
    """
    Returns a sorted list of stats objects:

    - **sort_field**: by which field to sort objects
    - **limit**: the maximum number of stats objects retrieved from the database
    - **skip**: how many stats objects to skip from the database before getting the set
    - **from_**: start date of the period (inclusive)
    - **to**: period end date (inclusive)
    """
    return await stats_methods.get_all(
        time_period=time_period,
        sort_field=sort_field,
        limit=limit, 
        skip=skip)


@router.post(
    '/', 
    response_model=StatsOut,
    tags=['stats'], 
    status_code=status.HTTP_201_CREATED,
    summary='Create a stats item',
)
async def create_stats(stats: Stats,
                       stats_methods: StatsRepository = Depends(get_stats_repository)
                       ) -> StatsOut:
    """
    Create a stats item:

    - **date**: event date
    - **views**: tumber of impressions
    - **clicks**: tumber of clicks
    - **cost**: click cost
    """
    return await stats_methods.create(stats=stats)


@router.delete(
    '/', 
    tags=['stats'],
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Removes all stats objects from the database',
)
async def remove_stats(stats_methods: StatsRepository = Depends(get_stats_repository)) -> None:
    """
    Removes all stats objects from the database
    """
    await stats_methods.remove_all()
