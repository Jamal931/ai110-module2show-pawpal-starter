import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.
This app helps a pet owner track care tasks, manage pets, and build a daily schedule.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", constraints={"available_minutes": "90"})

owner = st.session_state.owner

with st.expander("Owner & Pets", expanded=True):
    owner.name = st.text_input("Owner name", value=owner.name)

    st.markdown("### Add a pet")
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
    species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
    age = st.number_input("Age", min_value=0, max_value=30, value=2, key="pet_age")

    if st.button("Add pet"):
        new_pet = Pet(name=pet_name, species=species, age=age)
        owner.add_pet(new_pet)

    if owner.pets:
        st.markdown("#### Current pets")
        for pet in owner.pets:
            st.write(f"- {pet.describe_pet()}")
    else:
        st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
if not owner.pets:
    st.info("Add a pet first, then assign tasks to that pet.")
else:
    selected_pet_name = st.selectbox(
        "Assign task to pet",
        [pet.name for pet in owner.pets],
        key="task_pet",
    )
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)

    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"], key="task_category")
    start_time = st.text_input("Start time (HH:MM)", value="08:00", key="task_start_time")
    frequency = st.selectbox("Frequency", ["", "daily", "weekly"], key="task_frequency")

    if st.button("Add task"):
        new_task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
            start_time=start_time if start_time else None,
            frequency=frequency if frequency else None,
        )
        new_task.assign(owner, selected_pet)
        selected_pet.add_task(new_task)

    if owner.all_tasks():
        st.markdown("#### Current tasks")
        for pet in owner.pets:
            if pet.tasks:
                st.markdown(f"**{pet.name}**")
                for task in pet.tasks:
                    st.write(f"- {task.summary()}")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Schedule Preview")

if owner.all_tasks():
    filter_col, sort_col = st.columns(2)
    with filter_col:
        filter_status = st.selectbox("Show status", ["all", "pending", "completed"], index=0)
        filter_pet = st.selectbox(
            "Filter by pet", ["all"] + [pet.name for pet in owner.pets], index=0
        )
    with sort_col:
        sort_by = st.selectbox("Sort tasks by", ["start time", "priority", "duration"], index=0)

    scheduler = Scheduler(owner=owner, time_budget=owner.available_time())
    visible_tasks = scheduler.filter_tasks(
        status=filter_status if filter_status != "all" else None,
        pet_name=filter_pet if filter_pet != "all" else None,
    )

    if sort_by == "start time":
        visible_tasks = scheduler.sort_by_time(visible_tasks)
    elif sort_by == "priority":
        visible_tasks = scheduler.rank_tasks(visible_tasks)
    else:
        visible_tasks = sorted(visible_tasks, key=lambda task: task.duration_minutes)

    task_rows = [
        {
            "Pet": task.pet.name if task.pet else "-",
            "Title": task.title,
            "Category": task.category or "-",
            "Priority": task.priority,
            "Start": task.start_time or "-",
            "Duration": task.duration_minutes,
            "Status": "Completed" if task.completed else "Pending",
            "Due": task.due_date.isoformat() if task.due_date else "-",
        }
        for task in visible_tasks
    ]
    st.table(task_rows)

    if st.button("Generate schedule"):
        schedule = scheduler.generate_plan()
        warnings = scheduler.detect_conflicts(schedule.tasks)

        st.markdown("### Today's Schedule")
        st.table(
            [
                {
                    "Task": task.title,
                    "Pet": task.pet.name if task.pet else "-",
                    "Start": task.start_time or "-",
                    "Priority": task.priority,
                    "Duration": task.duration_minutes,
                    "Status": "Completed" if task.completed else "Pending",
                }
                for task in schedule.tasks
            ]
        )

        if warnings:
            for warning in warnings:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        st.markdown(schedule.explain_plan())
else:
    st.info("Add a task to see the scheduler preview and conflict detection.")
