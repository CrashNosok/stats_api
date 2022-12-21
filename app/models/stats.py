from pydantic import BaseModel, validator, condecimal
from datetime import date

from core.config import decimal_max_digits, decimal_places
from enum import Enum


class Stats(BaseModel):
    date: date
    views: int = 0
    clicks: int = 0
    cost: condecimal(max_digits=decimal_max_digits, decimal_places=decimal_places, ge=0) | None = None

    '''
    You can return this check if you want to prevent the user from entering 
    a date greater than the current one
    '''
    # @validator('date')
    # def date_check(cls, v):
    #     if datetime.now().date() > v:
    #         raise ValueError('Date too late')
    #     return v

    @validator('views', 'clicks')
    def check_negative(cls, v):
        if v < 0:
            raise ValueError('Too small number')
        return v

    @validator('cost')
    def check_cost(cls, cost, values):
        if cost > 0 and (values['clicks'] <= 0 or values['views'] < values['clicks']):
            raise ValueError('Incorrect value')
        return cost


class StatsOut(Stats):
    cpc: float = .0
    cpm: float = .0

    @validator('cpc', 'cpm')
    def precision_check(cls, v):
        return round(v, 2)


class GetStatsParams(BaseModel):
    from_: date
    to: date

    @validator('to')
    def date_sequence_check(cls, to, values):
        if to < values['from_']:
            raise ValueError('Dates should be in ascending order')
        return to


class SortModel(str, Enum):
    date: str = 'date'
    views: str = 'views'
    clicks: str = 'clicks'
    cost: str = 'cost'
    cpc: str = 'cpc'
    cpm: str = 'cpm'
