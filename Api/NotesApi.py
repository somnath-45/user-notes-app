from sqlalchemy.ext.asyncio import AsyncSession
from crud import CrudNotes
from fastapi import HTTPException, status, Depends, APIRouter
from Core.db import get_session
from Schema.notesschema import CreateNotes, PublicNotes
from typing import Annotated, List
from Model.Models import Note, User
from Core.auth import get_current_user


router = APIRouter()


@router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=PublicNotes)
async def create_notes(
    notes: CreateNotes,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Note:
    notes = await CrudNotes.create_notes(
        notes=notes, user_id=current_user.id, session=session
    )
    return notes


@router.get("/by_topic/{topics}", response_model=List[PublicNotes])
async def get_notes_by_topic(
    topics: str, session: Annotated[AsyncSession, Depends(get_session)]
) -> Note:
    topic = await CrudNotes.get_notes_by_topic(topic=topics, session=session)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        )
    return topic


@router.get("/user_notes/notes", response_model=List[PublicNotes])
async def get_user_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Note:
    user_notes = await CrudNotes.get_user_notes(
        user_id=current_user.id, session=session
    )
    if not user_notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No notes found"
        )
    return user_notes


@router.patch("/notes/{note_id}", response_model=PublicNotes)
async def update_notes(
    note_id: int,
    notes: CreateNotes,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Note:
    note = await CrudNotes.update_notes(note_id=note_id, notes=notes, session=session)
    return note


@router.delete("/notes/{noteid}", status_code=204)
async def delete_notes(
    noteid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    await CrudNotes.delete_notes(
        note_id=noteid, user_id=current_user.id, session=session
    )
    return {"message": "Deleted Succesfully"}
