from dataclasses import dataclass

@dataclass
class State:
    id : str
    name : str
    capital : str
    lat : float
    lng : float
    area : float
    population : float
    neighbors  : str

    def __str__(self):
        return f'{self.id}, {self.name}'