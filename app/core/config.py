from starlette.config import Config


config = Config('.env')
DATABASE_URL = config('STATS_DATABASE_URL', cast=str, default='postgresql://root:root@localhost:5432/statistics')
decimal_max_digits = 8
decimal_places = 2

