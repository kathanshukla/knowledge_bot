# import load
import google.generativeai as palm
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import os
from langchain_community.embeddings import GooglePalmEmbeddings
from dotenv import load_dotenv
# import main

#configuring google API
load_dotenv()
palm.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# loading Environment Variable --> mongo_uri
mongo_url = os.getenv('mongo_url')


# setting up the client and checking the connection
uri = mongo_url
client = MongoClient(uri, server_api=ServerApi('1'))# Create a new client and connect to the server

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


create_new_database = False

# MongoDB connection
if(True):
    DB_NAME = "policy_database"
    COLLECTION_NAME = "knowledge_bot"
    MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

    if(create_new_database):
        vector_search = MongoDBAtlasVectorSearch.from_documents(
            documents=load.text_chunks,
            embedding = GooglePalmEmbeddings(),
            collection=MONGODB_COLLECTION,
            # index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME
        )
    
    # creatubg cariable for vector searching
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        uri,
        DB_NAME + "." + COLLECTION_NAME,
        GooglePalmEmbeddings(),
    )




    
print("Execution is done!")
