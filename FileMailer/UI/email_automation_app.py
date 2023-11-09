import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Here is how you can implement the tabbed interface in Tkinter using the `ttk.Notebook` widget.

import tkinter as tk
from tkinter import ttk

class EmailAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Automation Program")
        self.setup_menu()
        self.setup_tabs()

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Settings", command=self.show_settings)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def show_preferences(self):
        # Placeholder for showing preferences dialog
        print("Preferences dialog placeholder")

    def show_settings(self):
        # Placeholder for showing settings dialog
        print("Settings dialog placeholder")

    def show_about(self):
        print("About dialog placeholder")

    def setup_tabs(self):
        # Create the tab control
        tab_control = ttk.Notebook(self.root)

        # Define the tabs
        self.template_files_tab = ttk.Frame(tab_control)
        self.contacts_departments_tab = ttk.Frame(tab_control)
        self.preview_tab = ttk.Frame(tab_control)
        self.progress_tab = ttk.Frame(tab_control)

        # Add tabs to the tab control
        tab_control.add(self.template_files_tab, text='Templates & Files')
        tab_control.add(self.contacts_departments_tab, text='Contacts & Departments')
        tab_control.add(self.preview_tab, text='Preview')
        tab_control.add(self.progress_tab, text='Progress')

        # Pack to make visible
        tab_control.pack(expand=1, fill="both")

    def run(self):
        self.root.mainloop()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = EmailAutomationApp(root)
    app.run()
