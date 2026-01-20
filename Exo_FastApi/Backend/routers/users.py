from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import extract

from core.database import get_db
from models.models import User, Event
# IMPORTANT : On importe bien UserWithEvent ici
from schemas import UserSchema, UserCreate, UserUpdate, UserWithEvent

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs (Users)"]
)

# 1. LISTE DES USERS (Calcul pour tout le monde)
# C'est cette route qui permet à ton filtre "Event" de marcher
@router.get("/", response_model=List[UserWithEvent])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    # On attache l'événement à chaque utilisateur de la liste
    for user in users:
        event = db.query(Event).filter(
            extract('month', Event.date) == extract('month', user.birthday),
            extract('day', Event.date) == extract('day', user.birthday),
            extract('year', Event.date) > extract('year', user.birthday)
        ).order_by(Event.date).first()
        
        user.event = event

    return users

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

# 5. LIRE UN SEUL USER (Détails)
@router.get("/{user_id}", response_model=UserWithEvent)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Recherche de l'événement (Logique identique à la liste)
    db_event = db.query(Event).filter(
        extract('month', Event.date) == extract('month', db_user.birthday),
        extract('day', Event.date) == extract('day', db_user.birthday),
        extract('year', Event.date) > extract('year', db_user.birthday)
    ).order_by(Event.date).first()

    # Mouchard pour le debug (Optionnel)
    if db_event:
        # Attention : ici on utilise .event car c'est le nom de ta colonne SQL
        print(f"✅ Event trouvé pour {db_user.firstname}: {db_event.event}")
    
    db_user.event = db_event
    return db_user