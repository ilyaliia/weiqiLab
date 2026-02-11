from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from engine.board import Board
from models.game import Game
from schemas.game.game import GameCreateSchema, BotCreateSchema

router = APIRouter()


class GameCreateBotSchema:
    pass


@router.post(
    "/games",
    summary="Create game",
    description="Creates a new game",
    tags=["Game 🎮"]
)
async def create_bot_game(
        game_data: BotCreateSchema,
        current_user = Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    #ID пользователя создающего игру
    user_id = int(current_user.sub)

    game = Game(
        player1_id=user_id,
        player2_id=0,  # bot
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


@router.post(
    "/games/{game_id}/move",
    summary="Make a move",
    description="Place a stone on the board in the specified game",
    tags=["Game 🎮"]
)

#Необходимо передавать JWT токен для аутентификации

async def make_move(
        game_id: int,
        x: int = Body(...),
        y: int = Body(...),
        current_user = Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session),
):
    #ID пользователя делающего ход
    user_id = int(current_user.sub)

    result = await session.execute(
        select(Game).where(Game.id == game_id)
    )
    game = result.scalar_one_or_none()

    #Если игра не найдена, возвращаем 404
    if not game:
        raise HTTPException(404, detail="Game is not founded")

    if game.player1_id != user_id and game.player2_id != user_id:
        raise HTTPException(403, detail="You are not a player in this game")

    #Создаем доску из текущего состояния игры для проверки хода
    board = Board(grid=game.grid)

    try:

        new_grid, captured = board.make_move(x, y, color=game.current_player)
    except Exception as e:
        raise HTTPException(400, detail=f"Can`t move: {str(e)}")

    #Обновление поля после хода
    game.grid = new_grid

    #Переход хода следующему игроку
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


@router.get(
    "/games/{game_id}",
    summary="Get game state",
    description="Returns current board state and game information",
    tags=["Game 🎮"]
)
async def get_game_state():
    pass

#
# @router.post(
#     "/{game_id}/resign",
#     summary="Resign game",
#     description="Surrender the current game",
#     tags=["Game 🎮"]
# )
# async def resign_game(game_id: int):
#     pass
