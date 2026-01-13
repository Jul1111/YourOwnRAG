from src.retrievalFunction import retrieve
from src.implementVectorDB import LANGUAGE_MODEL, create_vector_db_from_dataset, VECTOR_DB, reset_vector_db
from src.loadingDataset import load_multiple_files
import ollama
import os
import easygui as eg

def select_knowledge_sources():
    """
    Menu interactif pour choisir les sources via interface graphique.
    Fonctionne sur Windows, macOS et Linux.
    """
    choice = eg.buttonbox(
        msg='Configuration de la base de connaissance\n\nQue voulez-vous charger ?',
        title='YourOwnRAG',
        choices=['Fichiers', 'Dossiers', 'Défaut']
    )
    
    if choice is None:
        return ['tmp/cat-facts.txt']
    
    sources = []
    
    if choice == 'Fichiers':
        # Sélectionner plusieurs fichiers
        files = eg.fileopenbox(
            msg='Sélectionnez les fichiers à charger',
            title='Sélection de fichiers',
            multiple=True,
            filetypes=["*.txt", "*.pdf", "*.py", "*.json", "*.yaml", "*.*"]
        )
        if files:
            sources = files if isinstance(files, list) else [files]
            print(f"\n✓ {len(sources)} fichier(s) sélectionné(s)")
            for f in sources:
                print(f"  - {os.path.basename(f)}")
        else:
            print("\n✗ Aucun fichier sélectionné")
    
    elif choice == 'Dossiers':
        # Sélectionner plusieurs dossiers
        print("\nVous pouvez sélectionner plusieurs dossiers")
        count = 0
        while True:
            folder = eg.diropenbox(
                msg='Sélectionnez un dossier (Annuler pour terminer)',
                title='Sélection de dossier'
            )
            if not folder:
                break
            sources.append(folder)
            count += 1
            print(f"✓ Dossier {count} ajouté: {os.path.basename(folder)}")
        
        if sources:
            print(f"\n✓ Total: {len(sources)} dossier(s) sélectionné(s)")
        else:
            print("\n✗ Aucun dossier sélectionné")
    
    else:  # Défaut
        sources = ['tmp/cat-facts.txt']
        print("✓ Sources par défaut chargées")
    
    return sources if sources else ['tmp/cat-facts.txt']

# Réinitialiser la base de vecteurs
reset_vector_db()

# Sélectionner les sources de connaissance
sources = select_knowledge_sources()

# Charger et créer la base de données vectorielle
print('\nChargement des sources...')
chunks = load_multiple_files(sources)
create_vector_db_from_dataset(chunks)

print('\n' + '='*50)
print('Chatbot is ready! Type "exit" to quit.')
print('='*50 + '\n')

# Main chatbot loop
while True:
    # Get user input
    input_query = input('You: ')
    
    # Check if user wants to exit
    if input_query.lower() == 'exit':
        print('Goodbye!')
        break
    
    if not input_query.strip():
        continue
    
    retrieved_knowledge = retrieve(input_query)

    print('\nRetrieved knowledge:')
    for chunk, similarity in retrieved_knowledge:
      print(f' - (similarity: {similarity:.2f}) {chunk}')

    context = '\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])
    instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{context}'''

    stream = ollama.chat(
      model=LANGUAGE_MODEL,
      messages=[
        {'role': 'system', 'content': instruction_prompt},
        {'role': 'user', 'content': input_query},
      ],
      stream=True,
    )

    # print the response from the chatbot in real-time
    print('\nChatbot response:', end='')
    for chunk in stream:
      print(chunk['message']['content'], end='', flush=True)
    print('\n')