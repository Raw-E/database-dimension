# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for quality_comparison.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
from typing import Optional

# Local Development Imports
from foundation.v1 import CustomLogger

# Third-Party Imports
from pydantic import BaseModel, Field

# Configuration
logger = CustomLogger(log_level="INFO")


# Classes
class QualityRating(BaseModel):
    # Class Attributes
    benchmark_id: Optional[str] = Field(
        None, description="The ID of the thing being used as the comparison benchmark."
    )


class RatioRating(QualityRating):
    # Class Attributes
    subject_to_benchmark_ratio: float = Field(
        ...,
        gt=0,
        description="Ratio of subject quality to benchmark quality (values > 1 indicate higher quality than benchmark).",
    )


class OneToTenRating(QualityRating):
    # Class Attributes
    value: float = Field(
        ..., ge=1, le=10, description="Quality rating on a scale of 1 to 10"
    )
