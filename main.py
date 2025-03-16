from mcp.server.fastmcp import FastMCP
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create MCP server
mcp = FastMCP("NearbySearch")

async def get_current_location() -> Dict[str, Any]:
    """Get current location based on IP using ipapi.co"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://ipapi.co/json/")
            response.raise_for_status()
            data = response.json()
            return {
                "latitude": float(data["latitude"]),
                "longitude": float(data["longitude"]),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country_name")
            }
        except Exception as e:
            return {"error": str(e)}

# Tool to search nearby places
@mcp.tool()
async def search_nearby(
    keyword: str,
    radius: int = 1500,
    type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for nearby places using Google Places API based on current IP location.

    Args:
        keyword (str): The search term to look for (e.g., "coffee shop", "restaurant")
        radius (int, optional): Search radius in meters. Defaults to 1500
        type (str, optional): Specific type of place (e.g., "restaurant", "cafe"). See Google Places API docs for valid types

    Returns:
        Dict containing search results with place details
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY environment variable is required"}

    # Get current location
    location_data = await get_current_location()
    if "error" in location_data:
        return location_data
    
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    async with httpx.AsyncClient() as client:
        # Build Google Places Nearby Search URL
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": api_key,
        }
        if keyword:
            params["keyword"] = keyword
        if type:
            params["type"] = type
        
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                return {"error": data.get("status"), "message": data.get("error_message")}
            
            # Process and simplify results
            results = [
                {
                    "name": place["name"],
                    "address": place.get("vicinity"),
                    "location": place["geometry"]["location"],
                    "rating": place.get("rating"),
                    "types": place.get("types", [])
                }
                for place in data.get("results", [])
            ]
            return {
                "results": results,
                "count": len(results),
                "location": {"latitude": latitude, "longitude": longitude}
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    #mcp.run()
    import asyncio
    print(asyncio.run(search_nearby("restaurant")))