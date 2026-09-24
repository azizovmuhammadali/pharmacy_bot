import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Branch


def haversine(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    r = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


async def get_branches(session: AsyncSession) -> list[Branch]:
    result = await session.execute(select(Branch))
    return list(result.scalars().all())


async def get_branch(
    session: AsyncSession,
    branch_id: int,
) -> Branch | None:
    return await session.get(Branch, branch_id)


async def get_nearest_branch(
    session: AsyncSession,
    latitude: float,
    longitude: float,
) -> tuple[Branch | None, float | None]:
    branches = await get_branches(session)

    if not branches:
        return None, None

    nearest_branch = None
    nearest_distance = float("inf")

    for branch in branches:
        distance = haversine(
            latitude,
            longitude,
            branch.latitude,
            branch.longitude,
        )

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_branch = branch

    return nearest_branch, nearest_distance
