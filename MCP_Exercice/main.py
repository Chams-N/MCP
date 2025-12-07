from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="say_hello")
def say_hello():
    '''A simple function that prints a greeting message.'''
    print("Hello, MCP Environment!")



@mcp.tool()
def say_hello():
    print("Hello from mcp-env!")
    return "Hello, MCP Environment!"

if __name__ == "__main__":
    mcp.run(transport='stdio')  # stdio is for local testing    


#JSON rpc is a protocol that allows for remote procedure calls using JSON as the data format. It enables communication between a client and a server by sending requests and receiving responses in JSON format.

