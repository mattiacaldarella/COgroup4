"""
Represents a problem to solve
a class which is read from the text file
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Tool:
    id: int
    size: int
    number_available: int
    cost: int

@dataclass
class Request:
    id: int
    location_id: int
    first_day: int
    last_day: int
    days_needed: int
    tool_kind_id: int
    tools_needed: int

@dataclass
class ProblemData:
    """The data for the problem to solve"""

    data_set: str
    name: str
    days: int
    capacity: int
    max_trip_distance: int
    depot_coordinate: int
    vehicle_cost: int
    vehicle_day_cost: int
    distance_cost: int
    number_of_tool_types: int
    tools: List[Tool]
    coordinates: List[List[int]]
    requests: List[Request]
