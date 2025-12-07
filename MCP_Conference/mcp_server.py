import os
#bibliotheque standard pour interragir avec le systeme d'exploitation, utilisé pour gérer les varibles d'environnement
import django 
from fastmcp import FastMCP  
# Importation de la classe FastMCP depuis le module fastmcp, utilisée pour créer un serveur MCP rapide. 
from asgiref.sync import sync_to_async 
# Importation de sync_to_async pour convertir des fonctions synchrones en asynchrones, compatible avec les ORM Django. 
# Initialize Django environment 
import sys

sys.path.append(os.path.dirname(os.path.abspath(r"C:\Users\chams\OneDrive\Desktop\PYTHON\Django_env\workshop\workshop")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workshop.settings") 
django.setup() 
 
# Importation des modèles Django après initialisation pour éviter des erreurs de configuration. 
from ConferenceApp.models import Conference 
from SessionApp.models import Session 
 
# Create an MCP server 
mcp = FastMCP("Conference Assistant") 
# Lancement  
 
 #TOOLS
 
 #List all conferences
@mcp.tool()

async def list_conferences() -> str:
    """List all available conferences."""

    @sync_to_async
    def _get():
        return list(Conference.objects.all())

    conferences = await _get()

    if not conferences:
        return "No conferences found."

    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

#get details of a conference by name
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get a conference by name (case-insensitive)."""

    @sync_to_async
    def _get():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
        except Conference.DoesNotExist:
            return None

    conference = await _get()

    if conference == "MULTIPLE":
        return f"Multiple conferences match '{name}'. Please be more specific."

    if conference is None:
        return f"No conference found with name '{name}'."

    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

#Listing Sessions of a Conference
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions of a conference."""

    @sync_to_async
    def _get():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()), conf
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
        except Conference.DoesNotExist:
            return None, None

    sessions, conference = await _get()

    if sessions == "MULTIPLE":
        return f"Multiple conferences found with '{conference_name}'."

    if conference is None:
        return f"Conference '{conference_name}' not found."

    if not sessions:
        return f"No sessions for conference '{conference.name}'."

    return "\n".join([
        f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n  Topic: {s.topic}"
        for s in sessions
    ])

#Filter conferences by theme
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme (exact or partial)."""

    @sync_to_async
    def _get():
        return list(Conference.objects.filter(theme__icontains=theme))

    results = await _get()

    if not results:
        return f"No conferences found with theme '{theme}'."

    return "\n".join([f"- {c.name} ({c.location})" for c in results])

#Run Server
if __name__ == "__main__":  
    mcp.run(transport="stdio")