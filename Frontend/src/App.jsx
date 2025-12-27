import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import ProductForm from './components/ProductForm';
import StockForm from './components/StockForm'; // <--- NOUVEAU

function App() {
  const [products, setProducts] = useState([]);
  const [showProductForm, setShowProductForm] = useState(false);
  
  // États pour gérer le mouvement de stock
  const [selectedProduct, setSelectedProduct] = useState(null); // Quel produit on modifie ?
  const [movementType, setMovementType] = useState(null);       // ENTREE ou SORTIE ?

  const fetchProducts = () => {
    fetch("http://127.0.0.1:8000/products/")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Erreur:", err));
  };

  useEffect(() => { fetchProducts(); }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="max-w-7xl mx-auto py-10 px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Mon Stock</h1>
          <button onClick={() => setShowProductForm(true)} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition shadow">
            + Nouveau Produit
          </button>
        </div>

        {/* Formulaire Création Produit */}
        {showProductForm && (
          <ProductForm 
            onCancel={() => setShowProductForm(false)} 
            onProductAdded={() => { setShowProductForm(false); fetchProducts(); }} 
          />
        )}

        {/* Formulaire Mouvement de Stock (S'affiche si un produit est sélectionné) */}
        {selectedProduct && (
          <StockForm 
            product={selectedProduct}
            type={movementType}
            onClose={() => setSelectedProduct(null)}
            onSuccess={() => { setSelectedProduct(null); fetchProducts(); }}
          />
        )}

        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU / Nom</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prix</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actuel</th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {products.map((product) => (
                <tr key={product.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="font-bold text-gray-900">{product.nom}</div>
                    <div className="text-xs text-gray-500">REF: {product.sku}</div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{product.prix} €</td>
                  
                  {/* Colonne Stock avec couleur dynamique */}
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs font-bold rounded-full ${product.quantite_stock < product.seuil_alerte ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {product.quantite_stock} unités
                    </span>
                  </td>

                  {/* Colonne Actions (+ et -) */}
                  <td className="px-6 py-4 text-center space-x-2">
                    <button 
                      onClick={() => { setSelectedProduct(product); setMovementType("ENTREE"); }}
                      className="bg-green-100 text-green-700 hover:bg-green-200 px-3 py-1 rounded border border-green-300 transition"
                      title="Entrée de stock"
                    >
                      + Entrée
                    </button>
                    <button 
                      onClick={() => { setSelectedProduct(product); setMovementType("SORTIE"); }}
                      className="bg-red-100 text-red-700 hover:bg-red-200 px-3 py-1 rounded border border-red-300 transition"
                      title="Sortie de stock"
                    >
                      - Sortie
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default App;