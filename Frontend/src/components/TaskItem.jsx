// Ce composant est "bête". Il reçoit des infos et des ordres via les Props.
function TaskItem({ task, onDelete, onToggle }) {
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      padding: '10px', 
      borderBottom: '1px solid #eee',
      background: task.done ? '#f0fff4' : 'white' // Vert clair si fini
    }}>
      <span 
        onClick={() => onToggle(task.id)} 
        style={{ 
          textDecoration: task.done ? 'line-through' : 'none', 
          cursor: 'pointer',
          flexGrow: 1
        }}
      >
        {task.done ? "✅" : "⬜"} {task.title}
      </span>
      
      <button 
        onClick={() => onDelete(task.id)}
        style={{ background: 'red', color: 'white', border: 'none', borderRadius: '4px' }}
      >
        X
      </button>
    </div>
  );
}

export default TaskItem;