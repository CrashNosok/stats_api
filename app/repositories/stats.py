from models.stats import Stats as StatsModel,\
                        StatsOut as StatsOutModel,\
                        TimePeriod,\
                        SortModel
from db.stats import Stats as StatsDB
from .base import BaseRepository


def add_cpc_and_to_object(obj: StatsOutModel):
    if obj.clicks != 0:
        obj.cpc = obj.cost / obj.clicks
    if obj.views != 0:
        obj.cpm = obj.cost / obj.views * 1000


class StatsRepository(BaseRepository):
    async def get_all(self,
                    time_period: TimePeriod,
                    sort_field: SortModel,
                    limit: int,
                    skip: int) -> list[StatsOutModel]:
        query = StatsDB.select()\
            .where(StatsDB.c.date.between(
                time_period.from_, time_period.to))\
            .limit(limit)\
            .offset(skip)
        rows = await self.database.fetch_all(query)
        result = []
        for row in rows:
            obj = StatsOutModel.parse_obj(row)
            add_cpc_and_to_object(obj=obj)
            result.append(obj)
        return sorted(result, key=lambda d: getattr(d, str(sort_field.value)))


    async def create(self, stats: StatsModel) -> StatsOutModel:
        select_query = StatsDB.select().where(StatsDB.c.date == stats.date)
        old_stats = await self.database.fetch_one(select_query)

        if old_stats is not None:
            old_stats_obj: StatsModel = StatsModel.parse_obj(old_stats)
            query = StatsDB.update().where(StatsDB.c.date == stats.date).values(
                views=old_stats_obj.views + stats.views,
                clicks=old_stats_obj.clicks + stats.clicks,
                cost=old_stats_obj.cost + stats.cost,
            )
        else:
            query = StatsDB.insert().values(**stats.dict())
        await self.database.execute(query)
        stats_out = StatsOutModel.parse_obj(stats)
        add_cpc_and_to_object(obj=stats_out)
        return stats_out


    async def remove_all(self) -> None:
        await self.database.execute(StatsDB.delete())
