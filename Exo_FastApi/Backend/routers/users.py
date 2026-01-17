from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import extract

from core.database import get_db
from models.models import User, Event
from schemas import UserSchema, UserCreate, UserUpdate, UserWithEvent

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs (Users)"]
)

# 1. LISTE DES USERS
@router.get("/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 2. CRÉER UN USER
@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        firstname=user.firstname,
        birthday=user.birthday
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 3. SUPPRIMER UN USER
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.delete(db_user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}

# 4. MODIFIER UN USER
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db_user.name = user_update.name
    db_user.firstname = user_update.firstname
    db_user.birthday = user_update.birthday
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 5. LIRE UN SEUL USER (AVEC L'ÉVÉNEMENT)
@router.get("/{user_id}", response_model=UserWithEvent)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # A. On cherche le user
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # --- MOUCHARD 1 ---
    print(f"🔍 J'analyse l'utilisateur : {db_user.firstname} (Né le {db_user.birthday})")

    # B. On cherche l'événement
    # Rappel : Même Jour, Même Mois, Année > Année de naissance
    db_event = db.query(Event).filter(
        extract('month', Event.date) == extract('month', db_user.birthday),
        extract('day', Event.date) == extract('day', db_user.birthday),
        extract('year', Event.date) > extract('year', db_user.birthday)
    ).order_by(Event.date).first()

    # C. On attache l'event au user
    db_user.event = db_event
    
    return db_user