from pydantic import BaseModel

# 1. Socle commun
class ProductBase(BaseModel):
    nom: str
    description: str | None = None
    sku: str # La référence unique (ex: "IPHONE-15-NOIR")
    prix: float
    seuil_alerte: int = 10 # Par défaut, alerte si < 10
    tenant_id: int

# 2. Pour la création
class ProductCreate(ProductBase):
    pass

# 3. Pour la lecture
class ProductResponse(ProductBase):
    id: int
    quantite_stock: int # On affiche le stock, mais on ne le modifie pas ici !

    class Config:
        from_attributes = True