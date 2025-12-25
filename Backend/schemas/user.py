from pydantic import BaseModel

# 1. Socle commun
class UserBase(BaseModel):
    nom: str
    email: str
    role: str = "employe" # Par défaut, c'est un employé
    tenant_id: int # TRES IMPORTANT : Il faut dire à quelle entreprise il appartient !

# 2. Pour la création (Avec mot de passe)
class UserCreate(UserBase):
    mot_de_passe: str

# 3. Pour la lecture (On cache le mot de passe !)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True