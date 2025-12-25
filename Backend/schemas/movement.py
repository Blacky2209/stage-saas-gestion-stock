from pydantic import BaseModel
from datetime import datetime

# 1. Socle commun
class MovementBase(BaseModel):
    product_id: int
    user_id: int
    tenant_id: int
    type_mouvement: str # "ENTREE" ou "SORTIE"
    quantite: int
    motif: str | None = "Achat fournisseur"

# 2. Création
class MovementCreate(MovementBase):
    pass

# 3. Lecture
class MovementResponse(MovementBase):
    id: int
    date_mouvement: datetime

    class Config:
        from_attributes = True