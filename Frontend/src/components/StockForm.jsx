import { useState } from 'react';

export default function StockForm({ product, type, onClose, onSuccess }) {
  const [quantite, setQuantite] = useState(1);
  const [motif, setMotif] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const movement = {
      product_id: product.id,
      user_id: 1,    // On simule l'admin ID 1
      tenant_id: 1,  // On simule l'entreprise ID 1
      type_mouvement: type, // "ENTREE" ou "SORTIE"
      quantite: parseInt(quantite),
      motif: motif || (type === "ENTREE" ? "Réapprovisionnement" : "Vente client")
    };

    fetch("http://127.0.0.1:8000/movements/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(movement),
    })
      .then((res) => {
        if (res.ok) {
          onSuccess(); // Tout s'est bien passé
        } else {
          // Si le backend renvoie une erreur (ex: stock insuffisant)
          res.json().then(err => alert("Erreur : " + err.detail));
        }
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-96">
        <h2 className={`text-xl font-bold mb-4 ${type === 'ENTREE' ? 'text-green-600' : 'text-red-600'}`}>
          {type === 'ENTREE' ? '📥 Entrée de Stock' : '📤 Sortie de Stock'}
        </h2>
        <p className="text-sm text-gray-500 mb-4">Produit : {product.nom}</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Quantité</label>
            <input type="number" min="1" required className="w-full border p-2 rounded" 
              value={quantite} onChange={(e) => setQuantite(e.target.value)} />
          </div>

          <div>
            <label className="block text-sm font-medium">Motif</label>
            <input type="text" placeholder="Ex: Vente, Livraison..." className="w-full border p-2 rounded" 
              value={motif} onChange={(e) => setMotif(e.target.value)} />
          </div>
          
          <div className="flex justify-end space-x-2 mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Annuler</button>
            <button type="submit" className={`px-4 py-2 text-white rounded shadow ${type === 'ENTREE' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}>
              Valider
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}