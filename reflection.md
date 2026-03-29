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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- The scheduler only checks for exact start-time conflicts rather than detecting overlapping durations.
- This tradeoff is reasonable because it keeps the logic lightweight and still catches the most obvious schedule clashes in a simple pet care app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
