# Here is how you can implement the tabbed interface in Tkinter using the `ttk.Notebook` widget.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from application_controller import ApplicationController
from logger import Logger

config_path = 'FileMailer/config.json'

class EmailAutomationApp:
    def __init__(self, root, controller: ApplicationController, logger: Logger):
        self.root = root
        self.root.title("Email Automation Program")
        self.controller = controller
        self.logger = logger
        self.current_template_path = self.controller.get_current_template_path()
        
        self.setup_menu()
        self.setup_tabs()
        
        pass
    
    def run(self):
        self.root.mainloop()

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
        tab_control = ttk.Notebook(self.root)

        # Rename template_files_tab to mailing_tab
        self.mailing_tab = ttk.Frame(tab_control)
        self.contacts_tab = ttk.Frame(tab_control)
        self.departments_tab = ttk.Frame(tab_control)

        # Add renamed mailing_tab to the notebook control
        tab_control.add(self.mailing_tab, text='Mailing')
        tab_control.add(self.contacts_tab, text='Contacts')
        tab_control.add(self.departments_tab, text='Departments')

        tab_control.pack(expand=1, fill="both")

        # Call methods to populate each tab
        self.setup_mailing_tab()
        #self.setup_contacts_tab()
        #self.setup_departments_tab()


    def setup_mailing_tab(self):

        # Template Editor Section
        template_editor_label = ttk.Label(self.mailing_tab, text="Template Editor")
        template_editor_label.pack(anchor='nw')
        self.template_editor = tk.Text(self.mailing_tab, height=10)
        self.template_editor.pack(fill='x', expand=True)
        self.load_current_template()

        buttons_frame = ttk.Frame(self.mailing_tab)
        buttons_frame.pack(fill='x', padx=5, pady=5)  # Pack the frame into the mailing tab


        # Load Template Button
        self.load_template_button = ttk.Button(buttons_frame, text="Load Template", command=self.load_template)
        self.load_template_button.pack(side = 'left', padx = 2)
        
        # Save Template Button
        self.save_template_button = ttk.Button(buttons_frame, text="Save Template", command=self.save_template)
        self.save_template_button.pack(side = 'left', padx = 2)



        # Folder Select Section
        
        folder_select_frame = ttk.Frame(self.mailing_tab)
        folder_select_frame.pack(fill='x', expand=True)


        self.select_folder_button = ttk.Button(folder_select_frame, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side='right')

        # File List Section
        files_label = ttk.Label(self.mailing_tab, text="Files to Send")
        files_label.pack(anchor='nw')
        self.files_listbox = tk.Listbox(self.mailing_tab, height=10)
        self.files_listbox.pack(fill='x', expand=True)
        self.load_initial_folder()

        
        
         # Progress Section
        progress_label = ttk.Label(self.mailing_tab, text="Progress")
        progress_label.pack(anchor='nw')
        self.progress_bar = ttk.Progressbar(self.mailing_tab, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill='x', expand=True)
        self.progress_log = tk.Text(self.mailing_tab, height=5, state='disabled')
        self.progress_log.pack(fill='x', expand=True)
                
        # Controls for Sending Emails
        send_controls_frame = ttk.Frame(self.mailing_tab)
        send_controls_frame.pack(fill='x', expand=True)

        self.send_button = ttk.Button(send_controls_frame, text="Send Emails", command=self.send_emails)
        self.send_button.pack(side='right')

    def load_initial_folder(self):
        directory = self.controller.config_manager.config_data["directory"]
        if directory:
            success = self.controller.update_file_directory(directory)
            if success:
                self.refresh_file_list()
                self.controller.config_manager.set('directory',directory)
            else:
                messagebox.showerror("Error", "Failed to update the directory.")
    
    def select_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            success = self.controller.update_file_directory(directory)
            if success:
                self.refresh_file_list()
                self.controller.config_manager.set('directory',directory)
            else:
                messagebox.showerror("Error", "Failed to update the directory.")

    def refresh_file_list(self):
        self.files_listbox.delete(0, tk.END)  # Clear the current list
        files = self.controller.get_file_list()
        for file in files:
            file_info = self.controller.get_file_details(file)
            department_name = self.controller.get_department_name(file_info['department_code'])
            email_address = self.controller.get_contact_email(file_info['department_code'], file_info['receiver'])
            display_text = f"{file} - {department_name} - {file_info['receiver']} ({email_address})"
            self.files_listbox.insert(tk.END, display_text)  # Populate the listbox with formatted file info


    def update_template_preview(self):
        # Assume there are text fields or other widgets to input variables like manager_info, etc.
        manager_info = self.manager_info_entry.get()
        post_start_date = self.post_start_date_entry.get()
        post_end_date = self.post_end_date_entry.get()
        
        # Get the template content from the text editor widget
        template_content = self.template_editor.get("1.0", tk.END)
        
        # Replace placeholders in the template content with actual values
        preview_content = template_content.format(
            manager_info=manager_info,
            post_start_date=post_start_date,
            post_end_date=post_end_date
        )
        
        # Update a label or text widget with the preview content
        self.template_preview_display.config(text=preview_content)

    def load_current_template(self):
        with open(self.current_template_path) as f:
            if f is not None:
                for line in f:
                    self.template_editor.insert('1.0', line)

    def load_template(self):
            template_name = filedialog.askopenfilename(
                initialdir=self.controller.config_manager.get('template_directory', './'),
                title="Select template",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )
            if template_name:
                template_content = self.controller.get_current_template_path()
                if template_content is not None:
                    self.template_editor.delete('1.0', tk.END)
                    self.template_editor.insert('1.0', template_content)

    def save_template(self):
        if self.current_template_path:
            # Save to the current template path
            content = self.template_editor.get('1.0', tk.END)
            success = self.controller.template_manager.save_template(self.current_template_path,content)
            self.show_save_result(success)
        else:
            # If no current template path, use "Save As"
            self.save_template_as()

    def save_template_as(self):
        filepath = filedialog.asksaveasfilename(
            # ... existing parameters ...
        )
        if filepath:
            content = self.template_editor.get('1.0', tk.END)
            success = self.controller.template_manager.save_template(filepath, content)
            self.show_save_result(success)
            if success:
                # Update the current template path in both GUI and ConfigurationManager
                self.current_template_path = filepath
                self.controller.config_manager.set_current_template_path(filepath)

    def show_save_result(self, success):
        if success:
            messagebox.showinfo("Success", "Template saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to save the template.")

    def send_emails(self):
        selected_files = [self.files_listbox.get(idx) for idx in self.files_listbox.curselection()]
        template_content = self.template_editor.get('1.0', tk.END)
        # Call the controller to send the emails
        self.controller.send_emails(template_content, selected_files)
        # Update the GUI with progress

    def prompt_file_select(self):
        return filedialog.askopenfile()
    
    def get_department(self):
        #will make function to guide select csv files.
        pass

    def get_concacts(self):
        pass
        
    # ... rest of the class remains the same ...

if __name__ == "__main__":
    root = tk.Tk()
    logger = Logger("./log")
    controller = ApplicationController(config_path, logger)
    app = EmailAutomationApp(root, controller, logger)
    app.run()