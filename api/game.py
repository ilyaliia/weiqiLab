from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
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


@router.post("/move")
async def make_move(
        game_id: int = Body(...),
        x: int = Body(...),
        y: int = Body(...),
        session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Game).where(Game.id == game_id)
    )
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(404, detail="Игра не найдена")

    user_color = 1 if game.user_is_black else 2  # 1=black, 2=white

    if game.current_player != user_color:
        raise HTTPException(400, detail="Сейчас не ваш ход")

    board = Board(grid=game.grid)

    try:
        new_grid, captured = board.make_move(x, y, color=user_color)
    except Exception as e:
        raise HTTPException(400, detail=f"Недопустимый ход: {str(e)}")

    game.grid = new_grid
    game.current_player = 2 if game.current_player == 1 else 1

    if captured:
        if user_color == 1:
            game.white_captured += len(captured)
        else:
            game.black_captured += len(captured)

    await session.commit()

    return {
        "success": True,
        "message": "Ход принят",
        "new_grid": new_grid,
        "captured_stones": captured,
        "current_player": game.current_player,
        "black_captured": game.black_captured,
        "white_captured": game.white_captured
    }


@router.get("/{game_id}")
async def get_game_state():
    pass


@router.post("/{game_id}/resign")
async def resign_game(game_id: int):
    pass
