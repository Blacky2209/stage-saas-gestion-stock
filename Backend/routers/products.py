from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import Product # Import correct
from schemas.product import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Produits"]
)

# 1. Créer un Produit
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Vérifier si le SKU existe déjà (Doublon interdit)
    db_product = db.query(Product).filter(Product.sku == product.sku).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Ce code SKU existe déjà.")

    new_product = Product(
        nom=product.nom,
        description=product.description,
        sku=product.sku,
        prix=product.prix,
        seuil_alerte=product.seuil_alerte,
        tenant_id=product.tenant_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# 2. Lire tous les produits
@router.get("/", response_model=list[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()