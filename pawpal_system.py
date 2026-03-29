from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: Optional[str] = None
    frequency: Optional[str] = None
    deadline: Optional[str] = None
    due_date: Optional[date] = None
    start_time: Optional[str] = None
    notes: Optional[str] = None
    completed: bool = False
    pet: Optional["Pet"] = None
    owner: Optional["Owner"] = None

    def update_duration(self, duration_minutes: int) -> None:
        """Set the task duration in minutes."""
        self.duration_minutes = duration_minutes

    def update_priority(self, priority: str) -> None:
        """Set the task priority level."""
        self.priority = priority

    def summary(self) -> str:
        """Return a one-line description of the task."""
        status = "completed" if self.completed else "pending"
        frequency = f"/{self.frequency}" if self.frequency else ""
        time_text = f" at {self.start_time}" if self.start_time else ""
        due_text = f" due {self.due_date.isoformat()}" if self.due_date else ""
        return f"{self.title} ({self.duration_minutes}m){frequency}{time_text}{due_text} [{self.priority}] - {status}"

    def is_required_today(self) -> bool:
        """Return whether the task still needs to be done today."""
        if self.completed:
            return False
        if self.due_date and self.due_date > date.today():
            return False
        return True

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and repeat if recurring."""
        self.completed = True
        if self.frequency not in {"daily", "weekly"}:
            return None

        interval = timedelta(days=1 if self.frequency == "daily" else 7)
        new_due_date = (self.due_date or date.today()) + interval
        repeated = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            deadline=self.deadline,
            due_date=new_due_date,
            start_time=self.start_time,
            notes=self.notes,
            completed=False,
            pet=self.pet,
            owner=self.owner,
        )
        if self.pet:
            self.pet.add_task(repeated)
        return repeated

    def assign(self, owner: "Owner", pet: "Pet") -> None:
        """Link the task to an owner and a pet."""
        self.owner = owner
        self.pet = pet


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    needs: Dict[str, str] = field(default_factory=dict)
    tasks: List[Task] = field(default_factory=list)

    def update_needs(self, needs: Dict[str, str]) -> None:
        """Update the pet's care needs."""
        self.needs.update(needs)

    def describe_pet(self) -> str:
        """Return a short description of the pet."""
        age_text = f", age {self.age}" if self.age is not None else ""
        return f"{self.name} the {self.species}{age_text}"

    def is_dog(self) -> bool:
        """Return True if the pet is a dog."""
        return self.species.lower() == "dog"

    def is_cat(self) -> bool:
        """Return True if the pet is a cat."""
        return self.species.lower() == "cat"

    def add_task(self, task: Task) -> None:
        """Assign a task to this pet."""
        task.pet = self
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def total_task_time(self) -> int:
        """Return the total duration of all assigned tasks."""
        return sum(task.duration_minutes for task in self.tasks)


@dataclass
class Owner:
    name: str
    preferences: Dict[str, str] = field(default_factory=dict)
    constraints: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        """Update the owner's preferences."""
        self.preferences.update(preferences)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's care."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's care."""
        if pet in self.pets:
            self.pets.remove(pet)

    def available_time(self) -> Optional[int]:
        """Return the owner's available scheduling time in minutes."""
        if "available_minutes" in self.constraints:
            try:
                return int(self.constraints["available_minutes"])
            except (TypeError, ValueError):
                return None
        return None

    def all_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def describe_owner(self) -> str:
        """Return a short description of the owner."""
        pet_names = ", ".join(pet.name for pet in self.pets) or "no pets"
        return f"{self.name} cares for {pet_names}."


