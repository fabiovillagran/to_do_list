# My Personal To-Do List Application
This is a simple to-do list desktop application with a graphical user interface and SQLite backend. Users and tasks are stored in a local database, and CRUD operations are performed by users using a plain, simple & intuitive interface.
 
I created this project as a way to apply and further develop the software development skills I have been learning to a project that can be useful and easily understood by friends, colleagues and peers. With this project I wanted to focus on GUI (Tkinter) and SQL/CRUD skills, as well as the logic required to navigate the various user views of a graphical application (vs. traditional beginner-level CLI programs).

The interface is quite unexciting, as I mostly wanted to build something that works, but I feel I learned many foundational skills/concepts to build simple, useful tools as this one.  I wish to further develop my GUI skills, and translate those skills to web applications, using HTML/CSS/JavaScript and frameworks such as Bootstrap & Django instead of Python's Tkinter package.

## Tutorial
Upon launching the application, the user is greeted with the option to create a new user or view existing users.

![image](https://user-images.githubusercontent.com/64344879/131795365-d95e80da-5cc5-4714-95e0-0010ebe4b2b0.png)


Creating a new user prompts an alert that the user was successfully created.


![image](https://user-images.githubusercontent.com/64344879/131795493-aea06664-8a77-499a-8db5-f0e4e6306fce.png)


The user is then taken to the current tasks page, which displays all current tasks for that user and their completion status. Users can add, edit, delete, or update the status of a task, or switch users.

![image](https://user-images.githubusercontent.com/64344879/131795732-9d6fbab2-12ad-4a99-8ab7-b32885e337c8.png)


Updating the status of a task prompts an alert window to confirm successful updating of the task.


![image](https://user-images.githubusercontent.com/64344879/131796594-7baebb0a-ccde-44d7-9b5e-32ddbe243569.png)



Any feedback on how to improve this project would be greatly appreciated. Notable limitations include my methodology for matching tasks to users via non-unique identifiers (username vs user/task id), which I intend to fix in future updates.
