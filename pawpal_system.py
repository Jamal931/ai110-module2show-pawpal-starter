from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    needs: Dict[str, str] = field(default_factory=dict)

    def update_needs(self, needs: Dict[str, str]) -> None:
        pass

    def describe_pet(self) -> str:
        pass

    def is_dog(self) -> bool:
        pass

    def is_cat(self) -> bool:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: Optional[str] = None
    deadline: Optional[str] = None
    notes: Optional[str] = None

    def update_duration(self, duration_minutes: int) -> None:
        pass

    def update_priority(self, priority: str) -> None:
        pass

    def summary(self) -> str:
        pass

    def is_required_today(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    preferences: Dict[str, str] = field(default_factory=dict)
    constraints: Dict[str, str] = field(default_factory=dict)

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        pass

    def available_time(self) -> Optional[int]:
        pass

    def describe_owner(self) -> str:
        pass


class Schedule:
    def __init__(self, date: Optional[date] = None, tasks: Optional[List[Task]] = None, explanation: str = ""):
        self.date = date or date.today()
        self.tasks = tasks or []
        self.explanation = explanation

    def add_task(self, task: Task, start_time: Optional[str] = None) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def total_time(self) -> int:
        pass

    def format_display(self) -> str:
        pass

    def explain_plan(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: Optional[List[Task]] = None, time_budget: Optional[int] = None):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks or []
        self.time_budget = time_budget

    def generate_plan(self) -> Schedule:
        pass

    def rank_tasks(self) -> List[Task]:
        pass

    def apply_constraints(self, tasks: List[Task]) -> List[Task]:
        pass

    def build_daily_schedule(self, tasks: List[Task]) -> Schedule:
        pass

    def explain_choice(self, task: Task) -> str:
        pass
