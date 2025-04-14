from datetime import datetime, timedelta
import heapq
from collections import defaultdict

# Linked List Implementation
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.task)
            current = current.next
        return result

class Task:
    def __init__(self, name, deadline, workload, priority):
        self.name = name
        self.deadline = deadline
        self.workload = workload  # in minutes
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority  # used by heapq

    def __str__(self):
        return f"{self.name} | Priority: {self.priority}, Workload: {self.workload} mins, Deadline: {self.deadline}" # displays relevant task information

class TimeSlot:
    def __init__(self, start_time, task):
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=task.workload)
        self.task = task

    def overlaps(self, other):
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time) # checks if time slots overlap

class AvailabilitySlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def contains(self, time_slot):
        return self.start_time <= time_slot.start_time and time_slot.end_time <= self.end_time # checks if time slot is within given availability time ranges

# merge sort to sort tasks
def merge_sort(tasks, key=lambda x: x.deadline):
    if len(tasks) <= 1:
        return tasks
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], key)
    right = merge_sort(tasks[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

class Calendar:
    def __init__(self, availability_slots):
        self.schedule = defaultdict(list)  # calendar dictionary, key = day, value = list of TimeSlot
        self.availability = availability_slots

    def is_available(self, start_time, task): # checks if task can be scheduled at given start time using TimeSlot and AvailabilitySlot classes
        new_slot = TimeSlot(start_time, task)
        day_key = start_time.strftime('%Y-%m-%d')
        for slot in self.schedule[day_key]:
            if new_slot.overlaps(slot):
                return False
        return any(avail.contains(new_slot) for avail in self.availability)

    def find_next_available_time(self, task): # finds next available time slot for task
        for avail in self.availability:
            check_time = avail.start_time
            while check_time + timedelta(minutes=task.workload) <= avail.end_time:
                if self.is_available(check_time, task):
                    return check_time
                check_time += timedelta(minutes=5)
        return None

    def add_to_calendar(self, task): # adds task to calendar
        start_time = self.find_next_available_time(task)
        if start_time:
            slot = TimeSlot(start_time, task)
            day_key = start_time.strftime('%Y-%m-%d')
            self.schedule[day_key].append(slot)
            print(f"Scheduled '{task.name}' at {start_time.strftime('%Y-%m-%d %H:%M')}.")
        else:
            print(f"Couldn't schedule '{task.name}' — not enough time.")

    def display(self): # displays calendar
        if not self.schedule:
            print("Calendar is empty.")
            return
        for day in sorted(self.schedule.keys()):
            print(f"\n{day}:")
            for slot in sorted(self.schedule[day], key=lambda s: s.start_time):
                print(f"  {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')} | {slot.task.name} (Priority {slot.task.priority})")

    def sort_scheduled_tasks(self, sort_by): # sorts tasks in calendar by given criteria
        key_funcs = {
            "priority": lambda s: s.task.priority,
            "workload": lambda s: s.task.workload,
            "deadline": lambda s: s.task.deadline
        }
        if sort_by in key_funcs:
            for day in self.schedule:
                self.schedule[day] = merge_sort(self.schedule[day], key=key_funcs[sort_by])
            print(f"\nTasks sorted by {sort_by.capitalize()}:")
            self.display()
        else:
            print("Invalid sort option.")

class TaskScheduler:
    def __init__(self):
        self.tasks = []  # min heap for priority queue

    def add_task(self, task): # adds task to priority queue based of priority value
        heapq.heappush(self.tasks, task)

    def schedule_all(self, calendar): # schedules all tasks in priority queue
        while self.tasks:
            task = heapq.heappop(self.tasks)
            calendar.add_to_calendar(task)

# UI functions
def get_task_from_user(): # gets task information from user and creates Task object based on input
    name = input("Task name (or type 'done' to finish): ").strip()
    if name.lower() == "done":
        return None
    try:
        priority = int(input("Priority (1-5): ").strip())
        workload = int(input("Workload in minutes: ").strip())
        deadline_str = input("Deadline (YYYY-MM-DD HH:MM): ").strip()
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        return Task(name, deadline, workload, priority)
    except Exception as e:
        print(f"Invalid input: {e}")
        return get_task_from_user()

def get_availability_ranges(): # gets availability time ranges from user and creates AvailabilitySlot objects based on input
    slots = []
    print("\nEnter availability time ranges (or type 'done' to finish).")
    while True:
        start = input("Start time (YYYY-MM-DD HH:MM): ").strip()
        if start.lower() == "done":
            break
        end = input("End time (YYYY-MM-DD HH:MM): ").strip()
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
            if end_dt > start_dt:
                slots.append(AvailabilitySlot(start_dt, end_dt))
            else:
                print("End must be after start.")
        except:
            print("Invalid format.")
    return slots

# Main
def main():
    print("Welcome to the Task Scheduler!\n")

    availability = get_availability_ranges()
    if not availability:
        print("No availability given. Exiting.")
        return

    calendar = Calendar(availability)
    scheduler = TaskScheduler()

    print("\nEnter your tasks:")
    while True:
        task = get_task_from_user()
        if task is None:
            break
        scheduler.add_task(task)
        print(f"Task added: {task}\n")

    print("\nScheduling tasks...\n")
    scheduler.schedule_all(calendar)
    calendar.display()

    print("\nSort scheduled tasks?")
    print("1. By Priority")
    print("2. By Workload")
    print("3. By Deadline")
    print("4. No sorting")

    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        calendar.sort_scheduled_tasks("priority")
    elif choice == "2":
        calendar.sort_scheduled_tasks("workload")
    elif choice == "3":
        calendar.sort_scheduled_tasks("deadline")
    else:
        print("No additional sorting applied.")

if __name__ == "__main__":
    main()

# for future use:
# https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop
