"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for time_range.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
from datetime import datetime
from enum import Enum
from typing import Union

# Third-Party Imports
from pydantic import BaseModel

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
class TimeState(str, Enum):
    UNKNOWN = "UNKNOWN"


class TimeRange(BaseModel):
    start_time: Union[datetime, TimeState] = TimeState.UNKNOWN
    end_time: datetime


# Exception Classes
