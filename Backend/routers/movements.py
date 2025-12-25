from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import Movement, Product # On a besoin des deux !
from schemas.movement import MovementCreate, MovementResponse

router = APIRouter(
    prefix="/movements",
    tags=["Mouvements de Stock"]
)

# 2. Lire l'historique des mouvements (GET)
@router.get("/", response_model=list[MovementResponse])
def read_movements(db: Session = Depends(get_db)):
    return db.query(Movement).all()

@router.post("/", response_model=MovementResponse)
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)):
    # 1. On récupère le produit concerné
    product = db.query(Product).filter(Product.id == movement.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # 2. LOGIQUE MÉTIER : On met à jour la quantité du produit
    if movement.type_mouvement == "ENTREE":
        product.quantite_stock += movement.quantite
    
    elif movement.type_mouvement == "SORTIE":
        # Vérification anti-négatif !
        if product.quantite_stock < movement.quantite:
            raise HTTPException(status_code=400, detail="Stock insuffisant pour cette sortie !")
        product.quantite_stock -= movement.quantite
    
    else:
        raise HTTPException(status_code=400, detail="Type invalide. Utiliser 'ENTREE' ou 'SORTIE'")

    # 3. On enregistre le mouvement dans l'historique
    new_movement = Movement(
        tenant_id=movement.tenant_id,
        product_id=movement.product_id,
        user_id=movement.user_id,
        type_mouvement=movement.type_mouvement,
        quantite=movement.quantite,
        motif=movement.motif
    )

    db.add(new_movement)
    db.commit() # Sauvegarde TOUT (le mouvement + la mise à jour du produit)
    db.refresh(new_movement)
    
    return new_movement