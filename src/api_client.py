"""
API client module for ExpressionEngine MCP Server

This module handles making requests to the ExpressionEngine API
through the Reinos Webservice add-on.
"""

import logging
import aiohttp
import json
from urllib.parse import urljoin, urlencode

logger = logging.getLogger("ee_mcp.api_client")

class EEError(Exception):
    """Exception raised for ExpressionEngine API errors"""
    
    def __init__(self, message, status_code=None, details=None):
        """Initialize the exception
        
        Args:
            message (str): The error message
            status_code (int, optional): The HTTP status code
            details (dict, optional): Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class EEClient:
    """Client for ExpressionEngine API"""
    
    def __init__(self, base_url, auth):
        """Initialize the API client
        
        Args:
            base_url (str): The base URL for the ExpressionEngine API
            auth (EEAuth): The authentication handler
        """
        self.base_url = base_url
        self.auth = auth
    
    async def request(self, method, endpoint, data=None):
        """Make a request to the ExpressionEngine API
        
        Args:
            method (str): The HTTP method (GET, POST)
            endpoint (str): The API endpoint
            data (dict, optional): The request data
        
        Returns:
            dict: The response data
        
        Raises:
            EEError: If the request fails
        """
        # Build the URL
        url = urljoin(self.base_url, endpoint)
        
        # Get authentication parameters
        auth_params = self.auth.get_auth_params()
        
        # Prepare form data using aiohttp's FormData for proper encoding
        form_data = aiohttp.FormData()
        
        # Add authentication parameters
        for key, value in auth_params.items():
            form_data.add_field(key, str(value))
        
        if data:
            # Convert data to the expected format: data[field_name]
            for key, value in data.items():
                # Handle None values
                if value is None:
                    form_data.add_field(f"data[{key}]", "")
                else:
                    # Use FormData's add_field method which properly handles encoding
                    # including special characters in HTML content
                    form_data.add_field(f"data[{key}]", str(value))
        
        # Get headers
        headers = self.auth.get_auth_headers()
        
        # Log the request
        logger.info(f"Making {method} request to {url}")
        logger.debug(f"Form data fields count: {len(form_data._fields)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    # For GET requests, we still need to use urlencode for query parameters
                    # Convert FormData back to dict for URL encoding
                    url_params = {}
                    for field_info in form_data._fields:
                        # FormData fields are tuples: (name, value, content_type, filename)
                        field_name = field_info[0]
                        field_value = field_info[1]
                        url_params[field_name] = field_value
                    url_with_params = f"{url}?{urlencode(url_params)}"
                    async with session.get(url_with_params) as response:
                        return await self._handle_response(response)
                elif method.upper() == "POST":
                    # For POST requests, send FormData directly
                    async with session.post(url, headers=headers, data=form_data) as response:
                        return await self._handle_response(response)
                else:
                    raise EEError(f"Unsupported HTTP method: {method}")
        except aiohttp.ClientError as e:
            logger.error(f"Request error: {str(e)}")
            raise EEError(f"Request failed: {str(e)}")
    
    async def _handle_response(self, response):
        """Handle the API response
        
        Args:
            response (aiohttp.ClientResponse): The response object
        
        Returns:
            dict: The response data
        
        Raises:
            EEError: If the response indicates an error
        """
        # Get the response text first
        text = await response.text()
        logger.debug(f"Raw response: {text}")
        
        # Check for errors first
        if not response.ok:
            logger.error(f"API error: {response.status} - {text}")
            raise EEError(
                f"API error: {response.status}",
                status_code=response.status,
                details={"text": text}
            )
        
        # Check for PHP fatal errors and other server issues
        if "Fatal error" in text and "memory size" in text:
            logger.error(f"PHP memory exhausted: {text}")
            raise EEError(
                "Server memory exhausted. Try reducing search scope by: 1) Adding more specific search parameters, 2) Reducing the 'limit' parameter, 3) Searching within a specific channel, or 4) Using get_entry for known entry IDs instead of broad searches.",
                status_code=500,
                details={"error_type": "memory_exhausted", "text": text}
            )
        
        elif "Fatal error" in text:
            logger.error(f"PHP fatal error: {text}")
            raise EEError(
                "Server encountered a fatal error. This may be due to invalid parameters or server configuration issues.",
                status_code=500,
                details={"error_type": "php_fatal_error", "text": text}
            )
        
        elif "Warning:" in text or "Notice:" in text:
            logger.warning(f"PHP warning/notice in response: {text}")
            # Don't fail on warnings/notices, but log them
        
        # Try to parse as JSON first
        try:
            data = json.loads(text)
            logger.debug(f"Response data (JSON): {json.dumps(data, indent=2)}")
            return data
        except json.JSONDecodeError:
            # If JSON fails, it might be PHP array format
            # For PHP array responses, we'll return a structured response
            if text.strip().startswith('Array'):
                logger.debug("Response appears to be PHP array format")
                
                # Check for "No Entry found" in PHP array response
                if "No Entry found" in text:
                    return {
                        "success": False,
                        "message": "No entries found matching the search criteria. Try: 1) Broader search terms, 2) Different channel_name, 3) Checking if entries exist with search_entries using just site_id and channel_name",
                        "raw_response": text,
                        "data_type": "php_array_no_results"
                    }
                
                return {
                    "success": True,
                    "message": "Response received in PHP array format",
                    "raw_response": text,
                    "data_type": "php_array"
                }
            else:
                logger.error(f"Invalid response format: {text}")
                raise EEError(
                    "Invalid response format from server. The response was neither valid JSON nor recognized PHP array format.",
                    status_code=response.status,
                    details={"text": text}
                )
    
    async def search_entries(self, params=None):
        """Search entries in the ExpressionEngine API
        
        Args:
            params (dict, optional): Search parameters
        
        Returns:
            dict: The response data
        """
        # Use read_entry endpoint for searching/reading entries
        search_params = params or {}
        return await self.request("GET", "/webservice/rest/read_entry/php", data=search_params)
    
    async def get_entry(self, entry_id, site_id=1):
        """Get a specific entry from the ExpressionEngine API
        
        Args:
            entry_id (int): The entry ID
            site_id (int, optional): The site ID (defaults to 1)
        
        Returns:
            dict: The response data
        """
        return await self.request("GET", "/webservice/rest/read_entry/php", data={
            "site_id": site_id,
            "entry_id": entry_id
        })
    
    async def create_entry(self, entry_data):
        """Create an entry in the ExpressionEngine API
        
        Args:
            entry_data (dict): The entry data
        
        Returns:
            dict: The response data
        """
        return await self.request("POST", "/webservice/rest/create_entry/php", data=entry_data)
    
    async def update_entry(self, entry_id, entry_data):
        """Update an entry in the ExpressionEngine API
        
        Args:
            entry_id (int): The entry ID
            entry_data (dict): The entry data
        
        Returns:
            dict: The response data
        """
        # Add entry_id to the data
        update_data = entry_data.copy()
        update_data["entry_id"] = entry_id
        return await self.request("POST", "/webservice/rest/update_entry/php", data=update_data)
