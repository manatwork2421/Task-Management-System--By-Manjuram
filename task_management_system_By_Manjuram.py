'''
Project Name:Task Management system 
Made BY:Manjuram Gajanan Prabhudessai
'''


import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"
PRIORITY_ORDER = {"low": 1, "medium": 2, "high": 3}




class Task:
    '''
    Repersent single task in the system
    '''
    def __init__(self, task_id, title, description, priority, due_date=None,
                 completed=False, created_at=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """
        converts task object to dictonary for json serialization
        """
        return self.__dict__




class User:
    """
    represents user and manages all task related to that user
    """
    def __init__(self, username, tasks=None):
        self.username = username
        self.tasks = tasks if tasks else []

    def generate_task_id(self):
        '''
        generate the unique task id for the user
        '''
        return max([task.id for task in self.tasks], default=0) + 1

    def add_task(self):
        """
        adds new task for that user
        """
        title = input("Title: ")
        description = input("Description: ")
        priority = input("Priority (low/medium/high): ").lower()
        due = input("Due Date (YYYY-MM-DD or blank): ")
        due_date = due if due else None

        task = Task(
            self.generate_task_id(),
            title,
            description,
            priority,
            due_date
        )

        self.tasks.append(task)
        print("✅ Task added successfully")

    def view_tasks(self, filter_type=None):
        '''
        Docstring for view_tasks
        
        :param self: Display task
        :param filter_type: can be
                            1)completed
                            2)pending
        '''
        if not self.tasks:
            print("No tasks found.")
            return

        for task in self.tasks:
            if filter_type == "completed" and not task.completed:
                continue
            if filter_type == "pending" and task.completed:
                continue

            status = "DOne" if task.completed else "Not done"
            print(f"""
ID: {task.id}
Title: {task.title}
Priority: {task.priority}
Due Date: {task.due_date}
Status: {status}
Created At: {task.created_at}
-----------------------
""")

    def edit_task(self):#updates the existing task
        task_id = int(input("Enter Task ID: "))
        for task in self.tasks:
            if task.id == task_id:
                task.title = input("New Title: ") or task.title
                task.description = input("New Description: ") or task.description
                task.priority = input("New Priority: ") or task.priority
                due = input("New Due Date: ")
                task.due_date = due or task.due_date
                print("✏️ Task updated")
                return
        print("Task not found")

    def delete_task(self):#deletes the task using task id
        task_id = int(input("Enter Task ID: "))
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                print("🗑️ Task deleted")
                return
        print("Task not found")

    def mark_task(self):
        task_id = int(input("Enter Task ID: "))
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                print("🔄 Task status updated")
                return
        print(" Task not found")

    def sort_tasks(self):
        '''
        Sorts task based on their choice
        '''
        print("1. By Priority\n2. By Creation Date\n3. By Completion Status")
        choice = input("Choose: ")

        if choice == "1":
            self.tasks.sort(key=lambda t: PRIORITY_ORDER[t.priority], reverse=True)
        elif choice == "2":
            self.tasks.sort(key=lambda t: t.created_at)
        elif choice == "3":
            self.tasks.sort(key=lambda t: t.completed)

        print("📊 Tasks sorted")



class TaskManager:
    '''
    controls teh program flow  that is
        i)login
        ii)menu handling
        iii)file perisistance
    '''
    def __init__(self):
        self.users = self.load_data()
        self.current_user = None

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                raw = json.load(f)
                users = {}
                for username, tasks in raw.items():
                    users[username] = User(
                        username,
                        [Task(**task) for task in tasks]
                    )
                return users
        return {}

    def save_data(self):
        data = {
            username: [task.to_dict() for task in user.tasks]
            for username, user in self.users.items()
        }
        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    def login(self):
        username = input("Enter username: ")
        if username not in self.users:
            self.users[username] = User(username)
        self.current_user = self.users[username]

    def menu(self):
        while True:
            print("""
---- TASK MANAGEMENT SYSTEM ----
1. Add Task
2. View All Tasks
3. View Completed Tasks
4. View Pending Tasks
5. Edit Task
6. Delete Task
7. Mark Task Complete/Incomplete
8. Sort Tasks
9. Save & Exit
""")
            choice = input("Choose option: ")

            if choice == "1":
                self.current_user.add_task()
            elif choice == "2":
                self.current_user.view_tasks()
            elif choice == "3":
                self.current_user.view_tasks("completed")
            elif choice == "4":
                self.current_user.view_tasks("pending")
            elif choice == "5":
                self.current_user.edit_task()
            elif choice == "6":
                self.current_user.delete_task()
            elif choice == "7":
                self.current_user.mark_task()
            elif choice == "8":
                self.current_user.sort_tasks()
            elif choice == "9":
                self.save_data()
                print("💾 Data saved. Goodbye!")
                break
            else:
                print("❌ Invalid choice")

    def run(self):
        self.login()
        self.menu()



if __name__ == "__main__":
    TaskManager().run()
