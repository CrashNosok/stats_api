from repositories.stats import StatsRepository
from db.base import database


def get_stats_repository() -> StatsRepository:
    return StatsRepository(database)
