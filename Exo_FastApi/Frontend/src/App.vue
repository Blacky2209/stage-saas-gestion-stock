<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000/users/"

// 1. NAVIGATION ('menu', 'liste', 'ajout', 'edition', 'details')
const mode = ref('menu')

// 2. DONNÉES
const users = ref([])
const selectedUserId = ref(null) // Pour savoir QUI on modifie
const currentUser = ref(null)    // Pour stocker les infos de la fiche détail

const form = ref({
  name: '',
  firstname: '',
  birthday: ''
})

// --- FONCTIONS ---

// A. Voir la liste
const goToListe = async () => {
  try {
    const response = await axios.get(API_URL)
    users.value = response.data
    mode.value = 'liste'
  } catch (error) {
    console.error("Erreur chargement :", error)
  }
}

// B. Voir les DÉTAILS d'un utilisateur
const showDetails = async (id) => {
  try {
    // On appelle la route GET /users/ID
    const response = await axios.get(API_URL + id)
    currentUser.value = response.data
    mode.value = 'details' // On change l'écran vers la fiche
  } catch (error) {
    console.error("Erreur chargement détails :", error)
    alert("Impossible de charger les détails.")
  }
}

// C. Préparer le formulaire pour la Création
const openCreateForm = () => {
  mode.value = 'ajout'
  form.value = { name: '', firstname: '', birthday: '' }
}

// D. Préparer le formulaire pour l'Edition
const openEditForm = (user) => {
  mode.value = 'edition'
  selectedUserId.value = user.id
  form.value = {
    name: user.name,
    firstname: user.firstname,
    birthday: user.birthday
  }
}

// E. Sauvegarder (Create / Update)
const saveUser = async () => {
  if (!form.value.name) return alert("Remplis le nom !")

  try {
    if (mode.value === 'ajout') {
      await axios.post(API_URL, form.value)
    } else if (mode.value === 'edition') {
      await axios.put(API_URL + selectedUserId.value, form.value)
    }
    goToListe()
  } catch (error) {
    console.error("Erreur sauvegarde :", error)
  }
}

// F. Supprimer
const deleteUser = async (id) => {
  if (!confirm("Supprimer cet utilisateur ?")) return
  try {
    await axios.delete(API_URL + id)
    goToListe() 
  } catch (error) {
    console.error("Erreur suppression :", error)
  }
}
</script>

<template>
  <div class="container">
    <h1>Application Anniversaire 🎂</h1>

    <div v-if="mode === 'menu'" class="menu-box">
      <h2>Que veux-tu faire ?</h2>
      <div class="buttons">
        <button @click="goToListe" class="btn-blue">Voir la liste 📋</button>
        <button @click="openCreateForm" class="btn-green">Créer un User ➕</button>
      </div>
    </div>

    <div v-else-if="mode === 'liste'" class="card">
      <button @click="mode = 'menu'" class="btn-back">⬅ Retour au menu</button>
      <h2>Liste des utilisateurs</h2>
      
      <ul>
        <li v-for="user in users" :key="user.id" class="user-item">
          <span>{{ user.firstname }} {{ user.name }} ({{ user.birthday }})</span>
          
          <div class="actions">
            <button @click="showDetails(user.id)" class="btn-blue-light">👁️</button>
            
            <button @click="openEditForm(user)" class="btn-yellow">✏️</button>
            
            <button @click="deleteUser(user.id)" class="btn-red">🗑️</button>
          </div>
        </li>
      </ul>
      <p v-if="users.length === 0">Aucun utilisateur.</p>
    </div>

    <div v-else-if="mode === 'ajout' || mode === 'edition'" class="card">
      <button @click="mode = 'menu'" class="btn-back">⬅ Annuler</button>
      
      <h2 v-if="mode === 'ajout'">Nouvel Utilisateur</h2>
      <h2 v-else>Modifier l'utilisateur</h2>
      
      <input v-model="form.firstname" placeholder="Prénom" />
      <input v-model="form.name" placeholder="Nom" />
      <input type="date" v-model="form.birthday" />
      
      <button @click="saveUser" class="btn-green">
        {{ mode === 'ajout' ? 'Créer' : 'Mettre à jour' }}
      </button>
    </div>

    <div v-else-if="mode === 'details' && currentUser" class="card details-card">
      <button @click="mode = 'liste'" class="btn-back">⬅ Retour à la liste</button>
      
      <h2>👤 Fiche de {{ currentUser.firstname }}</h2>
      
      <div class="info-box">
        <p><strong>Nom :</strong> {{ currentUser.name }}</p>
        <p><strong>Prénom :</strong> {{ currentUser.firstname }}</p>
        <p><strong>Anniversaire :</strong> {{ currentUser.birthday }}</p>
        <p><strong>Date d'ajout :</strong> {{ new Date(currentUser.date_creation).toLocaleString() }}</p>
      </div>

      <div class="future-event-zone">
        
        <div v-if="currentUser.event">
          <h3>🎉 Prochain Événement !</h3>
          <p><strong>Quoi :</strong> {{ currentUser.event.event }}</p>
          <p><strong>Ville :</strong> {{ currentUser.event.city }} ({{ currentUser.event.postcode }})</p>
          <p><strong>Quand :</strong> {{ currentUser.event.date }}</p>
        </div>

        <div v-else>
          <p>😢 Aucun événement prévu pour cette date exacte (Jour/Mois).</p>
        </div>

      </div>
    </div>

  </div>
</template>

<style scoped>
.container { max-width: 500px; margin: 50px auto; font-family: sans-serif; text-align: center; }
.menu-box { border: 2px dashed #ccc; padding: 40px; border-radius: 10px; }
.buttons { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
.card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: left; }
input { display: block; width: 80%; margin: 10px auto; padding: 8px; }

/* Boutons */
button { cursor: pointer; padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; color: white; }
.btn-blue { background-color: #3498db; }
.btn-green { background-color: #2ecc71; }
.btn-back { background-color: #95a5a6; margin-bottom: 20px; width: 100%; }

/* Style liste */
ul { padding: 0; list-style: none; }
.user-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }

/* Boutons d'action */
.actions { display: flex; gap: 5px; }
.btn-red { background-color: #e74c3c; }
.btn-yellow { background-color: #f1c40f; color: black; }
.btn-blue-light { background-color: #3498db; margin-right: 5px; }

.btn-red:hover { background-color: #c0392b; }
.btn-yellow:hover { background-color: #f39c12; }
.btn-blue-light:hover { background-color: #2980b9; }

/* Style Détails */
.details-card { text-align: center; background: #fdfefe; }
.info-box { background: #ecf0f1; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: left; }
.future-event-zone { border: 2px dashed #bdc3c7; padding: 10px; color: #34495e; background-color: #f9f9f9; }
h3 { margin-top: 0; color: #e67e22; }
</style>