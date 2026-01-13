# Plan de Développement : Création d'un RAG personnalisé
---

## Phase 1 : Préparation et Chargement des Données
* **Objectif :** Préparer l'environnement et extraire le texte brut.
* **Actions :**
    * Installer les dépendances (`langchain`, `chromadb`, `sentence-transformers`, etc.).
    * Configurer le `DocumentLoader` (ex: `PyPDFLoader` ou `TextLoader`).
    * **Critère de validation :** Afficher dans la console le contenu texte du premier document chargé.

## Phase 2 : Segmentation (Chunking)
* **Objectif :** Découper les documents en morceaux de taille égale pour le modèle.
* **Actions :**
    * Implémenter `RecursiveCharacterTextSplitter`.
    * Ajuster `chunk_size` (ex: 500) et `chunk_overlap` (ex: 50).
    * **Critère de validation :** Vérifier que le nombre total de segments (chunks) est cohérent et que le texte n'est pas coupé en plein milieu d'un mot important.

## Phase 3 : Embeddings et Vector Store
* **Objectif :** Transformer le texte en données numériques et le stocker.
* **Actions :**
    * Charger un modèle d'embedding (ex: `all-MiniLM-L6-v2`).
    * Indexer les segments dans une base de données vectorielle (ChromaDB ou FAISS).
    * **Critère de validation :** Effectuer une recherche de similarité simple (`vectorstore.similarity_search("question")`) et obtenir des segments pertinents sans erreur.

## Phase 4 : Pipeline de Récupération (Retriever) et LLM
* **Objectif :** Connecter la base de données au modèle de langage.
* **Actions :**
    * Configurer l'accès au LLM (Hugging Face Hub API ou modèle local via Ollama/Llama.cpp).
    * Définir le `Prompt Template` (Instruction + Contexte + Question).
    * Créer la chaîne finale (RetrievalQA).
    * **Critère de validation :** Le système doit répondre à une question simple en citant le contexte.

## Phase 5 : Évaluation et Optimisation
* **Objectif :** Fiabiliser les réponses.
* **Actions :**
    * Tester les cas limites (questions hors contexte).
    * Ajuster le paramètre `k` (nombre de segments récupérés).
    * **Critère de validation :** Le RAG répond correctement à un jeu de 5 questions tests sans "halluciner".