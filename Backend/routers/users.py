from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User
from schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs (Users)"]
)

# 1. Créer un Utilisateur
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")

    # Création du nouvel utilisateur
    # ⚠️ NOTE : Pour l'instant le mot de passe est en clair. 
    # On ajoutera le cryptage (hachage) plus tard pour la sécurité.
    new_user = User(
        nom=user.nom,
        email=user.email,
        mot_de_passe=user.mot_de_passe,
        role=user.role,
        tenant_id=user.tenant_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. Lire tous les utilisateurs
@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()