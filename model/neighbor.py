from dataclasses import dataclass

@dataclass
class Neighbor:
    state1 : str
    state2 : str
    total_sightings : int

    def __str__(self):
        return f'{self.state1} - {self.state2} - {self.total_sightings}'