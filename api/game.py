from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.dependencies import get_current_user
from database import get_session
from engine.board import Board
from models.game import Game
from models.users import User
from schemas.game.game import GameCreateSchema, BotCreateSchema

router = APIRouter()


class GameCreateBotSchema:
    pass


@router.post("/vs-bot")
async def create_bot_game(
        game_data: BotCreateSchema,
        session: AsyncSession = Depends(get_session)
):
    game = Game(
        board_size=game_data.board_size,
        bot_rating=game_data.bot_rating,
        handicap=game_data.handicap,
        komi=game_data.komi,
        status="active"
    )

    # db save
    session.add(game)
    await session.commit()
    await session.refresh(game)

    return {
        "game_id": game.id,
        "board_size": game.board_size,
        "bot_rating": game.bot_rating,
        "status": game.status,
        "created_at": game.created_at.isoformat()
    }


@router.post("/{game_id}/move")
async def make_move(
        board: Board,
        game_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    # game = await session.get(Game, game_id)
    pass


@router.get("/{game_id}")
async def get_game_state():
    pass


@router.post("/{game_id}/resign")
async def resign_game(game_id: int):
    pass
