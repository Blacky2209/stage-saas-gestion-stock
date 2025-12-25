import { useEffect, useState } from "react";
// Imports propres grâce à notre structure
import { getAllTasks, createTask, deleteTask, toggleTask } from "../services/taskService";
import TaskItem from "../components/TaskItem";

function TodoPage() {
  const [tasks, setTasks] = useState([]);
  const [inputVal, setInputVal] = useState("");

  // 1. Charger les tâches au démarrage
  const refreshTasks = async () => {
    const data = await getAllTasks();
    setTasks(data);
  };

  useEffect(() => {
    refreshTasks();
  }, []);

  // 2. Gestionnaires d'événements (Handlers)
  const handleAdd = async () => {
    if (!inputVal) return;
    await createTask(inputVal);
    setInputVal(""); // Vider le champ
    refreshTasks();  // Recharger la liste
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    refreshTasks();
  };

  const handleToggle = async (id) => {
    await toggleTask(id);
    refreshTasks();
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', fontFamily: 'Arial' }}>
      <h1>📝 TaskMaster</h1>
      
      {/* Zone d'ajout */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input 
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Nouvelle tâche..."
          style={{ flexGrow: 1, padding: '8px' }}
        />
        <button onClick={handleAdd}>Ajouter</button>
      </div>

      {/* Liste des tâches */}
      <div style={{ border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden' }}>
        {tasks.map((t) => (
          <TaskItem 
            key={t.id} 
            task={t} 
            onDelete={handleDelete} 
            onToggle={handleToggle} 
          />
        ))}
        {tasks.length === 0 && <p style={{textAlign: 'center'}}>Aucune tâche !</p>}
      </div>
    </div>
  );
}

export default TodoPage;