-- 1. Table des ENTREPRISES (Tenants)
-- C'est la première table à créer car tout le monde dépend d'elle.
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    nom_societe VARCHAR(255) NOT NULL,
    adresse VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table des UTILISATEURS
-- Liés à une entreprise.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    nom VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    role VARCHAR(50), -- Admin, Employé...
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- 3. Table des FOURNISSEURS
CREATE TABLE fournisseurs (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(150),
    telephone VARCHAR(20),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- 4. Table des PRODUITS
-- Attention : contient seuil_alerte et le lien fournisseur
CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    fournisseur_id INT,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100), -- Référence unique du produit
    prix DECIMAL(10, 2),
    quantite_stock INT DEFAULT 0,
    seuil_alerte INT DEFAULT 10,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id)
);

-- 5. Table des COMMANDES (Achats fournisseurs)
CREATE TABLE commandes (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    fournisseur_id INT NOT NULL,
    date_commande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR(50), -- En attente, Reçue...
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id)
);

-- 6. Table de LIAISON (Contenu des commandes)
-- Pour dire : "Dans la commande 1, il y a 5 iPhone et 2 chargeurs"
CREATE TABLE ligne_commandes (
    id SERIAL PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite_commandee INT NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commandes(id),
    FOREIGN KEY (produit_id) REFERENCES produits(id)
);

-- 7. Table des MOUVEMENTS DE STOCK (La plus importante pour la traçabilité)
CREATE TABLE mouvements (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    produit_id INT NOT NULL,
    user_id INT NOT NULL,
    type_mouvement VARCHAR(10) NOT NULL, -- 'ENTREE' ou 'SORTIE'
    quantite INT NOT NULL,
    date_mouvement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motif VARCHAR(255), -- Vente, Vol, Perte, Achat...
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (produit_id) REFERENCES produits(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);