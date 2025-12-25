import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import TodoPage from "./pages/TodoPage";

// Imaginons une deuxième page simple
const AdminPage = () => <h1>Page Admin (Secrète)</h1>;

function App() {
  return (
    <BrowserRouter>
      {/* La Navbar qui est visible sur toutes les pages */}
      <nav style={{ padding: "10px", background: "#eee", marginBottom: "20px" }}>
        {/* 1. On ajoute le lien ici */}
        <Link to="/todos" style={{ marginRight: "10px" }}>Mes Tâches</Link>
        <Link to="/admin">Admin</Link>
      </nav>

      {/* ⚠️ J'ai retiré <TodoPage /> d'ici pour qu'elle ne s'affiche pas tout le temps */}

      {/* Le système de changement de page */}
      <Routes>
        <Route path="/" element={<TodoPage />} />
        {/* 2. On définit la route ici : Si l'URL est /todos -> Affiche TodoPage */}
        <Route path="/todos" element={<TodoPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;