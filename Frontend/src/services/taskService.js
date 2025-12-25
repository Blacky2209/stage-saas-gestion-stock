const API_URL = "http://127.0.0.1:8000";

export const getAllTasks = async () => {
  const res = await fetch(`${API_URL}/tasks`);
  return await res.json();
};

export const createTask = async (title) => {
  const res = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: title, done: false })
  });
  return await res.json();
};

export const deleteTask = async (id) => {
  await fetch(`${API_URL}/tasks/${id}`, { method: "DELETE" });
};

export const toggleTask = async (id) => {
  await fetch(`${API_URL}/tasks/${id}/toggle`, { method: "PUT" });
};