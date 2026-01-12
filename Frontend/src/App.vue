<script setup>
import { ref, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import ProductForm from './components/ProductForm.vue'
import StockForm from './components/StockForm.vue' // <--- NOUVEAU

const products = ref([])
const showProductForm = ref(false)

// Variables pour gérer le mouvement de stock
const selectedProduct = ref(null) // Quel produit on modifie ?
const movementType = ref(null)    // ENTREE ou SORTIE ?

const fetchProducts = () => {
  fetch("http://127.0.0.1:8000/products/")
    .then(res => res.json())
    .then(data => products.value = data)
    .catch(err => console.error("Erreur:", err))
}

// Fonction utilitaire pour ouvrir le formulaire de stock
const openStockForm = (product, type) => {
  selectedProduct.value = product
  movementType.value = type
}

// Fonction pour fermer le formulaire de stock
const closeStockForm = () => {
  selectedProduct.value = null
  movementType.value = null
}

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <main class="max-w-7xl mx-auto py-10 px-4">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Mon Stock (Vue.js)</h1>
        <button @click="showProductForm = true" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition shadow">
          + Nouveau Produit
        </button>
      </div>

      <ProductForm 
        v-if="showProductForm" 
        @close="showProductForm = false" 
        @refresh="fetchProducts" 
      />

      <StockForm 
        v-if="selectedProduct"
        :product="selectedProduct"
        :type="movementType"
        @close="closeStockForm"
        @success="closeStockForm(); fetchProducts()"
      />

      <div class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU / Nom</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prix</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actuel</th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="product in products" :key="product.id" class="hover:bg-gray-50">
              
              <td class="px-6 py-4">
                <div class="font-bold text-gray-900">{{ product.nom }}</div>
                <div class="text-xs text-gray-500">REF: {{ product.sku }}</div>
              </td>
              
              <td class="px-6 py-4 text-sm text-gray-900">{{ product.prix }} €</td>
              
              <td class="px-6 py-4">
                <span :class="[
                  'px-2 py-1 text-xs font-bold rounded-full',
                  product.quantite_stock < 5 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                ]">
                  {{ product.quantite_stock }} unités
                </span>
              </td>

              <td class="px-6 py-4 text-center space-x-2">
                <button 
                  @click="openStockForm(product, 'ENTREE')"
                  class="bg-green-100 text-green-700 hover:bg-green-200 px-3 py-1 rounded border border-green-300 transition"
                  title="Entrée de stock"
                >
                  + Entrée
                </button>
                <button 
                  @click="openStockForm(product, 'SORTIE')"
                  class="bg-red-100 text-red-700 hover:bg-red-200 px-3 py-1 rounded border border-red-300 transition"
                  title="Sortie de stock"
                >
                  - Sortie
                </button>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>