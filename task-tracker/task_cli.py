import sys
import json
import os
from datetime import datetime

# Data file name
DATA_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file or return empty list"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    """Add new task with auto-increment ID"""
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, new_description):
    """Update task description"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task ID {task_id} not found")

def delete_task(task_id):
    """Delete task by ID"""
    tasks = load_tasks()
    filtered = [t for t in tasks if t['id'] != task_id]
    if len(tasks) == len(filtered):
        print(f"Task ID {task_id} not found")
    else:
        save_tasks(filtered)
        print(f"Task {task_id} deleted")

def change_status(task_id, status):
    """Update task status"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"Task ID {task_id} not found")

def list_tasks(status=None):
    """List tasks with optional status filter"""
    tasks = load_tasks()
    
    if status:
        status = status.lower()
        valid_statuses = ['todo', 'in-progress', 'done']
        if status not in valid_statuses:
            print(f"Invalid status. Use: {', '.join(valid_statuses)}")
            return
        tasks = [t for t in tasks if t['status'] == status]
    
    if not tasks:
        print("No tasks found")
        return
    
    print("\nID  | Status        | Description")
    print("-" * 40)
    for task in tasks:
        print(f"{task['id']:<3} | {task['status']:<12} | {task['description']}")
    print()

def main():
    """Handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: task_cli [command] [options]")
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Missing task description")
            return
        add_task(sys.argv[2])
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task_cli update [id] [new_description]")
            return
        try:
            task_id = int(sys.argv[2])
            update_task(task_id, sys.argv[3])
        except ValueError:
            print("Error: ID must be an integer")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task_cli delete [id]")
            return
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Error: ID must be an integer")
    
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: task_cli mark-in-progress [id]")
            return
        try:
            task_id = int(sys.argv[2])
            change_status(task_id, "in-progress")
        except ValueError:
            print("Error: ID must be an integer")
    
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: task_cli mark-done [id]")
            return
        try:
            task_id = int(sys.argv[2])
            change_status(task_id, "done")
        except ValueError:
            print("Error: ID must be an integer")
    
    elif command == "list":
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status_filter)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()