from fastapi import APIRouter
from pydantic import BaseModel

# C'est comme une "mini application" FastAPI qu'on branchera sur la principale
router = APIRouter() 

# Le Schéma
class User(BaseModel):
    username: str
    email: str

# Simulation de base de données
fake_users_db = []

# --- LES ROUTES ---

@router.get("/users")
def get_all_users():
    return fake_users_db

@router.post("/users", status_code=201)
def create_user(user: User):
    fake_users_db.append(user)
    return {"msg": f"Utilisateur {user.username} ajouté !"}