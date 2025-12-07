import requests
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://openlibrary.org"

#MCP server global instance
mcp = FastMCP(name="Library Assistant")
@mcp.tool()
def search_books(query: str) -> list: 

    response = requests.get( 
        f"{BASE_URL}/search.json", 
        params={"q": query}, 
        timeout=10 
    ) 
 
    if response.status_code != 200: 
        return {"error": f"API Error {response.status_code}"} 
 
    data = response.json() 
 
    books = data.get("docs", [])[:10]  # limit to first 10 results 
 
    return [ 
        { 
            "title": b.get("title"), 
            "author": b.get("author_name", ["Unknown"])[0], 
            "year": b.get("first_publish_year"), 
            "work_id": b.get("key")  # e.g. "/works/OL82563W" 
        } 
        for b in books 
    ] 
 
 
@mcp.tool() 
def get_book_details(work_id: str) -> dict: 
    """ 
    Retrieve details about a specific book using its work ID. 
    Example work_id: /works/OL82563W 
    """ 
 
    # Normalize input 
    if not work_id.startswith("/works/"): 
        work_id = f"/works/{work_id}" 
 
    response = requests.get(f"{BASE_URL}{work_id}.json", timeout=10) 
 
    if response.status_code == 404: 
        return {"error": "Book not found"} 
 
    if response.status_code != 200: 
        return {"error": f"API Error {response.status_code}"} 
 
    return response.json() 
 
if __name__ == "__main__": 
    mcp.run(transport="stdio") 