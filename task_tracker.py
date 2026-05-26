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

    now_str = datetime.now().isoformat()
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
    else:
        print(f"Unknow command: {sys.argv[1]}")    

    