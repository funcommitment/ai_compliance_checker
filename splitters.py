from langchain_text_splitters import RecursiveCharacterTextSplitter
from loaders import load_file

docs=load_file("SampleBusinessContract.docx")

def split_chunks(doc_split):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000, #max thousand characters
        chunk_overlap=100 #100 character from previous chunk to next chunk for safety so nothing important misses
    )

    return splitter.split_documents(doc_split)

#splitted_chunks=split_chunks(docs)
#print(len(splitted_chunks))