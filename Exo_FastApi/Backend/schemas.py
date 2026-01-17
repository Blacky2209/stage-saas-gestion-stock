from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    firstname: str
    birthday: Optional[date]
    date_creation: datetime
    date_modif: datetime

    class Config:
        from_attributes = True



# NOUVEAU : Ce qu'on attend du Frontend pour créer un user
class UserCreate(BaseModel):
    name: str
    firstname: str
    birthday: date
    
# schemas.py
# ... tes autres classes ...

# Ajoute ça :
class UserUpdate(BaseModel):
    name: str
    firstname: str
    birthday: date

# ... tes autres schemas (UserCreate, UserUpdate, UserSchema) restent pareils ...

# 1. Le moule pour un Événement seul
class EventSchema(BaseModel):
    event: str      # <--- CORRECTION : Doit avoir le même nom que la colonne SQL
    city: Optional[str] = None # <--- CORRECTION : nullable=True dans ton model, donc Optional ici
    postcode: int
    date: date

    class Config:
        from_attributes = True

# 2. Le moule COMBINÉ (User + Event)
class UserWithEvent(UserSchema):
    # On reprend tout de UserSchema
    # Et on ajoute l'objet EventSchema qu'on a défini juste au-dessus
    event: Optional[EventSchema] = None