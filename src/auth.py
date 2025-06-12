"""
Authentication module for ExpressionEngine MCP Server

This module handles authentication for the Reinos Webservice API.
"""

import logging

logger = logging.getLogger("ee_mcp.auth")

class EEAuth:
    """Authentication handler for ExpressionEngine API"""
    
    def __init__(self, shortkey):
        """Initialize the authentication handler
        
        Args:
            shortkey (str): The shortkey for Reinos Webservice authentication
        """
        self.shortkey = shortkey
    
    def get_auth_params(self):
        """Get authentication parameters for the API request
        
        Returns:
            dict: The authentication parameters
        """
        return {
            "auth[shortkey]": self.shortkey
        }
    
    def get_auth_headers(self):
        """Get authentication headers for the API request
        
        Returns:
            dict: The authentication headers
        """
        return {
            "Content-Type": "application/x-www-form-urlencoded"
        }
