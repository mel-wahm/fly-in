from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Tuple
from enum import Enum


class Zone_Type(Enum):
    normal = 'normal'
    blocked = 'blocked'
    priority = 'priority'
    restricted = 'restricted'


class Zone_Role(Enum):
    start_hub = 'start_hub'
    end_hub = 'end_hub'
    hub = 'hub'


class Zone(BaseModel):
    name: str
    coordinates: Tuple[int, int]
    zone: Zone_Type = Zone_Type.normal
    max_drones: int = Field(ge=1, default=1)
    color : Optional[str] = None
    role : Zone_Role = Zone_Role.hub


    @field_validator('name')
    def val(cls, name):
        if '-' in name or ' ' in name:
            raise ValueError('Tha name of the zone cannot contain a dash "-"')
        return name

class Connection(BaseModel):
    connection: Tuple[str, str]
    max_link_capacity: int = Field(gt=0, default=1)

    @field_validator('connection')
    def val(cls, connection):
        if len(connection) != 2:
            raise ValueError("There should be exactly two zones in each connection.")
        if connection[0] == connection[1]:
            raise ValueError("The connected zones must not be identical.")
        return connection
