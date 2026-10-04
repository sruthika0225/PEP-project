from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    alarm_date: str
    alarm_time: str
    repeat: str
    status: str
