from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import chromadb 
splitter = RecursiveCharacterTextSplitter( #taken from the docs website
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
dir = 'rag_docs'
arr = os.listdir(dir)
client = chromadb.PersistentClient()
collection = client.get_or_create_collection(
    name="RAG",
)
for i in arr:
    f = open(f"{dir}/{i}")
    text = f.read()
    chunks = splitter.split_text(text)
    for x in range(len(chunks)):
        collection.add(ids = f"{i}_{x}", documents=chunks[x]) #need to find way to avoid duplicates?? also weirdly overwriting what i had lol
print(collection.query(
    query_texts=["what is the password"], #semantic match
    n_results=1,
))