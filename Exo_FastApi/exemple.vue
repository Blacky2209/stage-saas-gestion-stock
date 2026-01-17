:<script setup>
import { ref } from 'vue'

// 1. Les Variables (Données)
const nom = ref('')
const energie = ref(50)
const historique = ref(['Système prêt'])

// 2. Les Fonctions (Comportements)
const charger = () => {
  if (energie.value < 100) energie.value += 10
}

const vider = () => {
  if (energie.value > 0) energie.value -= 10
}

const ajouterLigne = () => {
  historique.value.push(`Action à ${new Date().toLocaleTimeString()}`)
}
</script>


<template>
  <div class="conteneur">
    <h1>Mon Composant Vue</h1>

    <div class="bloc">
      <input v-model="nom" placeholder="Ton nom..." />
      <p>Bonjour {{ nom }}</p>
    </div>

    <div class="bloc">
      <p>Batterie : {{ energie }}%</p>
      <div v-if="energie < 20" class="alerte">⚠️ Batterie Faible !</div>
      
      <button @click="charger">Charger</button>
      <button @click="vider">Utiliser</button>
    </div>

    <div class="bloc">
      <ul>
        <li v-for="(item, index) in historique" :key="index">
          {{ item }}
        </li>
      </ul>
      <button @click="ajouterLigne">Ajouter historique</button>
    </div>
  </div>
</template>


<style scoped>
.conteneur {
  max-width: 400px;
  margin: 0 auto;
  font-family: sans-serif;
}

.bloc {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

button {
  margin-right: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.alerte {
  color: red;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>
