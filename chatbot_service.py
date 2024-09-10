import openai
import os
import httpx
import logging
from pydantic import BaseModel
import re
from onoffice_service import OnOfficeAPI

# Initialize logging for easier debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    prompt: str


class ChatbotService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.onOffice = OnOfficeAPI(
            os.getenv("ONOFFICE_API_KEY"), os.getenv("ONOFFICE_SECRET_TOKEN")
        )  # Initialize OnOfficeAPI

    async def get_response(self, prompt):
        if not prompt:
            logger.error("Prompt is empty.")
            return "Sorry, the prompt cannot be empty."

        # Check for price and location in the prompt
        price_match = re.search(r"(\d+)", prompt)  # Extract numbers from the prompt
        location_match = re.search(r"in (.+)", prompt)  # Extract location after 'in'

        price = int(price_match.group(0)) if price_match else None
        location = location_match.group(1).strip() if location_match else None

        # If both price and location are found, query the OnOffice API
        if price and location:
            properties = await self.onOffice.search_properties(
                price_max=price, location=location
            )
            if properties:
                return (
                    f"I found {len(properties)} properties in {location} under {price}."
                )
            else:
                return f"No properties found in {location} under {price}."

        # If not querying properties, proceed with the OpenAI response
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai.api_key}",
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Don't give me any response that too large. Give me response maxing out at 500 characters.You are a realtor and you will only answer to that.Help my client get info or feed back - if any on their query. Here's their query; {prompt}. Remember, if anything is unclear just say; I am sorry I am a real statate bot and would love to help out on anything connected to our business.",
                            }
                        ],
                    },
                )
                logging.info(response)

                response.raise_for_status()
                logger.debug(response.json())  # View the response format
                return response.json()["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as http_err:
                logger.error(
                    f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}"
                )
                return f"HTTP error: {http_err.response.status_code}. Please try again later."

            except httpx.RequestError as req_err:
                logger.error(f"Request error occurred: {req_err}")
                return "Network error: Unable to connect to the OpenAI API. Please check your internet connection."

            except Exception as e:
                logger.error(
                    f"Unexpected error while getting ChatGPT API response: {e}"
                )
                return "Sorry, I couldn't process your request!"
