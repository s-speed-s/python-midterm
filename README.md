# python-midterm
# Task Scheduler

This is a console-based Task Scheduler built in Python that allows users to manage their tasks efficiently based on priority, deadlines, and availability. It automatically schedules tasks into available time slots and lets users view and sort their scheduled tasks.

---

## Features

- Add tasks with:
  - Priority (1-5, higher number means lower priority)
  - Workload (in minutes)
  - Deadline (`YYYY-MM-DD HH:MM`, 24 hour format)
- Input custom availability time ranges
- Automatically schedules tasks to avoid conflicts
- Sort scheduled tasks by:
  - Priority
  - Workload
  - Deadline
- Console-based user interface
- Insertion Sort used for post-scheduling sorting

When ran, the program will prompt the user for information relevant to creating the schedule. Follow the directions in the console to create your schedule.
