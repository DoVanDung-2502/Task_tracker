from datetime import datetime
import json
import os
import sys

JSON_FILE = "tasks.json"

def init_db():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump([],f,indent=4)
def read_db():
    init_db()
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
def write_db(tasks):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks,f,indent=4, ensure_ascii=False)

def add_task(description):
    if not description.strip():
        print("Error: Task description cannot be empty.")
        return False
    
    tasks = read_db()

    new_id = max([t['id'] for t in tasks], default=0) + 1

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_task = {
        'id' : new_id,
        'description' : description,
        'created_at' : now_str,
        'updated_at' : now_str,
        'status': "todo",
        }
    tasks.append(new_task)
    write_db(tasks)
    print(f"Added task '{description}' (ID: {new_id})")
    
def update_task(task_id, new_description):
    if not new_description.strip():
        print("Error: Description cannot be empty")
        return False
    
    tasks = read_db()
    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            found = True
            break
    if found:
        write_db(tasks)
        print(f"Updated task {task_id} '{new_description}'")
    else:
        print(f"Error: Task with ID {task_id} not found")
        return False
    return True

def delete_task(task_id):
    tasks = read_db()
    original_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]

    if len(tasks) < original_length:
        print(f"Task {task_id} deleted")
        write_db(tasks)
    else:
        print(f"Error: Task with ID {task_id} not found")
        return False
    return True
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task_tracker.py add [description]")
        sys.exit(1)
    
    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide detail task")
            print("Example: Python task_tracker.py add [description]")
        else:
            description = " ".join(sys.argv[2:])
            add_task(description)
            sys.exit(0)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python task_tracker.py update <task_id> <new_description>")
        else:
            try:
                task_id = int(sys.argv[2])
                new_description = " ".join(sys.argv[3:])
                update_task(task_id, new_description)
            except ValueError:
                print("Error: Task ID must be a number")
            sys.exit(0) 
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python task_tracker.py delete <task_id>")
        else:
            try:
                task_id = int(sys.argv[2])
                delete_task(task_id)  
            except ValueError:
                print("Error: Task ID must be a number")
        sys.exit(0)     

    