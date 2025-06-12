"""
Tools module for ExpressionEngine MCP Server

This module handles the MCP tools for interacting with the ExpressionEngine API.
"""

import logging
from modelcontextprotocol.types import ErrorCode, McpError

logger = logging.getLogger("ee_mcp.tools")

async def handle_ee_tool(client, args):
    """Handle the EE tool
    
    Args:
        client (EEClient): The ExpressionEngine API client
        args (dict): The tool arguments
    
    Returns:
        dict: The tool response
    
    Raises:
        McpError: If the action is invalid or the request fails
    """
    # Get the action and parameters
    action = args.get("action")
    params = args.get("params", {})
    
    # Log the action
    logger.info(f"Handling EE tool action: {action}")
    logger.debug(f"Parameters: {params}")
    
    # Handle the action
    try:
        if action == "list_entries":
            return await handle_list_entries(client, params)
        elif action == "get_entry":
            return await handle_get_entry(client, params)
        elif action == "create_entry":
            return await handle_create_entry(client, params)
        elif action == "update_entry":
            return await handle_update_entry(client, params)
        elif action == "delete_entry":
            return await handle_delete_entry(client, params)
        elif action == "list_categories":
            return await handle_list_categories(client, params)
        elif action == "get_category":
            return await handle_get_category(client, params)
        elif action == "create_category":
            return await handle_create_category(client, params)
        elif action == "update_category":
            return await handle_update_category(client, params)
        elif action == "delete_category":
            return await handle_delete_category(client, params)
        elif action == "list_channels":
            return await handle_list_channels(client, params)
        elif action == "get_channel":
            return await handle_get_channel(client, params)
        else:
            raise McpError(
                ErrorCode.InvalidParams,
                f"Invalid action: {action}",
            )
    except Exception as e:
        logger.error(f"Error handling EE tool action: {str(e)}")
        if isinstance(e, McpError):
            raise
        raise McpError(
            ErrorCode.InternalError,
            f"Error handling EE tool action: {str(e)}",
        )

async def handle_list_entries(client, params):
    """Handle the list_entries action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the entries
    response = await client.get_entries(params)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_entries_response(response),
            }
        ],
    }

async def handle_get_entry(client, params):
    """Handle the get_entry action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the entry ID
    entry_id = params.get("entry_id")
    if not entry_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: entry_id",
        )
    
    # Get the entry
    response = await client.get_entry(entry_id)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_entry_response(response),
            }
        ],
    }

async def handle_create_entry(client, params):
    """Handle the create_entry action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the entry data
    entry_data = params.get("entry_data")
    if not entry_data:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: entry_data",
        )
    
    # Create the entry
    response = await client.create_entry(entry_data)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Entry created successfully: {response.get('entry_id')}",
            }
        ],
    }

async def handle_update_entry(client, params):
    """Handle the update_entry action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the entry ID and data
    entry_id = params.get("entry_id")
    entry_data = params.get("entry_data")
    if not entry_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: entry_id",
        )
    if not entry_data:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: entry_data",
        )
    
    # Update the entry
    response = await client.update_entry(entry_id, entry_data)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Entry updated successfully: {entry_id}",
            }
        ],
    }

async def handle_delete_entry(client, params):
    """Handle the delete_entry action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the entry ID
    entry_id = params.get("entry_id")
    if not entry_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: entry_id",
        )
    
    # Delete the entry
    response = await client.delete_entry(entry_id)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Entry deleted successfully: {entry_id}",
            }
        ],
    }

async def handle_list_categories(client, params):
    """Handle the list_categories action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the categories
    response = await client.get_categories(params)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_categories_response(response),
            }
        ],
    }

async def handle_get_category(client, params):
    """Handle the get_category action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the category ID
    category_id = params.get("category_id")
    if not category_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: category_id",
        )
    
    # Get the category
    response = await client.get_category(category_id)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_category_response(response),
            }
        ],
    }

async def handle_create_category(client, params):
    """Handle the create_category action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the category data
    category_data = params.get("category_data")
    if not category_data:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: category_data",
        )
    
    # Create the category
    response = await client.create_category(category_data)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Category created successfully: {response.get('category_id')}",
            }
        ],
    }

async def handle_update_category(client, params):
    """Handle the update_category action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the category ID and data
    category_id = params.get("category_id")
    category_data = params.get("category_data")
    if not category_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: category_id",
        )
    if not category_data:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: category_data",
        )
    
    # Update the category
    response = await client.update_category(category_id, category_data)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Category updated successfully: {category_id}",
            }
        ],
    }

async def handle_delete_category(client, params):
    """Handle the delete_category action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the category ID
    category_id = params.get("category_id")
    if not category_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: category_id",
        )
    
    # Delete the category
    response = await client.delete_category(category_id)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": f"Category deleted successfully: {category_id}",
            }
        ],
    }

