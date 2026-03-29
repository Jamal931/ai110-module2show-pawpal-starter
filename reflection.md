# PawPal+ Project Reflection

## 1. System Design
Enter basic owner and pet information.
Add and edit pet care tasks (duration, priority, etc.).
Generate and view a daily care plan/schedule based on constraints.


**a. Initial design**

- Briefly describe your initial UML design.
Ans:

I chose these main classes and responsibilities:

- `Owner`
  - Holds owner-specific information like `name`, `preferences`, and `constraints`
  - Responsible for tracking available time, preferences, and any scheduling constraints that affect the day

- `Pet`
  - Holds pet-specific information like `name`, `species`, `age`, and `needs`
  - Responsible for representing the pet’s care requirements and any species-specific behavior

- `Task`
  - Holds task details like `title`, `duration_minutes`, `priority`, `category`, `deadline`, and `notes`
  - Responsible for representing a single care action, updating its properties, and exposing whether it is required today

- `Schedule`
  - Holds a daily plan with `date`, ordered `tasks`, and an `explanation`
  - Responsible for building the scheduled task list, calculating total time, formatting the output, and explaining the plan

- `Scheduler`
  - Holds the planning logic with references to `Owner`, `Pet`, `tasks`, and `time_budget`
  - Responsible for ranking tasks, applying constraints, generating the daily schedule, and explaining why tasks were chosen
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation? YES 
- If yes, describe at least one change and why you made it.
Ans: so Owner stores name, preferences, constraints, and pets
Responsible for owner-level data like available scheduling time and preference updates. it can also associate pets with the owner

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers owner available time, task priority, and task start time.
- Priority determines which tasks are included first, and the time budget ensures the schedule fits the owner’s available minutes.

**b. Tradeoffs**

- The scheduler only checks for exact start-time conflicts rather than detecting overlapping durations.
- This tradeoff is reasonable because it keeps the logic lightweight and still catches the most obvious schedule clashes in a simple pet care app.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI tools for design brainstorming, code generation, and validation.
- Helpful prompts were those that asked for class relationships, method behavior, and test plans.

**b. Judgment and verification**

- I rejected suggestions that added too much complexity to the scheduler, such as full overlap detection, in favor of a simpler conflict warning strategy.
- I verified AI output by checking the generated code against the app requirements and running tests.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, pet task assignment, time-based sorting, recurring daily task creation, and duplicate start time conflict detection.
- These tests ensure the core scheduling behaviors work and that the new algorithmic features behave as expected.

**b. Confidence**

- I am confident at about 4 stars because the key behaviors are covered and the scheduler passes the automated suite.
- Next, I would test overlapping task durations, multiple pet schedules, and invalid time input handling.

---

## 5. Reflection

**a. What went well**

- The project came together with a clean separation between the data model and scheduling logic.
- The UI now reflects the backend intelligence in a way that is easy to use.

**b. What you would improve**

- I would improve conflict detection to handle overlapping durations, not just exact start times.
- I would also add better task editing and persistence for the Streamlit interface.

**c. Key takeaway**

- I learned that being the lead architect means guiding AI suggestions with clear requirements and choosing the simplest design that meets the goals.
