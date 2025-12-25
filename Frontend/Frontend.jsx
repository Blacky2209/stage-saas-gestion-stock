/*
import { useState } from 'react'
import './App.css'

function App() {
  // 1. Le STATE : C'est la mémoire de la page.
  // Au début, c'est "null" (vide) car on n'a pas encore demandé le fruit.
  const [monFruit, setMonFruit] = useState(null);

  // 2. La FONCTION : C'est l'action d'aller chercher l'info
  const commanderFruit = async () => {
    try {
      // On appelle l'adresse du Backend
      const reponse = await fetch("http://127.0.0.1:8000/fruit-au-hasard");
      // On transforme la réponse en JSON (format lisible)
      const donnees = await reponse.json();
      
      // On met à jour la mémoire (le State)
      setMonFruit(donnees);
      
    } catch (erreur) {
      console.error("Erreur : Le backend ne répond pas !", erreur);
    }
  }

  // 3. L'AFFICHAGE (Le JSX)
  return (
    <div style={{ padding: '50px', textAlign: 'center' }}>
      <h1>🍎 Ma Boutique de Fruits</h1>
      
      <p>Clique pour demander le stock au serveur Python :</p>
      
      <button onClick={commanderFruit} style={{ fontSize: '20px', padding: '10px' }}>
        Chercher un fruit
      </button>

      { Si monFruit existe, on l'affiche. Sinon on n'affiche rien }
      {monFruit && (
        <div style={{ marginTop: '20px', border: '2px solid green', padding: '20px' }}>
          <h2>C'est une {monFruit.nom} !</h2>
          <p>Prix : <strong>{monFruit.prix} €</strong></p>
        </div>
      )}
    </div>
  )
}

export default App
*/


import { useState } from 'react'
import './App.css'

function App() {
  // --- LES STATES (Mémoire) ---
  const [nomFruit, setNomFruit] = useState(""); // Ce que l'utilisateur tape
  const [reponseServeur, setReponseServeur] = useState(""); // Ce que Python répond

  // --- LA FONCTION D'ENVOI (POST) ---
  const envoyerCommande = async () => {
    // 1. On prépare les données
    const maDonnee = {
      nom: nomFruit,
      prix: 5.50 // On met un prix fixe pour l'exemple
    };

    try {
      // 2. On envoie la requête
      const reponse = await fetch("http://127.0.0.1:8000/commander", {
        method: "POST", // <--- TRÈS IMPORTANT : On passe en mode écriture
        headers: {
          "Content-Type": "application/json" // On prévient Python qu'on envoie du JSON
        },
        body: JSON.stringify(maDonnee) // On transforme l'objet JS en texte
      });

      // 3. On traite la réponse
      const data = await reponse.json();
      setReponseServeur(data.message);

    } catch (error) {
      console.error("Erreur d'envoi", error);
    }
  }

  // --- L'AFFICHAGE ---
  return (
    <div style={{ padding: '50px', textAlign: 'center' }}>
      <h1>🚚 Envoyer une commande à Python</h1>

      <div style={{ margin: '20px' }}>
        <input 
          type="text" 
          placeholder="Nom du fruit (ex: Ananas)"
          value={nomFruit}
          // À chaque lettre tapée, on met à jour le State
          onChange={(e) => setNomFruit(e.target.value)} 
          style={{ padding: '10px', marginRight: '10px' }}
        />
        
        <button onClick={envoyerCommande} style={{ padding: '10px' }}>
          Envoyer
        </button>
      </div>

      {/* Affichage de la réponse du serveur */}
      {reponseServeur && (
        <p style={{ color: 'green', fontWeight: 'bold' }}>
          Réponse de Python : {reponseServeur}
        </p>
      )}
    </div>
  )
}

export default App