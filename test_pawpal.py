from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete():
    task = Task(
        title="Test task",
        duration_minutes=10,
        priority="low",
        category="testing",
    )

    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_pet_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog", age=3)
    task = Task(
        title="Play time",
        duration_minutes=20,
        priority="medium",
        category="enrichment",
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_sort_by_time_orders_tasks_chronologically():
    pet = Pet(name="Buddy", species="dog")
    task_early = Task(title="Early", duration_minutes=10, priority="low", start_time="08:00")
    task_late = Task(title="Late", duration_minutes=10, priority="low", start_time="14:30")
    task_middle = Task(title="Middle", duration_minutes=10, priority="low", start_time="11:15")

    pet.add_task(task_middle)
    pet.add_task(task_late)
    pet.add_task(task_early)

    scheduler = Scheduler(owner=Owner(name="Jordan"), pet=pet)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    assert [task.title for task in sorted_tasks] == ["Early", "Middle", "Late"]


def test_daily_task_recurs_when_completed():
    owner = Owner(name="Jordan")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    task = Task(
        title="Daily walk",
        duration_minutes=20,
        priority="high",
        category="walk",
        frequency="daily",
        start_time="09:00",
        due_date=date.today(),
    )
    task.assign(owner, pet)
    pet.add_task(task)

    repeated = task.mark_complete()

    assert task.completed
    assert repeated is not None
    assert repeated.frequency == "daily"
    assert repeated.due_date == date.today() + timedelta(days=1)
    assert repeated in pet.tasks


def test_detect_conflicts_returns_warning_for_duplicate_start_times():
    owner = Owner(name="Jordan")
    pet_a = Pet(name="Mochi", species="dog")
    pet_b = Pet(name="Whiskers", species="cat")
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)

    task_a = Task(title="Walk", duration_minutes=30, priority="high", start_time="09:00")
    task_b = Task(title="Brushing", duration_minutes=15, priority="medium", start_time="09:00")
    task_a.assign(owner, pet_a)
    task_b.assign(owner, pet_b)
    pet_a.add_task(task_a)
    pet_b.add_task(task_b)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts([task_a, task_b])

    assert len(warnings) == 1
    assert "Conflict at 09:00" in warnings[0]
    assert "Mochi" in warnings[0] and "Whiskers" in warnings[0]
