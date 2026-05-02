from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
import os
arr = os.listdir('rag_docs')
for i in arr:
    f = open(f"rag_docs/{i}")
    chunks = splitter.split_text(f.read())
    print(chunks)
#chunks = splitter.split_text(document)