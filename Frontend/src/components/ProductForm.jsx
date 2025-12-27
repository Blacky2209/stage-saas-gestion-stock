import { useState } from 'react';

export default function ProductForm({ onProductAdded, onCancel }) {
  // On crée des variables pour stocker ce que l'utilisateur tape
  const [nom, setNom] = useState("");
  const [sku, setSku] = useState("");
  const [prix, setPrix] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Empêche la page de se recharger

    // 1. On prépare les données à envoyer
    const newProduct = {
      nom: nom,
      sku: sku,
      prix: parseFloat(prix), // On s'assure que c'est un nombre
      description: description,
      seuil_alerte: 5,
      tenant_id: 1 // On force l'entreprise 1 pour l'instant
    };

    // 2. On envoie au Backend via l'API
    fetch("http://127.0.0.1:8000/products/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newProduct),
    })
      .then((res) => {
        if (res.ok) {
          // Si ça marche, on prévient App.jsx pour qu'il rafraîchisse la liste
          onProductAdded();
        } else {
          alert("Erreur lors de la création ! Vérifie le SKU (doublon ?)");
        }
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-xl w-96">
        <h2 className="text-xl font-bold mb-4">Ajouter un produit</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nom</label>
            <input type="text" required className="mt-1 block w-full border rounded-md p-2" 
              value={nom} onChange={(e) => setNom(e.target.value)} />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">SKU (Réf unique)</label>
            <input type="text" required className="mt-1 block w-full border rounded-md p-2" 
              value={sku} onChange={(e) => setSku(e.target.value)} />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Prix (€)</label>
            <input type="number" required className="mt-1 block w-full border rounded-md p-2" 
              value={prix} onChange={(e) => setPrix(e.target.value)} />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea className="mt-1 block w-full border rounded-md p-2" 
              value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>

          <div className="flex justify-end space-x-2 mt-4">
            <button type="button" onClick={onCancel} className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
              Annuler
            </button>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Créer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}