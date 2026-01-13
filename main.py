from src.retrievalFunction import retrieve
from src.implementVectorDB import LANGUAGE_MODEL, create_vector_db_from_dataset, VECTOR_DB, reset_vector_db
from src.loadingDataset import load_multiple_files
import ollama

# Réinitialiser au cas où
reset_vector_db()
# Load dataset and create vector database
# Charger depuis plusieurs sources
chunks = load_multiple_files([
    'tmp/cat-facts.txt',
    'data/',
    'src/mon_module.py',
    'config.json',
])
create_vector_db_from_dataset(chunks)

print('\n' + '='*50)
print('Chatbot is ready! Type "exit" to quit.')
print('='*50 + '\n')

# Main chatbot loop
while True:
    # Get user input
    input_query = input('Ask me a question: ')
    
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