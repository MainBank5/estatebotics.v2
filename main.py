from fastapi import FastAPI, HTTPException, Query
from onoffice_service import OnOfficeAPI
from chatbot_service import ChatbotService, ChatRequest
from dotenv import load_dotenv
import os
import httpx

#load environment variables 
load_dotenv()

#create app instance 
app = FastAPI()

#retrieve the API_key and secret token
API_KEY = os.getenv('ONOFFICE_API_KEY')
SECRET_TOKEN = os.getenv("ONOFFICE_SECRET_TOKEN")

#initialize onOfficeAPI
onOffice = OnOfficeAPI(API_KEY, SECRET_TOKEN)

#initilize the OpenAI chatbot api 
chatbot = ChatbotService()

#define a route
@app.get("/")
def read_root():
    return {"Hello": "World"}

#define a route to an external api 
@app.get("/properties")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()


@app.get("/onoffice/properties")
async def get_properties():
    try:
       properties = await onOffice.fetch_properties()
       return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {e}")

@app.get('/onoffice/properties/all')
async def get_all_properties():
    try:
        # Ensure you are calling the method on the instance
        properties = await onOffice.fetch_all_properties()  # Correctly referencing the instance
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {e}")

# Define a route to search properties
@app.get("/onoffice/properties/search")
async def search_properties( price_max: int = Query(None, description="Maximum price"), 
        location: str = Query(None, description="Location to search for"), 
        limit: int = Query(100, description="Number of results to return"),
        offset: int = Query(0, description="Offset for pagination")
    ):
    filters = {}
    
    if price_max is not None:
        filters["kaufpreis"] = [{"op": "<", "val": price_max}]
    
    if location is not None:
        filters["lage"] = [{"op": "LIKE", "val": f"%{location}%"}]  # Using LIKE for partial matches

    try:
        properties = await onOffice.search_properties(filters=filters, limit=limit, offset=offset)
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search properties: {e}")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await chatbot.get_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {e}")