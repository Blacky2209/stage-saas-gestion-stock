from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

'''app = FastAPI()

# --- 1. Autoriser React à nous parler (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" veut dire : tout le monde peut m'appeler
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Notre stock de données ---
stock_fruits = [
    {"nom": "Pomme Rouge", "prix": 2.50},
    {"nom": "Banane Bio", "prix": 1.99},
    {"nom": "Mangue", "prix": 4.00},
    {"nom": "Fraise", "prix": 3.20}
]

# --- 3. La Route (Le guichet) ---
@app.get("/fruit-au-hasard")
def donner_fruit():
    # On choisit un fruit au hasard dans la liste
    fruit_choisi = random.choice(stock_fruits)
    return fruit_choisi'''


'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # <--- INDISPENSABLE pour recevoir des données

app = FastAPI()

# 1. Configurer les permissions (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Le "Moule" (Modèle de données)
# On dit à Python : "Je n'accepte que des objets qui ont un 'nom' (texte) et un 'prix' (nombre)"
class NouvelleCommande(BaseModel):
    nom: str
    prix: float

# 3. La Route POST (Réception)
@app.post("/commander")
async def recevoir_commande(commande: NouvelleCommande):
    # Ici, tu ferais normalement l'enregistrement en base de données SQL.
    # Pour l'instant, on renvoie juste une confirmation.
    print(f"J'ai reçu une commande pour : {commande.nom}")
    return {"message": f"Commande reçue pour {commande.nom} qui coûte {commande.prix}€ !"}
'''

'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from routers import users # 1. On importe le fichier qu'on vient de créer

app = FastAPI()

# 2. On "branche" le routeur
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Le serveur tourne, va voir /users !"}

app = FastAPI()

# --- CORS (Toujours nécessaire) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. NOTRE BASE DE DONNÉES (Simulation) ---
# Chaque question a un ID, un texte, des options, et la bonne réponse (cachée)
db_quiz = [
    {
        "id": 1,
        "question": "Quel framework utilisons-nous pour le Frontend ?",
        "options": ["Vue.js", "React.js", "Angular"],
        "bonne_reponse": "React.js"
    },
    {
        "id": 2,
        "question": "Quel langage est utilisé par FastAPI ?",
        "options": ["Java", "Python", "C++"],
        "bonne_reponse": "Python"
    },
    {
        "id": 3,
        "question": "Que signifie SQL ?",
        "options": ["Structured Query Language", "Strong Question List", "Super Quick Load"],
        "bonne_reponse": "Structured Query Language"
    }
]

# --- 2. MODÈLES DE DONNÉES ---
# Ce que le frontend doit envoyer pour se faire corriger
class ReponseUtilisateur(BaseModel):
    question_id: int
    reponse_choisie: str

# --- 3. ROUTES ---

@app.get("/quiz")
def get_quiz():
    # On renvoie les questions MAIS on retire la "bonne_reponse" pour pas tricher !
    quiz_public = []
    for q in db_quiz:
        quiz_public.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })
    return quiz_public

@app.post("/verifier")
def verifier_reponse(reponse: ReponseUtilisateur):
    # On cherche la question correspondante dans notre "base de données"
    for q in db_quiz:
        if q["id"] == reponse.question_id:
            # On compare
            est_correct = (q["bonne_reponse"] == reponse.reponse_choisie)
            return {
                "correct": est_correct, 
                "message": "Bravo !" if est_correct else f"Dommage ! La bonne réponse était {q['bonne_reponse']}"
            }
    
    return {"error": "Question introuvable"}'''


'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse  # <--- 1. On importe l'outil de redirection
from routers import tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LA SOLUTION MAGIQUE ---
@app.get("/")
def redirect_to_docs():
    # 2. Dès qu'on arrive sur la racine "/", on est redirigé vers "/docs"
    return RedirectResponse(url="/docs")
# ---------------------------

app.include_router(tasks.router)'''


'''from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine
from sqlalchemy import text # Pour tester une requête SQL brute

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API TaskMaster en ligne !"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # On essaie de faire une requête simple "SELECT 1"
        db.execute(text("SELECT 1"))
        return {"status": "Succès", "message": "Connexion BDD réussie ! 🟢"}
    except Exception as e:
        return {"status": "Erreur", "message": f"Échec connexion : {str(e)} 🔴"}'''

'''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Le Backend du SaaS GOMAHTECH est en ligne ! 🚀"}'''



'''from fastapi import FastAPI
from core.database import engine
import models # On importe les modèles pour que la BDD les reconnaisse
from routers import tenants # On importe ton nouveau router

# 1. Cette ligne magique crée automatiquement les tables dans PostgreSQL
# si elles n'existent pas encore (basé sur tes fichiers models.py)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GOMAHTECH Stock SaaS")

# 2. On connecte le router des Tenants à l'application principale
app.include_router(tenants.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API SaaS Stock ! 🚀"}'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from models import models
from routers import tenants, users, products, movements # <--- 1. AJOUTE movements

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GOMAHTECH Stock SaaS")

# ... (CORS ne change pas) ...

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # <--- L'étoile magique : Tout le monde peut entrer !
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(movements.router) # <--- 2. AJOUTE LA ROUTE

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API SaaS Stock ! 🚀"}

@app.get("/anniv")
def anniversaire():
    return {"List_anniv": {"Fatou": "1990-01-01", "Lamine": "1992-02-02"}}

@app.get("/anniv/Fatou")
def anniversaire_fatou():
    return {"message": "Joyeux anniversaire Fatou ! 🎉🎂"}