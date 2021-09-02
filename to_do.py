import tkinter as tk
import tkinter.font as font
import datetime
import sqlite3
from sqlite3 import Error
from tkinter import messagebox

# initialize database if not created, establish connection, create cursor object for SQL execution in db
db_file = "database.sqlite3"

#-------------- def: create user tables--------------#
def make_data_tables(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()


    create_table_users = "CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text NOT NULL, joined_on date NOT NULL);"

    create_table_tasks = """CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY, task text NOT NULL, 
                        user_id integer NOT NULL, added date NOT NULL, status bool NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id));"""

    # execute SQL statements above to create tables

    c.execute(create_table_users)
    c.execute(create_table_tasks)

    conn.close()

#--------------- end create user tables--------------#

# show_frame function to switch between frames displayed in the window

def show_frame(frame):
    frame.tkraise()

copyright_symbol = u"\u00A9"

# window instantiation (put into a function)

window = tk.Tk()
window.minsize(900, 600)
window.title("My To Do List")
mystring=tk.StringVar(window)

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

#--------------------  UPDATE ALL FRAMES HERE -------------------#  

homepage = tk.Frame(window, bg = "#3A3A3D")
new_user_page = tk.Frame(window, bg = "#3A3A3D")
existing_user_page = tk.Frame(window, bg = "#3A3A3D")
current_task_page = tk.Frame(window, bg = "#3A3A3D")
add_task_page = tk.Frame(window, bg = "#3A3A3D")
edit_user_page = tk.Frame(window, bg="#3A3A3D")
edit_task_page = tk.Frame(window, bg="#3A3A3D")


for frame in (homepage, new_user_page, existing_user_page, current_task_page, add_task_page, edit_user_page, edit_task_page):
    frame.grid(row=0, column=0, sticky="nesw")



#--------------------------------END UPDATE FRAMES----------------------------#

def addUser(name_entry):    
    
    #NEW CONNECTION ESTABLISHED
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()

    name = name_entry.get()
    latest_id_query = "SELECT id FROM users ORDER BY id DESC LIMIT 1"

    query = c.execute(latest_id_query).fetchall()

    if not query:
        new_id = 1
    else:
        new_id = query[0][0]+1

    today = datetime.date.today()
    # new_id = 1

    new_user = "INSERT INTO users (id, name, joined_on) VALUES ({}, '{}', '{}');".format(new_id, name, today)
    c.execute(new_user)
    conn.commit()
    conn.close()
    print("Connection closed!")
    
    # CONNECTION CLOSED
    
    messagebox.showinfo("Success!", f"New user added: {name}")
    
    name_entry.delete(0, 'end')

    build_current_task_page(name)


def addTask(user_id,user_name, task_field):
    
    #NEW CONNECTION ESTABLISHED
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()
    latest_id_query = "SELECT id FROM tasks ORDER BY id DESC LIMIT 1"
    
    query = c.execute(latest_id_query).fetchall()

    if not query:
        new_id = 1
    else:
        new_id = query[0][0]+1

    today = datetime.date.today()
    
    task=task_field.get()

    query = f"INSERT INTO tasks (id, task, user_id, added, status) VALUES ({new_id}, '{task}', {user_id}, '{today}', 0);"
    c.execute(query)
    
    conn.commit()
    print("New task added successfully!")
    conn.close()
    print("Connection closed!\n")

    messagebox.showinfo("Success!", f"New task added: {task}")

    build_current_task_page(user_name)

    

def edit_task(user_id, user_name, old_task, new_task):
    
    #NEW CONNECTION ESTABLISHED
    
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()
    
    task_id_query = f"SELECT id FROM tasks WHERE task = '{old_task}'"
    print(task_id_query)
    task_id = c.execute(task_id_query).fetchall()[0][0]
    print(task_id)
    
    update_query = f"UPDATE tasks SET task = '{new_task}', added={datetime.date.today()} WHERE id = {task_id};"
    c.execute(update_query)

    conn.commit()
    conn.close()

    messagebox.showinfo("Success!", "Task successfully updated!")
    build_current_task_page(user_name)
    
def edit_user(user_name, new_user_name):
    
    #NEW CONNECTION ESTABLISHED
    
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()
    
    user_id_query = f"SELECT id FROM users WHERE name = '{user_name}'"
    print(user_id_query)
    user_id = c.execute(user_id_query).fetchall()[0][0]
    print(user_id)
    
    update_query = f"UPDATE users SET name = '{new_name}', added={datetime.date.today()} WHERE id = {user_id};"
    c.execute(update_query)

    conn.commit()
    conn.close()

    messagebox.showinfo("Success!", "Task successfully updated!")
    build_existing_user_page()

def delete_user(user_list):
     #NEW CONNECTION ESTABLISHED
    
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()

    current_user_index = user_list.curselection()[0]
    current_user = user_list.get(current_user_index)

    print(current_user)

    user_id_query = f"SELECT id FROM users WHERE name='{current_user}';"
    user_id = c.execute(user_id_query).fetchall()[0][0]

    delete_query = f"DELETE FROM users WHERE id = {user_id};"
    c.execute(delete_query)

    conn.commit()
    conn.close()
    messagebox.showinfo("Success!", "User successfully deleted!")

    print("Connection closed")
    build_existing_user_page()


def delete_task(task_list, user_name):
    
    # ESTABLISHING CONNECTION
    
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()

    task_title_index = task_list.curselection()[0]
    task_title = task_list.get(task_title_index)

    task_id_query = f"SELECT id FROM tasks WHERE task='{task_title}';"
    task_id = c.execute(task_id_query).fetchall()[0][0]

    delete_query = f"DELETE FROM tasks WHERE id = {task_id};"
    c.execute(delete_query)
    conn.commit()
    conn.close()
    print("Closing connection")
    messagebox.showinfo("Success!", "Task successfully deleted!")
    build_current_task_page(user_name)



def update_status(user_name, user_id, task_list):
    #NEW CONNECTION ESTABLISHED
    
    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()
    
    task_index = task_list.curselection()[0]
    task = task_list.get(task_index)

    task_id_query = f"SELECT id FROM tasks WHERE task = '{task}'"
    print(task_id_query)
    task_id = c.execute(task_id_query).fetchall()[0][0]
    print(task_id)
    
    status_check_query = f"SELECT status FROM tasks WHERE task = '{task}'"
    status_check = c.execute(status_check_query).fetchall()[0][0]
    
    if status_check==0:
        update_query = f"UPDATE tasks SET status = 1 WHERE id = {task_id};"
        c.execute(update_query)
    else:
        update_query = f"UPDATE tasks SET status = 0 WHERE id = {task_id};"
        c.execute(update_query)

    conn.commit()
    conn.close()

    messagebox.showinfo("Success!", "Status successfully updated!")
    build_current_task_page(user_name)



def build_homepage():
    
    homepage.columnconfigure(0, weight=1)
    homepage.rowconfigure([0, 1, 2, 3, 4], weight=1, minsize=7)
    # homepage.rowconfigure(1, weight=1, minsize=10)
    # homepage.rowconfigure(2, weight=1, minsize=100)
    # homepage.rowconfigure(3, weight=2, minsize=10)
    # homepage.rowconfigure(4, weight=2, minsize=10)

    header = tk.Label(master=homepage, text="My To-Do List", font=(None, 48), bg = "#3A3A3D", fg="white")
    #header.pack(pady=(70,131))
    header.grid(column=0, row=0, sticky="ew")

    btn_new_user = tk.Button(master=homepage, text="New Users", 
                    font=(None, 26), width=14, bg="blue", command=lambda: build_new_user_page()) # look up why lambda designation fixed this   ######   SHOW > BUILD
    btn_new_user.grid(column=0, row=2, sticky="n", pady=0)

    btn_existing_user = tk.Button(master=homepage, text="Existing Users", 
                        font=(None, 26), width=14, bg="red", command=lambda: build_existing_user_page())    ######   SHOW > BUILD
    # btn_existing_user.pack(pady=(5, 31))
    btn_existing_user.grid(column=0, row=2, sticky="s", pady=0)

    copyright = tk.Label(master=homepage, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    # copyright.pack(pady=(5,0))
    copyright.grid(column = 0, row=4, sticky="ew", pady=(20, 8))

    show_frame(homepage)

def build_new_user_page():
    
    new_user_page.columnconfigure(0, weight=1)
    new_user_page.rowconfigure([0, 1, 2, 3, 4, 5], weight=1, minsize=15)

    header = tk.Label(master=new_user_page, text="My To-Do List", font=(None, 48), bg = "#3A3A3D", fg="white")
    header.grid(column=0, row=0, sticky="ew")
    
    name_label = tk.Label(master=new_user_page, text="Name:", fg="white", bg="#3A3A3D", font=(None, 22))
    name_label.grid(column=0, row=2, padx=(0,400))

    name_entry = tk.Entry(master=new_user_page, textvariable=mystring, borderwidth=2, relief=tk.SUNKEN, width=22, justify="center", font=(None, 22))
    name_entry.grid(column=0, row=2, padx=(180, 0), pady=10)

    submit_btn = tk.Button(master=new_user_page, text="Submit", bg="blue", fg="white", font=(None, 18), command=lambda: addUser(name_entry))
    submit_btn.grid(column=0, row=3, sticky="n")

    home_btn = tk.Button(master=new_user_page, text="Back to Login Page", font=(None, 16), bg="orange", fg="white", command=lambda: show_frame(homepage)) 
    home_btn.grid(column=0, row=4)

    copyright = tk.Label(master=new_user_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, row=5, sticky="sew", pady=(20, 8))

    show_frame(new_user_page)


def build_existing_user_page():

    existing_user_page.columnconfigure(0, weight=1)
    existing_user_page.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

    db_file = "database.sqlite3"    # MAKE THE DB NAME A PARAMETER?
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()

    existing_user_page.columnconfigure(0, weight=1)
    existing_user_page.rowconfigure([0,1, 2, 3, 4], weight=1, minsize=15)

    # get list of users via SQL execution of cursor

    select_users = "SELECT id, name FROM users;"
    query = c.execute(select_users).fetchall() # list of rows currently in the db

    header = tk.Label(master=existing_user_page, text="Existing Users", font=(None, 42), bg = "#3A3A3D", fg="white")
    header.grid(column=0, row=0, sticky="ew", pady=(20,40))

    user_list = tk.Listbox(master=existing_user_page, width=30, font=(None, 16))
    user_list.configure(justify="center")
    
    for i, row in enumerate(query):
        id = row[0]
        name=row[1]
        user_list.insert(i, name)
    user_list.grid(column=0, row=1, pady=(20, 30))
    
    conn.close()        # CLOSING CONNECTION
    print("Connection closed!")

    # upon clicking select, get the name from the listbox, generate current_tasks view with all data pertaining to the particular user returned from the user_list

    select_btn = tk.Button(master=existing_user_page, text="See Tasks", bg="blue", fg="white", font=(None, 18), command=lambda: build_current_task_page_existing(user_list)) ######    BUILD
    select_btn.grid(column=0, row=2)

    delete_btn = tk.Button(master=existing_user_page, text="Delete User", bg="red", fg="white", font=(None, 18), command=lambda: delete_user(user_list)) ######    BUILD
    delete_btn.grid(column=0, row=3, pady=10)

    home_btn = tk.Button(master=existing_user_page, text="Back to Login Page", bg="orange", fg="white", font=(None, 14), command=lambda: show_frame(homepage))   ######   SHOW > BUILD
    home_btn.grid(column=0, row=4, pady=10)

    copyright = tk.Label(master=existing_user_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, row=5, sticky="ew", pady=(10, 8))

    show_frame(existing_user_page)

# user current_user as param in the function below to ensure the right data is generated
# run this function upon clicking a button from one of the other pages, to ensure correct render each time - may interfere with initial frame build?

def build_current_task_page(user_name): 
    current_task_page.columnconfigure([0, 2], weight=1)
    current_task_page.columnconfigure(1, weight=1)
    current_task_page.rowconfigure([0, 1, 2, 3, 4], weight=1)

    header = tk.Label(master=current_task_page, text=f"{user_name}'s Tasks", font=(None, 36), bg = "#3A3A3D", fg="white")
    header.grid(column=0, columnspan=3, row=0, sticky="ew", pady=20)

    # build_task_list(current_user)
    
    db_file = "database.sqlite3"    # MAKE THE DB NAME A PARAMETER?
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print("\nConnection established!\n")
        print(sqlite3.version)
        
    except Error as e:
        print(e)

    c = conn.cursor()
    
    user_query = f"SELECT id FROM users WHERE name = '{user_name}';"
    user_id = c.execute(user_query).fetchall()[0][0]             # maybe remove the [0]
    print(f"User_id: {user_id}")

    task_query = f"SELECT * FROM tasks WHERE user_id = {user_id}"
    task_query_result = c.execute(task_query).fetchall()
    
    print("task_query_result: \n", task_query_result)

    task_label = tk.Label(master=current_task_page, text="Task:", fg="white", font=(None, 26), bg = "#3A3A3D")
    task_label.grid(column=0, columnspan=3, row=1, sticky="ew", padx=(0, 180))

    status_label = tk.Label(master=current_task_page, text="Status:", fg="white", bg="#3A3A3D", font=(None, 26))
    status_label.grid(column=2, row=1)

    task_list = tk.Listbox(master=current_task_page, width=28, justify="center", font=(None, 16))
    print("Len task queryResult; {}".format(len(task_query_result)))
    
    status_list = tk.Listbox(master=current_task_page, bg="#3A3A3D", justify="left", font=(None, 16), borderwidth=0, highlightthickness=0)

    try:

        for i, row in enumerate(task_query_result):
            
            task_list.insert(i, row[1])
            if row[4] == 0:
                status_list.insert(i, " X  -  INCOMPLETE")
                status_list.itemconfig(i, {"fg":"red"})
            else:
                status_list.insert(i, " \u2713  -  COMPLETE")
                status_list.itemconfig(i, {"fg":"green"})
            
    
        task_list.grid(column=0, columnspan=3, row=2, sticky="n", padx=(0, 180), pady=10)
        status_list.grid(column=2, row=2, sticky="n", pady=10)
    except:
        messagebox.showwarning("NO TASKS FOUND", "WARNING:  Task list is currently empty for this user!  Please add a task.")

    conn.close()        # CLOSING CONNECTION
    print("Connection closed!")

    add_task_btn = tk.Button(master=current_task_page, text="Add Task", bg="blue", fg="white", font=(None, 14), command=lambda: build_add_task_page(user_name, user_id))
    add_task_btn.grid(column=0, columnspan=3, row=3, padx=(0, 150), pady=20)

    status_update_btn = tk.Button(master=current_task_page, text="Update Status", bg="green", fg="white", font=(None, 14), command=lambda: update_status(user_name, user_id, task_list))
    status_update_btn.grid(column=0, columnspan=3, row=3, padx=(150, 0), pady=20)

    edit_task_btn = tk.Button(master=current_task_page, text="Edit Task", bg="orange", fg="white", font=(None, 14), command=lambda: build_edit_task_page(user_id, user_name, task_list))
    edit_task_btn.grid(column=0, columnspan=3, row=5, pady=10)

    delete_task_btn = tk.Button(master=current_task_page, text="Delete Task", bg="red", fg="white", font=(None, 14), command=lambda: delete_task(task_list, user_name))
    delete_task_btn.grid(column=0, columnspan=3, row=6, pady=10)
    
    back_btn = tk.Button(master=current_task_page, text="Switch Users", bg="white", fg="blue", font=(None, 14), command=lambda: build_existing_user_page())  ######   BUILD
    back_btn.grid(column=0, columnspan=3, row=7, pady=7)

    copyright = tk.Label(master=current_task_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, columnspan=3, row=8, sticky="ew", pady=(20,8))

    show_frame(current_task_page)


def build_current_task_page_existing(target_listbox):
    user_name_index = target_listbox.curselection()[0]
    user_name = target_listbox.get(user_name_index)
    
    build_current_task_page(user_name) ######    BUILD

def build_add_task_page(user_name, user_id):  # need user_name, user_id

    add_task_page.columnconfigure(0, weight=1)
    add_task_page.rowconfigure([0, 1, 2, 3, 4], weight=1)

    header = tk.Label(master=add_task_page, text=f"Add task for {user_name}", font=(None, 38), bg="#3A3A3D", fg="white")
    header.grid(column=0, row=0, sticky="ew")

    task_entry = tk.Entry(master=add_task_page, justify="center", font=(None, 18))
    task_entry.grid(column=0, row=1, sticky="nesw", padx=200)

    btn_add_task = tk.Button(master=add_task_page, text="Add Task", bg="blue", fg="white", font=(None, 18), command=lambda: addTask(user_id, user_name, task_entry))     # MAY GIVE ISSUES - POSSIBLE DEBUG (7:15 ON 8/5) # 
    btn_add_task.grid(column=0, row=2)

    back_btn = tk.Button(master=add_task_page, text="Back to Tasks", bg="orange", fg="white", font=(None, 16), command=lambda: build_current_task_page(user_name))   ######   SHOW > BUILD
    back_btn.grid(column=0, row=3)

    copyright = tk.Label(master=add_task_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, row=4, sticky="ew", pady=(10,8))

    show_frame(add_task_page)

def build_edit_task_page(user_id, user_name, task_list):
    
    edit_task_page.columnconfigure(0, weight=1)
    edit_task_page.rowconfigure(0, weight=1)
    edit_task_page.rowconfigure(1, weight=1)
    edit_task_page.rowconfigure(2, weight=1)
    
    header = tk.Label(master=edit_task_page, text=f"Edit task for {user_name}", font=(None, 38), bg="#3A3A3D", fg="white")
    header.grid(column=0, row=0, sticky="ew", pady=(10,10))

    # current_task = task_list.curselect ######################333   HEREE HEERE -------------------------------------------

    current_task_index = task_list.curselection()[0]
    current_task = task_list.get(current_task_index)

    current_task_str = tk.StringVar(edit_task_page, value=current_task)
    task_entry = tk.Entry(master=edit_task_page, textvariable=current_task_str, font=(None, 20), justify="center")
    # task_entry.insert(END, current_task)
    task_entry.grid(column=0, row=1, sticky="nesw", padx=100, pady=180)

    btn_submit = tk.Button(master=edit_task_page, bg="red", fg="white", text="Submit", font=(None, 26), command=lambda: edit_task(user_id, user_name, current_task, task_entry.get()))
    btn_submit.grid(column=0, row=2, sticky="n")

    copyright = tk.Label(master=edit_task_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, row=3, sticky="ew", pady=(10,8))

    show_frame(edit_task_page)

def build_edit_user_page(user_id, user_name, user_list):

    edit_user_page.columnconfigure(0, weight=1)
    edit_user_page.rowconfigure(0, weight=1)
    edit_user_page.rowconfigure(1, weight=1)
    edit_user_page.rowconfigure(2, weight=1)
    edit_user_page.rowconfigure(3, weight=1)

    header = tk.Label(master=edit_user_page, text=f"Edit User:  {user_name}", font=(None, 48), bg="#3A3A3D", fg="white", borderwidth=2, relief=tk.GROOVE)
    header.grid(column=0, row=0, sticky="ew")

    current_user_index = user_list.curselection()[0]
    new_user_name = user_list.get(current_user_index)

    current_user_str = tk.StringVar(edit_user_page, value=new_user_name)

    user_entry = tk.Entry(master=edit_user_page, textvariable=current_user_str)
    task_entry.grid(column=0, row=1)

    btn_submit = tk.Button(master=edit_task_page, bg="red", fg="white", text="Submit", font=(None, 26), command=lambda: edit_user(user_name, new_user_name))
    btn_submit.grid(column=0, row=2)

    copyright = tk.Label(master=edit_user_page, text=f"{copyright_symbol} Fabio Villagran-Gonzalez", font=(None, 11),
                fg="white", height=1, bg = "#3A3A3D")
    copyright.grid(column = 0, row=3, sticky="ew", pady=(10,8))


#-------------- INITIALIZE ALL FRAMES (BUILD INITIAL FRAME) --------------------------#
if __name__ == "__main__":
    make_data_tables(db_file)
    build_homepage()

    window.mainloop()
 