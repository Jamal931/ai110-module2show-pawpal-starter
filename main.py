from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Jordan", constraints={"available_minutes": "90"})

    mochi = Pet(name="Mochi", species="dog", age=4)
    whiskers = Pet(name="Whiskers", species="cat", age=2)

    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    task1 = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        frequency="daily",
        start_time="09:00",
        notes="Take Mochi for a walk around the block.",
    )
    task1.assign(owner, mochi)
    mochi.add_task(task1)

    task2 = Task(
        title="Feed breakfast",
        duration_minutes=15,
        priority="medium",
        category="feeding",
        frequency="daily",
        start_time="08:30",
        notes="Feed both pets their morning meal.",
    )
    task2.assign(owner, whiskers)
    whiskers.add_task(task2)

    task3 = Task(
        title="Grooming",
        duration_minutes=40,
        priority="low",
        category="grooming",
        frequency="weekly",
        start_time="09:00",
        notes="Brush Whiskers and check claws.",
    )
    task3.assign(owner, whiskers)
    whiskers.add_task(task3)

    print("Tasks before sorting:")
    for task in owner.all_tasks():
        print(" -", task.summary())

    scheduler = Scheduler(owner=owner, time_budget=90)
    sorted_tasks = scheduler.sort_by_time(owner.all_tasks())
    print("\nTasks after sorting by start time:")
    for task in sorted_tasks:
        print(" -", task.summary())

    filtered_tasks = scheduler.filter_tasks(status="pending", pet_name="Whiskers")
    print("\nPending tasks for Whiskers:")
    for task in filtered_tasks:
        print(" -", task.summary())

    schedule = scheduler.generate_plan()
    warnings = scheduler.detect_conflicts(schedule.tasks)

    print("\nToday's Schedule")
    print("=================")
    print(schedule.format_display())

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(" -", warning)

    print("\nCompleting the daily walk task to create the next occurrence...")
    next_walk = task1.mark_complete()
    if next_walk:
        print("Created new recurring task:", next_walk.summary())


if __name__ == "__main__":
    main()
