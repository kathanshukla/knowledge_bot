from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#storing the data of pdfs into the loader variable
loader = PyPDFDirectoryLoader("/home/damner/code/pdf")
data = loader.load()

# Creating chunks of documents
text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=300,
    chunk_overlap=50,
    separators = ["\n\n","\n", "(?<=\. )"," ", ""]
)

text_chunks = text_splitter.split_documents(data)
print(len(text_chunks))
