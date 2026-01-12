<script setup>
import { ref } from 'vue'

// PROPS : Ce sont les infos envoyées par le parent (App.vue)
// C'est l'équivalent de function StockForm({ product, type }) en React
const props = defineProps(['product', 'type'])

// EMITS : Pour parler au parent
const emit = defineEmits(['close', 'success'])

const quantite = ref(1)
const motif = ref("")

const handleSubmit = () => {
  const movement = {
    product_id: props.product.id,
    user_id: 1,    
    tenant_id: 1,  
    type_mouvement: props.type, // "ENTREE" ou "SORTIE"
    quantite: parseInt(quantite.value),
    motif: motif.value || (props.type === "ENTREE" ? "Réapprovisionnement" : "Vente client")
  }

  fetch("http://127.0.0.1:8000/movements/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(movement),
  })
  .then(res => {
    if (res.ok) {
      emit('success') // On dit au parent "C'est bon, recharge le tableau !"
      emit('close')   // On dit au parent "Ferme la fenêtre"
    } else {
      res.json().then(err => alert("Erreur : " + err.detail))
    }
  })
  .catch(err => console.error(err))
}
</script>

<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-xl w-96">
      
      <h2 :class="['text-xl font-bold mb-4', props.type === 'ENTREE' ? 'text-green-600' : 'text-red-600']">
        {{ props.type === 'ENTREE' ? '📥 Entrée de Stock' : '📤 Sortie de Stock' }}
      </h2>
      
      <p class="text-sm text-gray-500 mb-4">Produit : {{ props.product.nom }}</p>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Quantité</label>
          <input v-model="quantite" type="number" min="1" required class="w-full border p-2 rounded" />
        </div>

        <div>
          <label class="block text-sm font-medium">Motif</label>
          <input v-model="motif" type="text" placeholder="Ex: Vente, Livraison..." class="w-full border p-2 rounded" />
        </div>
        
        <div class="flex justify-end space-x-2 mt-4">
          <button type="button" @click="$emit('close')" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
            Annuler
          </button>
          
          <button type="submit" :class="['px-4 py-2 text-white rounded shadow', props.type === 'ENTREE' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700']">
            Valider
          </button>
        </div>
      </form>
    </div>
  </div>
</template>