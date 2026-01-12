<script setup>
import { ref } from 'vue'

// On définit les événements que ce composant peut envoyer au parent (App.vue)
const emit = defineEmits(['close', 'refresh'])

// Les variables du formulaire
const nom = ref("")
const sku = ref("")
const prix = ref("")
const description = ref("")

const handleSubmit = () => {
  // 1. Préparation des données
  const newProduct = {
    nom: nom.value,
    sku: sku.value,
    prix: parseFloat(prix.value),
    description: description.value,
    seuil_alerte: 5,
    tenant_id: 1
  }

  // 2. Envoi au Backend
  fetch("http://127.0.0.1:8000/products/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newProduct),
  })
  .then(res => {
    if (res.ok) {
      // Si ça marche, on prévient le parent pour qu'il recharge la liste
      emit('refresh')
      emit('close')
    } else {
      alert("Erreur ! Vérifie le SKU (doublon ?)")
    }
  })
  .catch(err => console.error(err))
}
</script>

<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl w-96">
      <h2 class="text-xl font-bold mb-4">Ajouter un produit (Vue)</h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        
        <input v-model="nom" type="text" placeholder="Nom" required class="w-full border p-2 rounded" />
        <input v-model="sku" type="text" placeholder="SKU (Réf unique)" required class="w-full border p-2 rounded" />
        <input v-model="prix" type="number" placeholder="Prix (€)" required class="w-full border p-2 rounded" />
        <textarea v-model="description" placeholder="Description" class="w-full border p-2 rounded"></textarea>
        
        <div class="flex justify-end space-x-2 mt-4">
          <button type="button" @click="$emit('close')" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
            Annuler
          </button>
          <button type="submit" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
            Créer
          </button>
        </div>

      </form>
    </div>
  </div>
</template>