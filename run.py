#!/usr/bin/env python3
"""
Run script for ExpressionEngine MCP Server

This script runs the ExpressionEngine MCP Server.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import and run the server
if __name__ == "__main__":
    from main import mcp
    mcp.run(transport="stdio")
