# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from decimal import Decimal
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import List, Optional, Literal

class LocationModel(BaseModel):
    city: str
    dist: str
    ward: str = None
    street: str = None
    long: Decimal = None
    lat: Decimal = None
    address: str = None
    description: str = None

class AttrModel(BaseModel):
    area: Decimal = None
    total_area: Decimal = None
    width: Decimal = None
    length: Decimal = None
    height: Decimal = None
    total_room: int = None
    bedroom: int = None
    floor: Decimal = None
    direction: str = None
    interior: str = None
    feature: str = None
    type_detail: str = None
    certificate: str = None
    built_year: str = None
    condition: str = None
    site_id: str = None

class AgentModel(BaseModel):
    name: str = None
    agent_type: str = None
    phone_number: str = None
    email: str = None
    address: str = None
    profile: str = None
    

class ProjectModel(BaseModel):
    name: str = None
    profile: str = None

class PropertyCrawlerItem(BaseModel):
    id: str
    title: str
    url: HttpUrl
    site: str
    price: int
    price_currency: str
    images: List[HttpUrl]
    thumbnail: HttpUrl #automatic create thumbnail
    description: str
    property_type: str 
    # property_type: Literal['apartment', 'house', 'land', 'shop']
    publish_at: str = None
    initial_at: str
    update_at: str
    location: LocationModel
    attr: AttrModel
    agent: Optional[AgentModel]
    project: Optional[ProjectModel]


def validate_item(item, is_raw=True):
    '''Validate item

    Args:
        item (dict): Item to validate

    Raises:
        Exception: Validation failed
    '''
    return PropertyCrawlerItem(**item)