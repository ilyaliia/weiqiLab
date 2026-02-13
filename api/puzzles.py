from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_session
from models.puzzles import Puzzles, DailyPuzzle
from schemas.puzzles.puzzles import PuzzleSchema

router = APIRouter()


@router.get("/puzzles", tags=["Puzzles 🧩"])
async def get_puzzles(
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        session: AsyncSession = Depends(get_session)
):
    query = select(Puzzles)

    if difficulty:
        query = query.where(Puzzles.difficulty == difficulty)
    if category:
        query = query.where(Puzzles.category == category)

    result = await session.execute(
        query.offset(offset).limit(limit)
    )
    return result.scalars().all()


@router.post("/puzzles", tags=["Puzzles 🧩"])
async def create_puzzle(
    puzzle_data: PuzzleSchema,
    session: AsyncSession = Depends(get_session)
):
    new_puzzle = Puzzles(**puzzle_data.model_dump())
    session.add(new_puzzle)
    await session.commit()
    await session.refresh(new_puzzle)
    return {"id": new_puzzle.id, "message": "Puzzle created"}


@router.get("/puzzles/random", tags=["Puzzles 🧩"])
async def get_random_puzzle(
        difficulty: Optional[str] = None,
        session: AsyncSession = Depends(get_session)
):
    query = select(Puzzles)

    if difficulty:
        query = query.where(Puzzles.difficulty == difficulty)

    result = await session.execute(
        query.order_by(func.random()).limit(1)
    )

    puzzle = result.scalar_one_or_none()

    if not puzzle:
        return {"error": "No puzzles found"}

    return puzzle   # random puzzle


@router.get("/puzzles/daily", tags=["Puzzles 🧩"])
async def get_daily_puzzle(
    session: AsyncSession = Depends(get_session)
):
    today = date.today()

    result = await session.execute(
        select(DailyPuzzle)
        .options(selectinload(DailyPuzzle.puzzle))
        .where(DailyPuzzle.date == today)
    )
    daily = result.scalar_one_or_none()

    if not daily:
        return {"error": "No daily puzzle for today"}

    return daily.puzzle


@router.post("/puzzles/daily", tags=["Puzzles 🧩"])
async def set_daily_puzzle(
        puzzle_id: int,
        session: AsyncSession = Depends(get_session)
):
    from datetime import date

    puzzle = await session.get(Puzzles, puzzle_id)
    if not puzzle:
        return {"error": "Puzzle not found"}

    today = date.today()

    await session.execute(
        delete(DailyPuzzle).where(DailyPuzzle.date == today)
    )

    daily = DailyPuzzle(
        date=today,
        puzzle_id=puzzle_id
    )
    session.add(daily)
    await session.commit()

    return {"message": "Daily puzzle set", "puzzle_id": puzzle_id}


@router.get("/puzzles/{puzzle_id}", tags=["Puzzles 🧩"])
async def get_puzzle_by_id(
        puzzle_id: int,
        session: AsyncSession = Depends(get_session)
):
    puzzle = await session.get(Puzzles, puzzle_id)
    if not puzzle:
        return {"message": "Not found"}
    return puzzle


@router.delete("/puzzles/{puzzle_id}", tags=["Puzzles 🧩"])
async def delete_puzzle(
        puzzle_id: int,
        session: AsyncSession = Depends(get_session)
):
    puzzle = await session.get(Puzzles, puzzle_id)
    if not puzzle:
        return {"message": "Not found"}

    await session.delete(puzzle)
    await session.commit()
    return {"message": f"Successfully deleted puzzle {puzzle_id}"}
