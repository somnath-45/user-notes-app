from Model.Models import Note
from Schema.notesschema import CreateNotes, UpdateNotes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status


async def create_notes(
    notes: CreateNotes, user_id: int, session: AsyncSession
) -> Note:
    db_notes = Note(topic=notes.topic, text=notes.text, user_id=user_id)
    session.add(db_notes)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    await session.refresh(db_notes)
    return db_notes


async def get_notes_by_topic(topic: str, session: AsyncSession) -> List[Note]:
    statement = select(Note).where(Note.topic == topic)
    result = await session.execute(statement)
    notes = result.scalars().all()
    return notes


async def get_user_notes(user_id: int, session: AsyncSession) -> List[Note]:
    statement = select(Note).where(Note.user_id == user_id)
    result = await session.execute(statement)
    notes = result.scalars().all()
    return notes


async def delete_notes(user_id: int, note_id: int, session: AsyncSession) -> None:
    statement = select(Note).where(Note.id == note_id, Note.user_id == user_id)
    result = await session.execute(statement)
    result = result.scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notes not found"
        )
    await session.delete(result)
    await session.commit()
    return None


async def update_notes(
    note_id: int, notes: CreateNotes, session: AsyncSession
) -> Note:

    statement = select(Note).where(Note.id == note_id)
    result = await session.execute(statement)
    db_note = result.scalar_one_or_none()

    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    # update only provided fields
    if notes.topic is not None:
        db_note.topic = notes.topic
    if notes.text is not None:
        db_note.text = notes.text

    await session.commit()
    await session.refresh(db_note)

    return db_note
