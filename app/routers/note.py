from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get("/", response_model=List[schemas.NoteRes])
def get_notes(db: Session = Depends(get_db), current_user: models.User = Depends(
            oauth2.get_current_user)):

    notes = db.query(models.Note).filter(models.Note.owner==current_user.id).all()
    return notes

@router.get("/{note_id}", response_model=schemas.NoteRes)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(
            oauth2.get_current_user)):
    note = db.query(models.Note).filter(models.Note.owner == current_user.id).filter(
        models.Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró \
la nota ingresada entre las notas pertenecientes al usuario con el que se hizo la \
petición")

    return note

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteRes)
def create_note(note: schemas.Note, db: Session = Depends(get_db), current_user: models.User =
            Depends(oauth2.get_current_user)):
    new_note = models.Note(**note.dict(), owner=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.put("/{note_id}", response_model=schemas.NoteRes)
def update_note(note_id: int, note:schemas.Note, db: Session = Depends(get_db), current_user: 
                models.User = Depends(oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.owner == current_user.id).filter(
        models.Note.id == note_id)

    if note_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró \
la nota ingresada entre las notas pertenecientes al usuario con el que se hizo la \
petición")

    note_query.update(note.dict(), synchronize_session=False)
    db.commit()

    return note_query.first()

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(
                oauth2.get_current_user)):
    note_query = db.query(models.Note).filter(models.Note.owner == current_user.id).filter(
        models.Note.id == note_id)

    if note_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La nota con el id '{note_id}' no se encontró entre las notas pertenecientes al \
usuario con el que se hizo la petición")

    note_query.delete(synchronize_session=False)
    db.commit()

    return
