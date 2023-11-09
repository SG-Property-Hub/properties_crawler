import pytz
from datetime import date, datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, validator
from pydantic.networks import HttpUrl

from .site_crawler.mogi import (
    mogi_item, mogi_list)
from .site_crawler.bds68 import (
    bds68_item, bds68_list)
from .site_crawler.muaban import (
    muaban_item, muaban_list)
from .site_crawler.nhatot import (
    nhatot_item, nhatot_list)

class LocationModel(BaseModel):
    city: str
    dist: str
    ward: str = None
    street: str = None
    long: float = None
    lat: float = None
    address: str = None
    description: str = None

class AttrModel(BaseModel):
    area: float = None
    total_area: float = None
    width: float = None
    length: float = None
    height: float = None
    total_room: int = None
    bedroom: int = None
    bathroom: int = None
    floor: float = None
    direction: str = None
    interior: str = None
    feature: str = None
    type_detail: str = None
    certificate: str = None
    built_year: int = None
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
    price: int = None
    price_currency: str = 'VND'
    price_string: str
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
    project: ProjectModel = None


def validate_item(item, is_raw=True):
    '''Validate item

    Args:
        item (dict): Item to validate

    Raises:
        Exception: Validation failed
    '''
    return PropertyCrawlerItem(**item)


crawler = {
    'mogi': {
        'list': mogi_list,
        'item': mogi_item,
    },
    'bds68':{
        'list': bds68_list,
        'item': bds68_item,
    },
    'muaban':{
        'list': muaban_list,
        'item': muaban_item,
    },
    'nhatot':{
        'list': nhatot_list,
        'item': nhatot_item,
    }
}
