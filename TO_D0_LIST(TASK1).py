import tkinter as tk
from tkinter import messagebox
import datetime

def load_tasks():
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
            return [task.strip() for task in tasks]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.txt', 'w') as file:
        file.write('\n'.join(tasks))

def add_task(root, tasks_listbox):
    def save_task():
        task_name = task_entry.get()
        priority = priority_var.get().lower()
        due_date = due_date_entry.get()

        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        new_task = f"Task: {task_name}, Priority: {priority}, Due Date: {due_date}, Status: Not Completed"
        tasks_listbox.insert(tk.END, new_task)

        tasks_list = tasks_listbox.get(0, tk.END)
        save_tasks(tasks_list)
        messagebox.showinfo("Success", "Task added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Task")

    task_label = tk.Label(add_window, text="Task Name:")
    task_label.pack()
    task_entry = tk.Entry(add_window)
    task_entry.pack()

    priority_label = tk.Label(add_window, text="Priority:")
    priority_label.pack()
    priority_var = tk.StringVar(add_window)
    priority_var.set("High")
    priority_option = tk.OptionMenu(add_window, priority_var, "High", "Medium", "Low")
    priority_option.pack()

    due_date_label = tk.Label(add_window, text="Due Date (YYYY-MM-DD):")
    due_date_label.pack()
    due_date_entry = tk.Entry(add_window)
    due_date_entry.pack()

    save_button = tk.Button(add_window, text="Save", command=save_task)
    save_button.pack()

def remove_task(root, tasks_listbox):
    def remove_selected_task():
        selected_task = tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            tasks_listbox.delete(index)
            tasks_list = tasks_listbox.get(0, tk.END)
            save_tasks(tasks_list)
            messagebox.showinfo("Success", "Task removed successfully!")
            remove_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a task to remove.")

    remove_window = tk.Toplevel(root)
    remove_window.title("Remove Task")

    tasks_listbox.pack()

    remove_button = tk.Button(remove_window, text="Remove", command=remove_selected_task)
    remove_button.pack()

def complete_task(root, tasks_listbox):
    def complete_selected_task():
        selected_task = tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task = tasks_listbox.get(index)
            updated_task = task.replace("Status: Not Completed", "Status: Completed")
            tasks_listbox.delete(index)
            tasks_listbox.insert(index, updated_task)
            tasks_list = tasks_listbox.get(0, tk.END)
            save_tasks(tasks_list)
            messagebox.showinfo("Success", "Task marked as completed!")
            complete_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a task to mark as completed.")

    complete_window = tk.Toplevel(root)
    complete_window.title("Mark Task as Completed")

    tasks_listbox.pack()

    complete_button = tk.Button(complete_window, text="Mark as Completed", command=complete_selected_task)
    complete_button.pack()

def display_tasks(root):
    display_window = tk.Toplevel(root)
    display_window.title("View Tasks")

    tasks = load_tasks()

    tasks_listbox = tk.Listbox(display_window)
    for task in tasks:
        tasks_listbox.insert(tk.END, task)
    tasks_listbox.pack()

def main():
    root = tk.Tk()
    root.title("To-Do List")

    tasks = load_tasks()

    tasks_listbox = tk.Listbox(root, font=('Arial', 12), width=50, height=15)
    for task in tasks:
        tasks_listbox.insert(tk.END, task)
    tasks_listbox.pack(padx=10, pady=10)

    add_button = tk.Button(root, text="Add Task", command=lambda: add_task(root, tasks_listbox))
    add_button.pack()

    remove_button = tk.Button(root, text="Remove Task", command=lambda: remove_task(root, tasks_listbox))
    remove_button.pack()

    complete_button = tk.Button(root, text="Mark as Completed", command=lambda: complete_task(root, tasks_listbox))
    complete_button.pack()

    view_button = tk.Button(root, text="View Tasks", command=lambda: display_tasks(root))
    view_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
