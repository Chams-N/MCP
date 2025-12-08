from fastmcp import FastMCP

mcp = FastMCP(
    name="MyCalculator"
)

# Define calculator operations as tools
@mcp.tool()
# Adds two numbers and returns the result.
def add(a: float, b: float) -> float:
    return a + b

@mcp.tool()
# Subtracts b from a and returns the result.
def subtract(a: float, b: float) -> float:
    """Subtracts b from a and returns the result."""
    return a - b

@mcp.tool()
# Multiplies two numbers and returns the result.
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers and returns the result."""
    return a * b

@mcp.tool()
# Divides a by b and returns the result.
def divide(a: float, b: float) -> float:
    """Divides a by b and returns the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")
