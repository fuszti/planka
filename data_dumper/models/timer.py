from dataclasses import dataclass


@dataclass
class Timer:
    total_seconds: int

    @property
    def hours(self):
        return self.total_seconds // 60 // 60
    
    @property
    def minutes(self):
        return (self.total_seconds % (60 * 60) // 60)
    
    @property
    def seconds(self):
        return self.total_seconds % 60