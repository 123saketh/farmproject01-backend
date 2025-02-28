from bson import ObjectId
from fastapi import FastAPI, HTTPException,status
from app.Models.UpdateUser import UpdateUser
from app.Models.User import User
from .db import MongoDB
from fastapi.middleware.cors import CORSMiddleware
import logging
from pymongo.results import InsertOneResult , UpdateResult, DeleteResult
from .constants import sampleDb,sampleDb_users

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():

    return {"message": "Hello, Namaste!"}

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "email": user["email"],
        "jobTitle": user["jobTitle"],
        "gender": user["gender"]
        # Add other fields as needed
    }

@app.get('/users')
async def getusers():
    try:
        # Initialize MongoDB connection
        mongo_instance = MongoDB(db_name=sampleDb, collection_name=sampleDb_users)
        collection = mongo_instance.get_collection()
        users = await collection.find().to_list(100)
        return {"users": [user_helper(user) for user in users]}
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get('/users/{user_id}',response_model=User,status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id:str):
    try:
        # Initialize MongoDB connection
        mongo_instance = MongoDB(db_name=sampleDb, collection_name=sampleDb_users)
        collection = mongo_instance.get_collection()
        user = await collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_helper(user)
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error fetching user by id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user:User):
    try:
        # Initialize MongoDB connection
        mongo_instance = MongoDB(db_name=sampleDb, collection_name=sampleDb_users)
        collection = mongo_instance.get_collection()
        user_dict = user.model_dump()  # Convert the user object to a dictionary using model_dump
        result: InsertOneResult = await collection.insert_one(user_dict)
        return {"id":str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.put('/users/{user_id}',response_model=User,status_code = status.HTTP_200_OK)
async def update_user(user_id:str,user:UpdateUser):
    try:
        # Initialize MongoDB connection
        mongo_instance = MongoDB(db_name=sampleDb, collection_name=sampleDb_users)
        collection = mongo_instance.get_collection()
        update_data = {k: v for k, v in user.model_dump().items() if v is not None}
        result:UpdateResult = await collection.find_one_and_update({"_id":ObjectId(user_id)},
                                                             {"$set":update_data},
                                                             return_document=True
                                                             )
        
        if result:
            return user_helper(result)
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error updating user by id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.delete('/users/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:str):
    try:
        # Initialize MongoDB connection
        mongo_instance = MongoDB(db_name=sampleDb, collection_name=sampleDb_users)
        collection = mongo_instance.get_collection()
        result:DeleteResult = await collection.find_one_and_delete({"_id":ObjectId(user_id)})
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return
    except Exception as e:
        logger.error(f"Error deleting user by id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