class Schedule:
    """A daily plan of pet care tasks for one owner and one pet."""

    def __init__(
        self,
        date: Optional[date] = None,
        tasks: Optional[List[Task]] = None,
        explanation: str = "",
        owner: Optional[Owner] = None,
        pet: Optional[Pet] = None,
    ):
        self.date = date or date.today()
        self.tasks = tasks or []
        self.explanation = explanation
        self.owner = owner
        self.pet = pet

    def add_task(self, task: Task, start_time: Optional[str] = None) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        if task in self.tasks:
            self.tasks.remove(task)

    def total_time(self) -> int:
        """Return the total scheduled duration."""
        return sum(task.duration_minutes for task in self.tasks)

    def format_display(self) -> str:
        """Return a readable text version of the schedule."""
        header = f"Schedule for {self.date.isoformat()}"
        if self.pet:
            header += f" - {self.pet.name}"
        lines = [header, "" if self.tasks else "No tasks scheduled."]
        for task in self.tasks:
            lines.append(task.summary())
        return "\n".join(lines)

    def explain_plan(self) -> str:
        """Return the explanation for the selected schedule."""
        if self.explanation:
            return self.explanation
        if not self.tasks:
            return "No tasks selected for today."
        return "This plan includes the highest-priority incomplete tasks that fit the available time."


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        pet: Optional[Pet] = None,
        tasks: Optional[List[Task]] = None,
        time_budget: Optional[int] = None,
    ):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks or []
        self.time_budget = time_budget

    def get_source_tasks(self) -> List[Task]:
        """Return the current set of tasks to schedule."""
        if self.tasks:
            return self.tasks
        if self.pet:
            return [task for task in self.pet.tasks]
        return self.owner.all_tasks()

    def generate_plan(self) -> Schedule:
        """Create a daily schedule for available tasks."""
        source_tasks = [task for task in self.get_source_tasks() if task.is_required_today()]
        filtered_tasks = self.filter_tasks(source_tasks, status="pending")
        ranked_tasks = self.rank_tasks(filtered_tasks)
        selected_tasks = self.apply_constraints(ranked_tasks)
        scheduled = self.build_daily_schedule(selected_tasks)
        return scheduled

    def _time_key(self, start_time: Optional[str]) -> int:
        if not start_time:
            return 24 * 60
        try:
            hour, minute = map(int, start_time.split(":"))
            return hour * 60 + minute
        except ValueError:
            return 24 * 60

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by their scheduled start time."""
        tasks = tasks if tasks is not None else self.get_source_tasks()
        return sorted(tasks, key=lambda task: self._time_key(task.start_time))

    def filter_tasks(
        self,
        tasks: Optional[List[Task]] = None,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks matching completion status and/or pet name."""
        tasks = tasks if tasks is not None else self.get_source_tasks()
        if status:
            status = status.lower()
            if status == "completed":
                tasks = [task for task in tasks if task.completed]
            elif status == "pending":
                tasks = [task for task in tasks if not task.completed]
        if pet_name:
            tasks = [task for task in tasks if task.pet and task.pet.name == pet_name]
        return tasks

    def rank_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by priority and duration."""
        tasks = tasks if tasks is not None else self.get_source_tasks()
        priority_values = {"high": 3, "medium": 2, "low": 1}

        def task_rank(task: Task) -> tuple:
            priority_score = priority_values.get(task.priority.lower(), 0)
            return (-priority_score, task.duration_minutes)

        return sorted(tasks, key=task_rank)

    def apply_constraints(self, tasks: List[Task]) -> List[Task]:
        """Filter tasks to fit within the time budget."""
        if self.time_budget is None:
            return tasks
        selected: List[Task] = []
        total = 0
        for task in tasks:
            if total + task.duration_minutes <= self.time_budget:
                selected.append(task)
                total += task.duration_minutes
        return selected

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return a list of warnings for tasks that share the same start time."""
        tasks = tasks if tasks is not None else self.get_source_tasks()
        conflicts: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.start_time:
                conflicts.setdefault(task.start_time, []).append(task)

        warnings: List[str] = []
        for start_time, grouped in conflicts.items():
            if len(grouped) > 1:
                pets = ", ".join(task.pet.name if task.pet else "unknown" for task in grouped)
                warnings.append(
                    f"Conflict at {start_time}: {len(grouped)} tasks scheduled ({pets})."
                )
        return warnings

    def build_daily_schedule(self, tasks: List[Task]) -> Schedule:
        """Build the final Schedule object from selected tasks."""
        explanation = "Selected tasks based on priority and available time."
        active_pet = self.pet
        if not active_pet and self.owner.pets:
            active_pet = self.owner.pets[0]
        sorted_tasks = self.sort_by_time(tasks)
        return Schedule(
            date=date.today(),
            tasks=sorted_tasks,
            explanation=explanation,
            owner=self.owner,
            pet=active_pet,
        )

    def explain_choice(self, task: Task) -> str:
        """Explain why a task was chosen for the schedule."""
        if task.completed:
            return f"{task.title} is already completed."
        reason = f"{task.title} was chosen because it is {task.priority} priority."
        if task.pet:
            reason += f" It belongs to {task.pet.name}."
        return reason
