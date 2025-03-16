# NearbySearch MCP Server

An MCP server for nearby place searches with IP-based location detection.

![GitHub License](https://img.shields.io/github/license/kukapay/nearby-search-mcp) 
![GitHub Last Commit](https://img.shields.io/github/last-commit/kukapay/nearby-search-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

## Features

- **IP-based Location Detection**: Uses ipapi.co to determine your current location
- **Google Places Integration**: Searches for nearby places based on keywords and optional type filters
- **Simple Interface**: Single tool endpoint with customizable radius

## Requirements

- Python 3.10+
- Google Cloud Platform API Key with Places API enabled
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kukapay/nearby-search-mcp.git
cd nearby-search-mcp
```

2. Install dependencies:
```bash
# Using uv (recommended)
uv add "mcp[cli]" httpx python-dotenv

# Or using pip
pip install mcp httpx python-dotenv
```

3. Client Configuration

```json
{
  "mcpServers": {
    "nearby-search": {
      "command": "uv",
      "args": ["--directory", "path/to/nearby-search-mcp", "run", "main.py"],
      "env": {
        "GOOGLE_API_KEY": "your google api key"
      }
    }
  }
}
````

## Usage

### Running the Server

- **Development Mode** (with MCP Inspector):
```bash
mcp dev main.py
```

- **Install in Claude Desktop**:
```bash
mcp install main.py --name "NearbySearch"
```

- **Direct Execution**:
```bash
python main.py
```

### Available Endpoints

**Tool: `search_nearby`**
 - Searches for places near your current location
 - Parameters:
   - `keyword` (str): What to search for (e.g., "coffee shop")
   - `radius` (int, optional): Search radius in meters (default: 1500)
   - `type` (str, optional): Place type (e.g., "restaurant", "cafe")


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
