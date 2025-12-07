from mcp.server.fastmcp import FastMCP
import os
import json
from datetime import datetime
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

mcp = FastMCP(name="Aéroport Info")

def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

# RESOURCE
@mcp.resource("flights://today")
def flights_resource():
    """Expose the JSON file as a resource"""
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

# TOOL: Find a flight by number
@mcp.tool()
def find_flight(flight_number: str) -> str:
    flights = _load_flights()
    for f in flights:
        if f["flight_number"].lower() == flight_number.lower():
            return (
                f"✈️ {f['flight_number']} — {f['departure_city']} → {f['arrival_city']}\n"
                f"Airline: {f['airline']}\n"
                f"Status: {f['status']}"
            )
    return "Flight not found."

# TOOL: Filter by destination
@mcp.tool()
def flights_to(destination: str) -> str:
    flights = _load_flights()
    matches = [f for f in flights if destination.lower() in f["arrival_city"].lower()]
    if not matches:
        return f"No flights to {destination}."
    
    result = f"Flights to {destination}:\n"
    for f in matches:
        result += f"- {f['flight_number']} at {f['arrival_time']} ({f['status']})\n"
    return result

# TOOL: Filter by status
@mcp.tool()
def flights_by_status(status: str) -> str:
    flights = _load_flights()
    matches = [f for f in flights if f["status"].lower() == status.lower()]
    if not matches:
        return f"No flights with status '{status}'."

    result = f"Flights with status {status}:\n"
    for f in matches:
        result += f"- {f['flight_number']} ({f['airline']})\n"
    return result

# TOOL+:( count flights)
# TOOL: Next flight after a given time
@mcp.tool()
def next_flight_after(airport_code: str, time_str: str) -> str:
    """
    Returns the next flight departing from an airport after a given time (HH:MM).
    Example: next_flight_after("CDG", "15:00")
    """
    flights = _load_flights()

    # Parse the user-provided time
    try:
        user_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return "Invalid time format. Use HH:MM."

    # Filter flights leaving this airport
    matches = [
        f for f in flights
        if f["departure"].lower() == airport_code.lower()
    ]

    if not matches:
        return f"No flights departing from {airport_code}."

    # Convert flights to comparable (time, flight) pairs
    future_flights = []
    for f in matches:
        flight_time = datetime.strptime(f["departure_time"], "%H:%M").time()
        if flight_time > user_time:
            future_flights.append((flight_time, f))

    if not future_flights:
        return f"No flights after {time_str} from {airport_code}."

    # Sort flights by time
    future_flights.sort(key=lambda x: x[0])

    # Select the earliest
    _, f = future_flights[0]

    return (
        f"Next flight after {time_str} from {airport_code}:\n"
        f"✈️ {f['flight_number']} — {f['departure_city']} → {f['arrival_city']}\n"
        f"Time: {f['departure_time']}\n"
        f"Airline: {f['airline']}\n"
        f"Status: {f['status']}"
    )
# RUN
if __name__ == "__main__":
    mcp.run(transport="stdio")
