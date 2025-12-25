from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# --- Modèle de données (Pydantic) ---
class Task(BaseModel):
    id: int = None  # Optionnel à la création
    title: str
    done: bool = False

# --- Fausse Base de Données ---
fake_tasks_db = [
    {"id": 1, "title": "Apprendre FastAPI", "done": True},
    {"id": 2, "title": "Comprendre React", "done": False}
]

# --- Les Routes ---

# 1. Lire tout (GET)
@router.get("/tasks", response_model=List[Task])
def get_tasks():
    return fake_tasks_db

# 2. Ajouter (POST)
@router.post("/tasks")
def add_task(task: Task):
    # On génère un faux ID (en vrai, SQL le fait tout seul)
    new_id = len(fake_tasks_db) + 1
    task.id = new_id
    fake_tasks_db.append(task.dict())
    return task

# 3. Supprimer (DELETE)
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global fake_tasks_db
    # On garde tout SAUF celui qui a l'ID donné
    fake_tasks_db = [t for t in fake_tasks_db if t["id"] != task_id]
    return {"message": "Supprimé"}

# 4. Mettre à jour (PUT - Pour cocher/décocher)
@router.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    for t in fake_tasks_db:
        if t["id"] == task_id:
            t["done"] = not t["done"] # On inverse (True devient False et inversement)
            return t
    raise HTTPException(status_code=404, detail="Tâche introuvable")