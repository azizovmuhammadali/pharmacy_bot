from aiogram import F, Router
from aiogram.types import Message

from bot import texts as T
from bot.services import branch as branch_service

router = Router()


@router.message(F.location)
async def nearest_branch(message: Message, session):
    branch, distance = await branch_service.get_nearest_branch(
        session=session,
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )

    if not branch:
        await message.answer(T.NO_BRANCHES_USE_ADDRESS)
        return

    await message.answer(
        text=(
            f"{T.NEAREST_BRANCH_TITLE}\n\n"
            f"{branch.name}\n"
            f"{T.BRANCH_ADDRESS}: {branch.address}\n"
            f"{T.BRANCH_PHONE}: {branch.phone or '-'}\n"
            f"{T.BRANCH_DISTANCE}: {distance:.2f} km"
        )
    )
