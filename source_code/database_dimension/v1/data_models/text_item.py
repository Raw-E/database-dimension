"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for text_item.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports

# Third-Party Imports
from pydantic import BaseModel, Field

# Local Development Imports
from foundation.v1 import CustomLogger

# Current Project Imports

# Type Variables

# Type Aliases

# Constants

# Configuration
logger = CustomLogger(log_level="INFO")

# Helper Functions

# Main Functions


# Classes
class TextItem(BaseModel):
    content: str = Field(..., description="The content of the text item.")


# Exception Classes
