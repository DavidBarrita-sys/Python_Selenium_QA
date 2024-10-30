import asyncpg
from typing import Dict

DATABASE_CONFIG = {
    'user': 'userqa',
    'password': 'aHRn1UVGUCJpgWIIOGMCQYu4Y71T0MjX',
    'database': 'mean_machine_qa_6j1s',
    'host': 'dpg-csc1g1g8fa8c738ror80-a.oregon-postgres.render.com',
    'port': '5432'
}


class DatabaseConnection:
    def __init__(self, config: Dict):
        self.config = config
        self.connection = None

    async def __aenter__(self):
        self.connection = await asyncpg.connect(**self.config)
        return self.connection

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.connection.close()


async def fetch_user_forecast_count(connection, user_name: str, forecast_value: str) -> int:
    query = """
    SELECT COUNT(*) AS total_forecasts
    FROM "MeanMachine_forecast" mmf
    INNER JOIN "MeanMachine_user" mmu
    ON mmf."idUser" = mmu.id
    WHERE mmu."userName" = $1 AND mmf.forecast = $2;
    """
    return await connection.fetchval(query, user_name, forecast_value)