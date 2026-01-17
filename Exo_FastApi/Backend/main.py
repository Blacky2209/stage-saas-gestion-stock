'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Autoriser ton frontend à parler au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/lancer")
def lancer_piece():
    # Choisi au hasard entre Pile et Face
    resultat = random.choice(["PILE", "FACE"])
    return {"resultat": resultat}

#  Le décorateur dit : "Si un utilisateur va sur '/bjr'..."
@app.get("/bjr") 
def dire_bonjour():
    # "...alors exécute cette fonction Python"
    return {"message": "Salut"}

@app.get("/calcul/{a}/{b}")
def calcul(a: int, b: int):
    # FastAPI a lu ": int". 
    # 1. Il extrait 'a' et 'b' de l'URL.
    # 2. Il VÉRIFIE que ce sont des nombres.
    # 3. Il les CONVERTIT automatiquement de texte vers entier.
    # 4. Si ce n'est pas un nombre, il renvoie une erreur AVANT même d'exécuter ta fonction.
    return {"resultat": a + b}

from pydantic import BaseModel

# 1. On définit le MOULE (le Schéma)
class Article(BaseModel):
    nom: str
    prix: float
    en_stock: bool = True  # Valeur par défaut

# 2. On utilise le moule dans la route
@app.post("/creer-article")
def creer(article: Article):
    # Ici, la variable 'article' est DÉJÀ validée.
    # On est sûr à 100% que article.prix est un nombre flottant.
    return {"nom": article.nom, "prix_ttc": article.prix * 1.20}
'''

'''from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text # Pour écrire du SQL brut
from database import get_db, engine # On importe ta config

# On initialise l'application
app = FastAPI()

# --- LA ROUTE DE TEST ---

@app.get("/")
def read_root():
    return {"message": "Ca tourne !"}

@app.get("/test-connexion")
def test_mysql_connection(db: Session = Depends(get_db)):
    try:
        # On demande à la base de faire un calcul simple (1 + 1)
        # C'est le "Ping" universel pour les bases de données
        db.execute(text("SELECT 1"))
        return {"status": "✅ SUCCÈS", "message": "Bravo ! FastAPI est bien connecté à ta base MySQL."}
    except Exception as e:
        return {"status": "❌ ERREUR", "detail": str(e)}'''
    

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 1. On importe la configuration BDD
from core.database import engine, Base
# 2. On importe tes modèles pour que la BDD sache quoi créer
from models import models
# 3. On importe ton fichier de routes (que tu viens de créer)
# (Assure-toi que ton fichier s'appelle bien users.py dans un dossier routers)
from routers import users 


# --- CRÉATION AUTOMATIQUE DES TABLES ---
# Cette ligne crée les tables dans MySQL si elles n'existent pas encore.
# C'est magique : ça regarde ton code Python et ça génère le SQL.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ACTIVATION DES ROUTES ---
# C'est ici qu'on "branche" ton fichier users.py sur l'application principale
app.include_router(users.router)

# Route de base juste pour vérifier que l'API tourne
@app.get("/")
def root():
    return {"message": "API Anniversaire en ligne !"}