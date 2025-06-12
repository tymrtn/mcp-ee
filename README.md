# ExpressionEngine MCP Server

This is a Model Context Protocol (MCP) server for interacting with an ExpressionEngine site through the Reinos Webservice API. It allows AI assistants like Claude to manage ExpressionEngine content.

## Features

- **Connect to a single ExpressionEngine site** via Reinos Webservice.
- **Search, view, create, and update entries**.
- **Secure authentication** using a shortkey.
- **Graceful error handling** for common server issues like memory limits and "no results" responses.
- **Detailed logging** for all operations.

## Requirements

- Python 3.9 or higher
- An active ExpressionEngine installation
- The [Reinos Webservice](https://addons.reinos.nl/webservice) add-on for ExpressionEngine

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/tymrtn/mcp-ee.git
    cd ee-mcp
    ```

2.  Create a virtual environment and install the dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -e .
    ```

3.  Set up your configuration by copying the example environment file:
    ```bash
    cp env.example .env
    ```
    Then, edit the `.env` file with your ExpressionEngine site details.

## Configuration

The MCP server is configured using a simple `.env` file:

```dotenv
# ExpressionEngine site API URL (e.g., https://your-site.com)
API_URL=https://your-site.com

# ExpressionEngine shortkey for Reinos Webservice authentication
SHORTKEY=your-shortkey-here
```

Each MCP server instance connects to a single ExpressionEngine site. To manage multiple sites, you can run multiple MCP server instances, each with its own `.env` configuration.

## Available Tool: `manage_content`

The MCP server provides a single tool, `manage_content`, which supports the following actions for entry management:

-   `search_entries`: Search for entries with various filters.
-   `get_entry`: Get a specific entry by its ID.
-   `create_entry`: Create a new entry.
-   `update_entry`: Update an existing entry.

### Parameters

The `params` argument is a dictionary containing the data for the action. Key parameters include:
-   `site_id`: The ID of the site (usually `1`).
-   `channel_name`: The short name of the channel (e.g., `blog`, `news`).
-   `entry_id`: The ID of the entry to get or update.
-   `title`: The title of the entry.
-   `status`: The status of the entry (e.g., `open`, `closed`, `Draft`).
-   Other custom field names (e.g., `body`, `summary`, `title2`).

## Example Usage

Here are some examples of how to use the `manage_content` tool:

### Search Entries

```python
# Search for the 5 most recent entries in the 'home' channel
manage_content(
    action="search_entries",
    params={
        "site_id": 1,
        "channel_name": "home",
        "title": "starting",
        "limit": 5
    }
)
```

### Get a Specific Entry

```python
manage_content(
    action="get_entry",
    params={
        "entry_id": 655,
        "site_id": 1
    }
)
```

### Create a New Entry

```python
manage_content(
    action="create_entry",
    params={
        "site_id": 1,
        "channel_name": "home",
        "title": "New Blog Post via MCP",
        "status": "open",
        "summary": "This is a summary.",
        "body": "This is the main body content of the post."
    }
)
```

### Update an Existing Entry

```python
manage_content(
    action="update_entry",
    params={
        "entry_id": 655,
        "site_id": 1,
        "title": "Updated Title for an Existing Entry",
        "status": "Draft"
    }
)
```

## Error Handling

The server is designed to handle common API and server errors gracefully:

-   **Memory Exhaustion**: If a search query is too broad and exhausts server memory, the server returns a helpful error message with suggestions on how to narrow the search scope.
-   **No Results**: If a search yields no results, the server provides a clear message with tips for modifying the search criteria.
-   **Invalid Parameters**: The server validates required parameters for actions like `create_entry` and returns specific error messages if they are missing.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
