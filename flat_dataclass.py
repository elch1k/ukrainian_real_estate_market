from dataclasses import dataclass
from typing import Optional


@dataclass
class ApartmentInfo:
    price: Optional[float] = None
    currency: Optional[str] = None
    city: Optional[str] = None
    main_area: Optional[str] = None
    second_area: Optional[str] = None
    street_name: Optional[str] = None
    subway: bool = False
    total_square: Optional[float] = None
    kitchen_square: Optional[float] = None
    living_square: Optional[float] = None
    room: Optional[int] = None
    total_floor: Optional[int] = None
    flat_floor: Optional[int] = None
    deal_type: Optional[str] = None
    checked_apartment: Optional[bool] = None
    newbuild_name: Optional[str] = None
    animal: bool = False
    photo_count: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    agency_name: Optional[str] = None
    parse_date: Optional[str] = None
    publication_date: Optional[str] = None
    url: Optional[str] = None
    is_active: bool = True
    no_active_date: Optional[str] = None