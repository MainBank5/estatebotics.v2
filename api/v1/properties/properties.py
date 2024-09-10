import httpx
from fastapi import APIRouter, status

# router object
router = APIRouter(
    prefix="/api/v1/properties",
    tags=['Properties'],
    responses={ 404: {"description" : "Not Found"}}
)


#define a route to an external api 
@router.get("/")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()

