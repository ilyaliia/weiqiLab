from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security
from database import get_session
from engine.board import Board
from models.game import Game
from models.users import User
from schemas.game.game import BotCreateSchema

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
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    # who create user_id
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
async def make_move(
        game_id: int,
        x: int = Body(...),
        y: int = Body(...),
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session),
):
    user_id = int(current_user.sub)

    result = await session.execute(
        select(Game).where(Game.id == game_id)
    )
    game = result.scalar_one_or_none()

    if not game:
        raise HTTPException(404, detail="Game not found")

    if game.player1_id != user_id and game.player2_id != user_id:
        raise HTTPException(403, detail="You are not a player in this game")

    user_color = 1 if user_id == game.player1_id else 2

    if user_color != game.current_player:
        raise HTTPException(400, detail="Not your turn")

    board = Board(grid=game.grid)

    board.current_player = game.current_player  # switch color (before move)

    # make move
    result = board.make_move(x, y, game.current_player)

    if result is False:
        raise HTTPException(400, detail="Illegal move")

    new_grid, captured = result

    game.grid = new_grid

    if captured:
        if user_color == 1:  # black
            game.black_captured += len(captured)
        else:  # white
            game.white_captured += len(captured)

    game.current_player = 2 if game.current_player == 1 else 1  # Switch color (after)

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
@router.post(
    "/{game_id}/resign",
    summary="Resign game",
    description="Surrender the current game",
    tags=["Game 🎮"]
)
async def resign_game(game_id: int):
    pass


match_queue = []  # queue for find match
@router.post("/match")
async def find_match(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    """Найти соперника"""
    user_id = int(current_user.sub)

    # add in queue
    if user_id not in match_queue:
        match_queue.append(user_id)

    if len(match_queue) >= 2:
        p1_id = match_queue.pop(0)  # black
        p2_id = match_queue.pop(0)  # white

        # get user objects from db
        p1_result = await session.execute(
            select(User).where(User.id == p1_id)
        )
        p2_result = await session.execute(
            select(User).where(User.id == p2_id)
        )
        p1 = p1_result.scalar_one_or_none()
        p2 = p2_result.scalar_one_or_none()

        # create game
        game = Game(
            player1_id=p1_id,  # black
            player2_id=p2_id,  # white
            board_size=19,
            handicap=0,
            komi=6.5,
            current_player=1,
            status="active",
            grid=[[0] * 19 for _ in range(19)],
            black_captured=0,
            white_captured=0
        )
        session.add(game)
        await session.commit()
        await session.refresh(game)

        # for response
        your_color = 1 if user_id == p1_id else 2
        opponent = p2 if your_color == 1 else p1

        return {
            "status": "game_created",
            "game_id": game.id,
            "your_color": your_color,
            "opponent": {
                "id": opponent.id,
                "username": opponent.username
            }
        }

    position = match_queue.index(user_id) + 1

    return {
        "status": "waiting",
        "position": position,
        "queue_size": len(match_queue)
    }


@router.get("/games/{game-id}")
async def get_game_by_id(game_id: str, session: AsyncSession = Depends(get_session)):
    game = await session.get(Game, game_id)
    return game.grid
