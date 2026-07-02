from pydantic import BaseModel, Field, field_validator
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
    max_drones: int = Field(gt=0, default=1)
    color: Optional[str] = None
    role: Zone_Role = Zone_Role.hub

    @field_validator('name')
    def name_val(cls, name: str) -> str:
        if '-' in name or ' ' in name:
            raise ValueError('The name of the zone cannot contain a dash "-"')
        return name

    @field_validator('color')
    def color_val(cls, color: str) -> str:
        if not color.replace('_', '').isalpha():
            raise ValueError('The color of the zone can only contain letters.')
        return color


class Connection(BaseModel):
    connection: Tuple[str, str]
    max_link_capacity: int = Field(gt=0, default=1)

    @field_validator('connection')
    def val(cls, connection: Tuple[str, str]) -> Tuple[str, str]:
        if connection[0] == connection[1]:
            raise ValueError("The connected zones must not be identical.")
        return connection
