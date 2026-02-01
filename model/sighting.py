import datetime
from dataclasses import dataclass
from datetime import datetime
@dataclass
class Sighting:
    id : int
    s_datetime : datetime
    city: str
    state : str
    country : str
    shape : str
    duration : int
    duration_hm : str
    comments : str
    date_posted : datetime
    latitude : float
    longitude : float