<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000/users/"

// --- 1. TYPES (Doit correspondre au Backend) ---
interface Event {
  event: string;
  city: string;
  postcode: number;
  date: string;
}

interface User {
  id: number;
  name: string;
  firstname: string;
  birthday: string;
  date_creation: string;
  event?: Event; // Peut être présent (objet) ou absent (null)
}

interface UserForm {
  name: string;
  firstname: string;
  birthday: string;
}

type PageMode = 'menu' | 'liste' | 'ajout' | 'edition' | 'details';

// --- 2. VARIABLES ---
const mode = ref<PageMode>('menu')
const users = ref<User[]>([])
const selectedUserId = ref<number | null>(null)
const currentUser = ref<User | null>(null)

const form = ref<UserForm>({
  name: '',
  firstname: '',
  birthday: ''
})

// --- RECHERCHE ---
const searchId = ref('')      
const searchEvent = ref('')   

// --- FILTRE INTELLIGENT ---
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    
    // 1. Filtre par ID (Si 'searchId' est vide, on prend tout)
    const matchId = searchId.value === '' || user.id === Number(searchId.value)

    // 2. Filtre par Événement (Si 'searchEvent' est vide, on prend tout)
    const searchTerm = searchEvent.value.toLowerCase()
    
    // On vérifie si l'utilisateur a un event ET si son nom correspond
    const matchEvent = searchEvent.value === '' || (
      user.event && user.event.event.toLowerCase().includes(searchTerm)
    )

    // Il faut que les DEUX conditions soient vraies
    return matchId && matchEvent
  })
})

// --- 3. FONCTIONS ---

// Réinitialiser les filtres
const clearFilters = () => {
  searchId.value = ''
  searchEvent.value = ''
}

const goToListe = async () => {
  try {
    const response = await axios.get<User[]>(API_URL)
    users.value = response.data
    mode.value = 'liste'
    clearFilters() // On remet à zéro en arrivant sur la liste
  } catch (error) {
    console.error("Erreur chargement :", error)
  }
}

const showDetails = async (id: number) => {
  try {
    const response = await axios.get<User>(API_URL + id)
    currentUser.value = response.data
    mode.value = 'details'
  } catch (error) {
    console.error("Erreur chargement détails :", error)
    alert("Impossible de charger les détails.")
  }
}

const openCreateForm = () => {
  mode.value = 'ajout'
  form.value = { name: '', firstname: '', birthday: '' }
}

const openEditForm = (user: User) => {
  mode.value = 'edition'
  selectedUserId.value = user.id
  form.value = {
    name: user.name,
    firstname: user.firstname,
    birthday: user.birthday
  }
}

const saveUser = async () => {
  if (!form.value.name) return alert("Remplis le nom !")
  try {
    if (mode.value === 'ajout') {
      await axios.post(API_URL, form.value)
    } else if (mode.value === 'edition' && selectedUserId.value !== null) {
      await axios.put(API_URL + selectedUserId.value, form.value)
    }
    goToListe()
  } catch (error) {
    console.error("Erreur sauvegarde :", error)
  }
}

const deleteUser = async (id: number) => {
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
      
      <div class="filters-container">
        <input 
          v-model="searchId" 
          type="number" 
          placeholder="🔍 ID..." 
          class="filter-input small"
        />
        <input 
          v-model="searchEvent" 
          type="text" 
          placeholder="🎉 Chercher un événement..." 
          class="filter-input large"
        />
        <button v-if="searchId || searchEvent" @click="clearFilters" class="btn-reset" title="Effacer les filtres">
          ❌
        </button>
      </div>

      <ul>
        <li v-for="(user, index) in filteredUsers" :key="user.id" class="user-item">
          
          <div class="user-info">
            <span class="main-text">
              <strong class="row-number">N°{{ index + 1 }}</strong>
              <small class="tech-id">(#{{ user.id }})</small>
              {{ user.firstname }} {{ user.name }}
            </span>
            
            <span v-if="user.event" class="event-badge">
              🎉 {{ user.event.event }}
            </span>
          </div>
          
          <div class="actions">
            <button @click="showDetails(user.id)" class="btn-blue-light">👁️</button>
            <button @click="openEditForm(user)" class="btn-yellow">✏️</button>
            <button @click="deleteUser(user.id)" class="btn-red">🗑️</button>
          </div>
        </li>
      </ul>

      <p v-if="filteredUsers.length === 0 && users.length > 0" class="empty-msg">
        🚫 Aucun résultat. Essaie d'effacer les filtres.
      </p>
      <p v-if="users.length === 0" class="empty-msg">La base de données est vide.</p>
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
      
      <h2>👤 Fiche de {{ currentUser.firstname }} (ID: {{ currentUser.id }})</h2>
      
      <div class="info-box">
        <p><strong>Nom :</strong> {{ currentUser.name }}</p>
        <p><strong>Prénom :</strong> {{ currentUser.firstname }}</p>
        <p><strong>Anniversaire :</strong> {{ currentUser.birthday }}</p>
        <p><strong>Inscrit le :</strong> {{ new Date(currentUser.date_creation).toLocaleString() }}</p>
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
.container { max-width: 600px; margin: 50px auto; font-family: sans-serif; text-align: center; }
.menu-box { border: 2px dashed #ccc; padding: 40px; border-radius: 10px; }
.buttons { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
.card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: left; }
input { display: block; width: 80%; margin: 10px auto; padding: 8px; }

/* Styles Filtres */
.filters-container { display: flex; gap: 8px; margin-bottom: 20px; align-items: center; }
.filter-input { padding: 10px; border: 2px solid #3498db; border-radius: 5px; font-size: 14px; outline: none; margin: 0; }
.filter-input.small { width: 20%; } 
.filter-input.large { width: 70%; }
.filter-input:focus { background-color: #f0f8ff; }
.btn-reset { background: transparent; border: none; font-size: 1.2em; cursor: pointer; padding: 0 5px; }

/* Styles Liste */
.user-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid #eee; }

/* Info User : Flex row pour aligner Nom et Badge */
.user-info { display: flex; flex-direction: row; align-items: center; gap: 10px; flex-wrap: wrap; }
.main-text { font-size: 1em; }

.row-number { color: #2c3e50; font-weight: bold; margin-right: 5px; }
.tech-id { color: #95a5a6; font-size: 0.8em; margin-right: 5px; }

/* Badge Event */
.event-badge {
  background-color: #27ae60; /* Vert pour bien ressortir */
  color: white;
  font-size: 0.75em;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: 12px;
  box-shadow: 0 2px 2px rgba(0,0,0,0.1);
}

/* Boutons */
button { cursor: pointer; padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; color: white; }
.btn-blue { background-color: #3498db; }
.btn-green { background-color: #2ecc71; }
.btn-back { background-color: #95a5a6; margin-bottom: 20px; width: 100%; }

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
.empty-msg { text-align: center; color: #7f8c8d; font-style: italic; margin-top: 20px; }
</style>