import hmac
import hashlib
import time
import base64
import httpx
import logging

# Initialize logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OnOfficeAPI:
    def __init__(self, api_key, secret_token):
        self.api_key = api_key
        self.secret_token = secret_token.encode('utf-8')  # Encode the secret key
        self.base_url = "https://api.onoffice.de/api/stable/api.php"

    def generate_hmac(self, timestamp, action, resourcetype):
        """
        Generate HMAC signature for authentication.
        """
        hmac_string = f"{timestamp}{self.api_key}{resourcetype}{action}".encode('utf-8')
        logger.debug(f"HMAC Message: {hmac_string}")
        
        hmac_digest = hmac.new(self.secret_token, hmac_string, hashlib.sha256).digest()
        hmac_base64 = base64.b64encode(hmac_digest).decode('utf-8')
        
        logger.debug(f"Generated HMAC (base64): {hmac_base64}")
        return hmac_base64

    async def make_request(self, action, resource_type, parameters):
        """
        Make a request to the OnOffice API.
        """
        timestamp = str(int(time.time()))
        hmac_signature = self.generate_hmac(timestamp, action, resource_type)
        
        payload = {
            "token": self.api_key,
            "request": {
                "actions": [
                    {
                        "actionid": action,
                        "resourcetype": resource_type,
                        "resourceid": "",
                        "identifier": "",
                        "timestamp": timestamp,
                        "hmac": hmac_signature,
                        "hmac_version": 2,
                        "parameters": parameters
                    }
                ]
            }
        }
        
        logger.debug(f"Request payload: {payload}")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                logger.debug(f"Response from OnOfficeAPI: {result}")
                
                return result
            except httpx.RequestError as req_err:
                logger.error(f"An error occurred: {req_err}")
                raise
            except httpx.HTTPStatusError as http_err:
                # Handle HTTP errors (e.g., 4xx and 5xx responses)
                logger.error(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
                return f"HTTP error: {http_err.response.status_code}. Please try again later."
            except Exception as e:
                logger.error(f"unexpected error occured : {e}")
                return "Sorry couldnt complete your request. Error"

    async def fetch_properties(self):
        """
        Call the make_request method to fetch properties.
        """
        action = "urn:onoffice-de-ns:smart:2.5:smartml:action:read"
        resource_type = "estate"
        parameters = {
            "data": ["Id", "kaufpreis", "lage"],  # Specify the fields you want to retrieve
            "filter": {
                "status": [{"op": "=", "val": 1}],  # Example filter for active properties
                "kaufpreis": [{"op": "<", "val": 300000}]  # Example filter for price
            },
            "listlimit": 10  # Limit the number of properties returned
        }
        
        return await self.make_request(action, resource_type, parameters)
    
    async def fetch_all_properties(self):
        """
        Call the make_request method to fetch all properties without filters.
          """
        action = "urn:onoffice-de-ns:smart:2.5:smartml:action:read"
        resource_type = "estate"
        parameters = {
        "data": ["Id", "kaufpreis", "lage"],  # Specify the fields you want to retrieve
        "listlimit": 100,  # Adjust the limit as needed
        "listoffset": 0    # Start from the first record
        
        }
    
        return await self.make_request(action, resource_type, parameters)
    
    async def search_properties(self, filters=None, limit=100, offset=0):
       """
      Search for properties based on provided filters.
    
      Args:
        filters (dict): A dictionary of filters to apply to the search.
        limit (int): The maximum number of properties to return.
        offset (int): The offset for pagination.
    
      Returns:
          dict: The response from the API containing the search results.
       """
       action = "urn:onoffice-de-ns:smart:2.5:smartml:action:read"
       resource_type = "estate"
    
       parameters = {
        "data": ["Id", "kaufpreis", "lage"],  # Specify the fields you want to retrieve
        "listlimit": limit,
        "listoffset": offset
         }

       if filters:
        parameters["filter"] = filters  # Add filters if provided
    
       return await self.make_request(action, resource_type, parameters)