from langchain_community.document_loaders import UnstructuredWordDocumentLoader,TextLoader,PyPDFLoader

def load_file(file_name):
    f_extension=file_name.split('.')[-1].lower()
    
    if f_extension=="txt":
        loader=TextLoader(file_name)
    elif f_extension=="docx":
        loader=UnstructuredWordDocumentLoader(file_name)
    elif f_extension=="pdf":
        loader=PyPDFLoader(file_name)
    else:
        raise ValueError("Not the right format either in text,pdf or docx only")
    
    return loader.load()

#docs=load_file("SampleBusinessContract.docx")
#print(docs))

