from pydantic import BaseModel
from datetime import datetime

# 1. Le socle commun
class TenantBase(BaseModel):
    nom_societe: str
    adresse: str | None = None

# 2. Pour la création (ce qu'on envoie)
class TenantCreate(TenantBase):
    pass

# 3. Pour la lecture (ce qu'on reçoit)
class TenantResponse(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True