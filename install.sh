#!/bin/bash
# Installation script for ExpressionEngine MCP Server

# Check if Python 3.10 or higher is installed
python3 --version | grep -q "Python 3.1[0-9]"
if [ $? -ne 0 ]; then
    echo "Python 3.10 or higher is required. Please install Python 3.10 or higher."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for this session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if ! command -v uv &> /dev/null; then
        echo "Failed to install uv. Please install it manually: https://github.com/astral-sh/uv"
        exit 1
    fi
fi

# Create a virtual environment
echo "Creating virtual environment..."
uv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

# Make run.py executable
echo "Making run.py executable..."
chmod +x run.py
if [ $? -ne 0 ]; then
    echo "Failed to make run.py executable."
    exit 1
fi

# Create a .env file
echo "Creating .env file..."
if [ ! -f .env ]; then
    echo "# Environment variables for ExpressionEngine MCP Server" > .env
    echo "" >> .env
    echo "# Multiple ExpressionEngine sites configuration using JSON format" >> .env
    echo "" >> .env
    echo "# Production site" >> .env
    echo "SITE_PRODUCTION={\"api_url\": \"https://www.bmi.com\", \"api_key\": \"your-production-api-key\"}" >> .env
    echo "" >> .env
    echo "# Development site" >> .env
    echo "SITE_DEVELOPMENT={\"api_url\": \"http://awards.ddev.site\", \"api_key\": \"your-dev-api-key\"}" >> .env
    echo "" >> .env
    echo "# UAT site" >> .env
    echo "SITE_UAT={\"api_url\": \"https://uat.bmi.com\", \"api_key\": \"your-uat-api-key\"}" >> .env
    echo "" >> .env
    echo "# Default site to use (must match one of the site names above)" >> .env
    echo "DEFAULT_SITE=DEVELOPMENT" >> .env
    echo "Created .env file. Please update it with your API keys."
else
    echo ".env file already exists."
fi

echo "Installation complete!"
echo "To run the MCP server, activate the virtual environment and run ./run.py:"
echo "source venv/bin/activate"
echo "./run.py"
echo ""
echo "To use the MCP server with Claude Desktop, copy the claude_desktop_config.json file to your Claude Desktop configuration directory and update it with your site configurations."
echo ""
echo "Multi-site Configuration:"
echo "The MCP server now supports multiple ExpressionEngine sites. You can configure them in the .env file."
echo "Each site is defined with a JSON object containing api_url and api_key properties."
echo "The environment variable name format is SITE_NAME, where NAME is the unique identifier for the site."
echo "You can specify which site to use for each command, or set a default site in the DEFAULT_SITE variable."
