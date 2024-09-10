import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import APIRouter, status, Query
from fastapi import Response, Depends, HTTPException
from onoffice_service import OnOfficeAPI

# retrieve the API_key and secret token
API_KEY = os.getenv("ONOFFICE_API_KEY")
SECRET_TOKEN = os.getenv("ONOFFICE_SECRET_TOKEN")

# initialize onOfficeAPI
onOffice = OnOfficeAPI(API_KEY, SECRET_TOKEN)


# router object
router = APIRouter(
    prefix="/api/v1/onoffice",
    tags=["On-Office"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/properties")
async def get_properties():
    try:
        properties = await onOffice.fetch_properties()
        return properties["response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {e}")


@router.get("/properties/all")
async def get_all_properties():
    try:
        # Ensure you are calling the method on the instance
        properties = (
            await onOffice.fetch_all_properties()
        )  # Correctly referencing the instance
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {e}")


# Define a route to search properties
@router.get("/properties/search")
async def search_properties(
    price_max: int = Query(None, description="Maximum price"),
    location: str = Query(None, description="Location to search for"),
    limit: int = Query(100, description="Number of results to return"),
    offset: int = Query(0, description="Offset for pagination"),
):
    filters = {}

    if price_max is not None:
        filters["kaufpreis"] = [{"op": "<", "val": price_max}]

    if location is not None:
        filters["lage"] = [
            {"op": "LIKE", "val": f"%{location}%"}
        ]  # Using LIKE for partial matches

    try:
        properties = await onOffice.search_properties(
            filters=filters, limit=limit, offset=offset
        )
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search properties: {e}")
