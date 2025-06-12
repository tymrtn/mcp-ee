#!/usr/bin/env python3
"""
ExpressionEngine MCP Server

This server provides MCP tools for interacting with an ExpressionEngine site
through the Reinos Webservice API.
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from api_client import EEClient, EEError
from auth import EEAuth

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "..", "ee_mcp.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger("ee_mcp")

# Initialize FastMCP server
mcp = FastMCP("ee-mcp")

class EEMcpServer:
    """ExpressionEngine MCP Server"""
    
    def __init__(self):
        """Initialize the MCP server"""
        # Get configuration from environment variables
        self.api_url = os.environ.get("API_URL", "")
        self.shortkey = os.environ.get("SHORTKEY", "")
        
        # Validate configuration
        if not self.api_url or not self.shortkey:
            logger.error("Missing required environment variables: API_URL and/or SHORTKEY")
            sys.exit(1)
        
        # Initialize authentication and client
        self.auth = EEAuth(self.shortkey)
        self.client = EEClient(self.api_url, self.auth)
        
        logger.info(f"Initialized EE MCP Server for: {self.api_url}")

# Initialize the server
server = EEMcpServer()

# Define the tool function
async def manage_content(action: str = None, params: Dict[str, Any] = None) -> str:
    """Interact with ExpressionEngine content.

Args:
    action: The action to perform. Available actions: search_entries, get_entry, create_entry, update_entry
    params: Parameters for the action

Available Actions:
- search_entries: Search for entries (params: site_id, channel_name, limit, etc.)
- get_entry: Get a specific entry (params: entry_id, site_id)
- create_entry: Create a new entry (params: site_id, channel_name, title, status, etc.)  
- update_entry: Update an existing entry (params: entry_id, site_id, title, status, etc.)

Example entry data fields:
- site_id: Site ID (usually 1)
- channel_name: Channel name (e.g., 'expatinfo', 'blog')
- title: Entry title
- status: Entry status ('open', 'closed', 'featured')
- summary: Entry summary/excerpt
- body: Entry body content
- title2: Secondary title field
"""
    # Convert params from MultiDict to dict if it's not None
    if params:
        params = dict(params)
    else:
        params = {}

    if not action:
        return "Missing required parameter: action"
    
    # Get the client
    client = server.client
    
    # Handle the action
    try:
        if action == "search_entries":
            result = await client.search_entries(params)
            return json.dumps(result, indent=2)
        
        elif action == "get_entry":
            entry_id = params.get("entry_id")
            site_id = params.get("site_id", 1)
            if not entry_id:
                return "Missing required parameter: entry_id"
            result = await client.get_entry(entry_id, site_id)
            return json.dumps(result, indent=2)
        
        elif action == "create_entry":
            # Validate required fields
            required_fields = ["site_id", "channel_name", "title", "status"]
            missing_fields = [field for field in required_fields if not params.get(field)]
            if missing_fields:
                return f"Missing required parameters: {', '.join(missing_fields)}"
            
            result = await client.create_entry(params)
            return json.dumps(result, indent=2)
        
        elif action == "update_entry":
            entry_id = params.get("entry_id")
            if not entry_id:
                return "Missing required parameter: entry_id"
            
            # Remove entry_id from params since it's handled separately
            update_params = {k: v for k, v in params.items() if k != "entry_id"}
            result = await client.update_entry(entry_id, update_params)
            return json.dumps(result, indent=2)
        
        else:
            available_actions = [
                "search_entries", "get_entry", "create_entry", "update_entry"
            ]
            return f"Invalid action: {action}. Available actions: {', '.join(available_actions)}"
    
    except EEError as e:
        logger.error(f"EE API error executing action {action}: {e.message}")
        # Return the helpful error message from EEError
        return f"Error: {e.message}"
    
    except Exception as e:
        logger.error(f"Unexpected error executing action {action}: {str(e)}")
        return f"Unexpected error executing action {action}: {str(e)}"

# Register the tool
ee = mcp.tool()(manage_content)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")
