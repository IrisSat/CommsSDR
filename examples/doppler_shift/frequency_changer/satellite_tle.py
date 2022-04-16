"""
Data class definition for TLE
"""
from dataclasses import dataclass


@dataclass
class SatelliteTLE:
    """
    Class containing the TLE definition for doppler calculations
    """
    name: str
    tle1: str
    tle2: str
    frequency: float