async def handle_list_channels(client, params):
    """Handle the list_channels action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the channels
    response = await client.get_channels(params)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_channels_response(response),
            }
        ],
    }

async def handle_get_channel(client, params):
    """Handle the get_channel action
    
    Args:
        client (EEClient): The ExpressionEngine API client
        params (dict): The action parameters
    
    Returns:
        dict: The action response
    """
    # Get the channel ID
    channel_id = params.get("channel_id")
    if not channel_id:
        raise McpError(
            ErrorCode.InvalidParams,
            "Missing required parameter: channel_id",
        )
    
    # Get the channel
    response = await client.get_channel(channel_id)
    
    # Format the response
    return {
        "content": [
            {
                "type": "text",
                "text": format_channel_response(response),
            }
        ],
    }

def format_entries_response(response):
    """Format the entries response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the entries
    entries = response.get("entries", [])
    
    # Format the entries
    if not entries:
        return "No entries found."
    
    # Build the formatted response
    formatted = f"Found {len(entries)} entries:\n\n"
    
    for entry in entries:
        formatted += f"Entry ID: {entry.get('entry_id')}\n"
        formatted += f"Title: {entry.get('title')}\n"
        formatted += f"URL Title: {entry.get('url_title')}\n"
        formatted += f"Status: {entry.get('status')}\n"
        formatted += f"Entry Date: {entry.get('entry_date')}\n"
        
        # Add custom fields
        for key, value in entry.items():
            if key not in ["entry_id", "title", "url_title", "status", "entry_date"]:
                formatted += f"{key}: {value}\n"
        
        formatted += "\n"
    
    return formatted

def format_entry_response(response):
    """Format the entry response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the entry
    entry = response.get("entry", {})
    
    # Format the entry
    if not entry:
        return "Entry not found."
    
    # Build the formatted response
    formatted = f"Entry ID: {entry.get('entry_id')}\n"
    formatted += f"Title: {entry.get('title')}\n"
    formatted += f"URL Title: {entry.get('url_title')}\n"
    formatted += f"Status: {entry.get('status')}\n"
    formatted += f"Entry Date: {entry.get('entry_date')}\n"
    
    # Add custom fields
    for key, value in entry.items():
        if key not in ["entry_id", "title", "url_title", "status", "entry_date"]:
            formatted += f"{key}: {value}\n"
    
    return formatted

def format_categories_response(response):
    """Format the categories response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the categories
    categories = response.get("categories", [])
    
    # Format the categories
    if not categories:
        return "No categories found."
    
    # Build the formatted response
    formatted = f"Found {len(categories)} categories:\n\n"
    
    for category in categories:
        formatted += f"Category ID: {category.get('cat_id')}\n"
        formatted += f"Name: {category.get('cat_name')}\n"
        formatted += f"URL Title: {category.get('cat_url_title')}\n"
        formatted += f"Group ID: {category.get('group_id')}\n"
        formatted += f"Parent ID: {category.get('parent_id')}\n"
        
        # Add custom fields
        for key, value in category.items():
            if key not in ["cat_id", "cat_name", "cat_url_title", "group_id", "parent_id"]:
                formatted += f"{key}: {value}\n"
        
        formatted += "\n"
    
    return formatted

def format_category_response(response):
    """Format the category response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the category
    category = response.get("category", {})
    
    # Format the category
    if not category:
        return "Category not found."
    
    # Build the formatted response
    formatted = f"Category ID: {category.get('cat_id')}\n"
    formatted += f"Name: {category.get('cat_name')}\n"
    formatted += f"URL Title: {category.get('cat_url_title')}\n"
    formatted += f"Group ID: {category.get('group_id')}\n"
    formatted += f"Parent ID: {category.get('parent_id')}\n"
    
    # Add custom fields
    for key, value in category.items():
        if key not in ["cat_id", "cat_name", "cat_url_title", "group_id", "parent_id"]:
            formatted += f"{key}: {value}\n"
    
    return formatted

def format_channels_response(response):
    """Format the channels response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the channels
    channels = response.get("channels", [])
    
    # Format the channels
    if not channels:
        return "No channels found."
    
    # Build the formatted response
    formatted = f"Found {len(channels)} channels:\n\n"
    
    for channel in channels:
        formatted += f"Channel ID: {channel.get('channel_id')}\n"
        formatted += f"Name: {channel.get('channel_name')}\n"
        formatted += f"Title: {channel.get('channel_title')}\n"
        formatted += f"URL: {channel.get('channel_url')}\n"
        
        # Add custom fields
        for key, value in channel.items():
            if key not in ["channel_id", "channel_name", "channel_title", "channel_url"]:
                formatted += f"{key}: {value}\n"
        
        formatted += "\n"
    
    return formatted

def format_channel_response(response):
    """Format the channel response
    
    Args:
        response (dict): The API response
    
    Returns:
        str: The formatted response
    """
    # Get the channel
    channel = response.get("channel", {})
    
    # Format the channel
    if not channel:
        return "Channel not found."
    
    # Build the formatted response
    formatted = f"Channel ID: {channel.get('channel_id')}\n"
    formatted += f"Name: {channel.get('channel_name')}\n"
    formatted += f"Title: {channel.get('channel_title')}\n"
    formatted += f"URL: {channel.get('channel_url')}\n"
    
    # Add custom fields
    for key, value in channel.items():
        if key not in ["channel_id", "channel_name", "channel_title", "channel_url"]:
            formatted += f"{key}: {value}\n"
    
    return formatted
