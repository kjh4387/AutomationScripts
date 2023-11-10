# Here is how you can implement the tabbed interface in Tkinter using the `ttk.Notebook` widget.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from application_controller import ApplicationController
from logger import Logger
import os
import logging
import asyncio
import threading

import queue

config_path = './config.json'
default_template_path = './defaulttemplate.txt'

class EmailAutomationApp:
    def __init__(self, root, controller: ApplicationController, logger: Logger):
        self.root = root
        self.setup_menu()
        self.message_queue = queue.Queue()
        self.check_queue()
        self.root.title("Email Automation Program")
        self.controller = controller
        self.logger = logger   
        self.logger.set_app(self)
        self.current_template_path = self.controller.get_current_template_path()
        tkinter_handler = TkinterLogHandler(self)
        self.setup_tabs()

        self.controller.config_manager.set('contact_data','./contacts.csv')
        self.controller.config_manager.set('department_data','./departments.csv')
        
        
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
        self.show_smtp_config_window()

    def show_about(self):
        messagebox.showinfo("about", "Auto Emailer. made by 김자현.\n mail:wkgusdl21@gmail.com\n ver:0.8")
        

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
        self.setup_contacts_tab()
        self.setup_departments_tab()


    def setup_mailing_tab(self):
        

        # Template Editor Section

        subject_label = ttk.Label(self.mailing_tab, text="Subject:")
        subject_label.pack(side='top', fill='x', padx=5, pady=2)
        self.subject_entry = ttk.Entry(self.mailing_tab)
        self.subject_entry.bind("<FocusOut>", self.on_subject_change)
        self.subject_entry.pack(side='top', fill='x', padx=5, pady=2)
        self.load_saved_subject()

        template_editor_label = ttk.Label(self.mailing_tab, text="Template Editor")
        template_editor_label.pack(anchor='nw')
        self.template_editor = tk.Text(self.mailing_tab, height=10)
        self.template_editor.bind("<KeyRelease>", self.on_template_change)
        self.template_editor.bind("<FocusOut>", self.on_template_change)
        self.template_editor.pack(fill='x', expand=True)
    

        self.load_current_template()
       
        self.variable_inputs_frame = ttk.Frame(self.mailing_tab)
        self.variable_inputs_frame.pack(fill='x', padx=5, pady=5)  # Pack the frame into the mailing tab

        self.on_template_change()
        
        
        self.load_variable_inputs()
        buttons_frame = ttk.Frame(self.mailing_tab)
        buttons_frame.pack(fill='x', padx=5, pady=5)  # Pack the frame into the mailing tab


        # Load Template Button
        self.load_template_button = ttk.Button(buttons_frame, text="Load Template", command=self.load_template)
        self.load_template_button.pack(side = 'left', padx = 2)
        
        # Save Template Button
        self.save_template_button = ttk.Button(buttons_frame, text="Save Template", command=self.save_template)
        self.save_template_button.pack(side = 'left', padx = 2)

        self.preview_button = ttk.Button(buttons_frame, text="Preview", command=self.preview_template)
        self.preview_button.pack(side='top', pady=5)



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
        self.log_viewer = tk.Text(self.mailing_tab, height=5, state='disabled')
        self.log_viewer.pack(fill='x', expand=True)
                
        # Controls for Sending Emails
        send_controls_frame = ttk.Frame(self.mailing_tab)
        send_controls_frame.pack(fill='x', expand=True)

        self.send_button = ttk.Button(send_controls_frame, text="Send Emails", command=self.send_emails)
        self.send_button.pack(side='right')

        self.send_all_button = ttk.Button(send_controls_frame, text="Send All", command=self.send_all_emails)
        self.send_all_button.pack(side='top', pady=5)

    def update_log(self, message):
        """ Append a message to the log viewer. """
        self.log_viewer.config(state='normal')
        self.log_viewer.insert('end', message + '\n')
        self.log_viewer.config(state='disabled')
        self.log_viewer.see('end')  # Auto-scroll to the end

    def log_message(self, message):
        """ Thread-safe way to log a message. """
        self.root.after(0, lambda: self.update_log(message))

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
            display_text = f"{file} - {department_name} - {file_info['receiver']} - {email_address}"
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

    def setup_variable_inputs(self, placeholders):
        # Clear the previous variable inputs
        for widget in self.variable_inputs_frame.winfo_children():
            widget.destroy()

        # Create an entry for each placeholder
        self.variable_entries = {}
        for placeholder in placeholders:
            if placeholder not in ['department', 'receiver']:  # Skip automatic variables
                label = ttk.Label(self.variable_inputs_frame, text=f"{placeholder}:")
                label.pack(side='top', fill='x', padx=5, pady=2)
                entry = ttk.Entry(self.variable_inputs_frame)
                entry.placeholder_name = placeholder  # Set custom attribute
                self.variable_entries[placeholder] = entry
                entry.bind("<FocusOut>", self.on_variable_input_change)  # Bind the event
                text = self.controller.config_manager.get(f"template_variable_{placeholder}")
                if text:
                    entry.insert(0, text)
                entry.pack(side='top', fill='x', padx=5, pady=2)
                
    def on_template_change(self, event=None):
        # Get template content
        template_content = self.template_editor.get("1.0", tk.END)

        # Find placeholders in the template content
        placeholders = self.controller.template_manager.find_placeholders(template_content)

        # Setup variable inputs
        self.setup_variable_inputs(placeholders)

    def on_subject_change(self, event):
        self.controller.config_manager.set("subject",event.widget.get())
    
    def load_saved_subject(self):
        saved_value = self.controller.config_manager.get(f"subject")
        if saved_value is not None:
            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, saved_value)

    def on_variable_input_change(self, event):
        # Get the placeholder name from the entry widget
        placeholder = event.widget.placeholder_name
        # Save the current value to the configuration
        self.controller.config_manager.set(f"template_variable_{placeholder}", event.widget.get())

    def get_subject_entry(self):
        return self.subject_entry

    def get_variable_inputs(self):
        """Collect user inputs for each template variable."""
        variable_data = {}
        for variable, entry in self.variable_entries.items():
            variable_data[variable] = entry.get()
        return variable_data

    def load_current_template(self):
        if self.current_template_path:
            try:
                with open(self.current_template_path, 'r', encoding='utf-8') as f:  # Ensure the file is read with the correct encoding
                    content = f.read()
                    self.template_editor.delete('1.0', tk.END)  # Clear the existing content
                    self.template_editor.insert('1.0', content)  # Insert new content
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {e}")
                self.logger.log(f"Failed to load template: {e}", level=logging.ERROR)
        else:
            messagebox.showinfo("Info", "No template file is currently selected or file does not exist. new template is made")
            with open("./template.txt",'w') as file:
                pass
            self.logger.log("No template file is currently selected or file does not exist.", level=logging.INFO)

    def load_variable_inputs(self):
        # Load the variable inputs from the configuration
        for placeholder, entry in self.variable_entries.items():
            saved_value = self.controller.config_manager.get(f"template_variable_{placeholder}")
            if saved_value is not None:
                entry.delete(0, tk.END)
                entry.insert(0, saved_value)

    def load_template(self):
            self.current_template_path = filedialog.askopenfilename(
                initialdir=self.controller.config_manager.get('template_directory', './'),
                title="Select template",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )
            try:
                with open(self.current_template_path, 'r', encoding='utf-8') as f:  # Ensure the file is read with the correct encoding
                    content = f.read()
                    self.template_editor.delete('1.0', tk.END)  # Clear the existing content
                    self.template_editor.insert('1.0', content)  # Insert new content
                    controller.config_manager.set('current_template_path',self.current_template_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {e}")
                self.logger.log(f"Failed to load template: {e}", level=logging.ERROR)
        

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

    def preview_template(self):
        # Extract the content from the template editor
        template_content = self.template_editor.get("1.0", tk.END)

        # Get the variable inputs from the user
        variable_data = self.get_variable_inputs()

        # Prepare the template with actual variable data
        preview_content = self.controller.template_manager.prepare_template(
            template_content,
            **variable_data  # Unpack the dictionary as keyword arguments
        )

        if preview_content:
            # Create a top-level window for the preview
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Template Preview")
            preview_text = tk.Text(preview_window, wrap='word', height=20, width=80)
            preview_text.pack(expand=True, fill='both')
            preview_text.insert('1.0', preview_content)
            preview_text.config(state='disabled')  # Make the text read-only
        else:
            messagebox.showerror("Error", "Failed to prepare template for preview.")


    def send_emails(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "No files selected.")
            return

        # Start a new thread for the email sending tasks
        threading.Thread(target=self._send_emails_sync, args=(selected_indices,), daemon=True).start()

    def _send_emails_sync(self, selected_indices):
        failed_emails = []
        total_emails = len(selected_indices)
        for count,index in enumerate(selected_indices, start=1):
            file_info = self.files_listbox.get(index)
            filename, department, receiver, email = file_info.split(' - ')
            variable_data = self.get_variable_inputs()
            template_content = self.template_editor.get("1.0", tk.END)
            prepared_content = self.controller.template_manager.prepare_template(
                template_content,
                department=department,
                receiver=receiver,
                **variable_data
            )
            if prepared_content:
                subject = self.subject_entry.get()
                try:
                    self.controller.email_manager.send_email(email, subject, prepared_content,os.path.abspath(os.path.join(self.controller.config_manager.get('directory'),filename)))
                    logger.log(f"mail has been send. {email},{subject}")
                    # Update the GUI or progress bar in the main thread, if necessary
                except ValueError as e:
                    self.message_queue.put(str(e))
                    break
                except Exception as e:
                    failed_emails.append(email)  # Keep track of failed emails
                    self.message_queue.put(f"Failed to send email for {filename}: {e}")
                    continue
            progress = int((count / total_emails) * 100)
            self.root.after(0, lambda p=progress: self.update_progress(p))
        self.root.after(0, self.reset_progress)
        
    def update_progress(self, value):
        """ Update the progress bar value. """
        self.progress_bar['value'] = value

    def reset_progress(self):
        """ Reset the progress bar to 0. """
        self.progress_bar['value'] = 0

    def send_all_emails(self):
        # Start a new thread for the email sending tasks for all files
        threading.Thread(target=self._send_all_emails_sync, daemon=True).start()

    def _send_all_emails_sync(self):
        all_files = [self.files_listbox.get(idx) for idx in range(self.files_listbox.size())]
        failed_emails = []
        total_emails = len(all_files)
        for count,file_info in enumerate(all_files, start=1):
            filename, department, receiver, email = file_info.split(' - ')
            variable_data = self.get_variable_inputs()
            template_content = self.template_editor.get("1.0", tk.END)
            prepared_content = self.controller.template_manager.prepare_template(
                template_content,
                department=department,
                receiver=receiver,
                **variable_data
            )
            if prepared_content:
                subject = self.subject_entry.get()
                try:
                    self.controller.email_manager.send_email(email, subject, prepared_content,os.path.abspath(os.path.join(self.controller.config_manager.get('directory'),filename)))
                    # Update the GUI or progress bar in the main thread, if necessary
                except ValueError as e:
                    self.message_queue.put(str(e))
                    break
                except Exception as e:
                    failed_emails.append(email)  # Keep track of failed emails
                    self.message_queue.put(f"Failed to send email for {filename}: {e}")
                    continue
            else:
                # Update the GUI in the main thread
                pass
        # Inform the user that the task is done
            progress = int((count / total_emails) * 100)
            self.root.after(0, lambda p=progress: self.update_progress(p))
        self.root.after(0, self.reset_progress)
        self.root.after(0, lambda: messagebox.showinfo("Done", "Finished sending all emails."))

    def check_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            messagebox.showerror("Error", message)
        # Check the queue again after some delay
        self.root.after(500, self.check_queue)

    def get_variable_inputs(self):
        """Collect user inputs for each template variable."""
        variable_data = {}
        for variable, entry in self.variable_entries.items():
            variable_data[variable] = entry.get()
        return variable_data
    
    def extract_department_and_receiver(self, filename):
        # Implement the logic to extract department and receiver from the filename
        # This is just a placeholder logic; adjust it to match your filename format
        parts = filename.split('_')
        department = parts[0]
        receiver = parts[1]
        return department, receiver

    def prompt_file_select(self):
        return filedialog.askopenfile()
    
    # In your main.py, within the EmailAutomationApp class:

    def setup_contacts_tab(self):
        # Contacts List
        contacts_list_label = ttk.Label(self.contacts_tab, text="Contacts List")
        contacts_list_label.pack(anchor='nw')
        self.contacts_listbox = tk.Listbox(self.contacts_tab, height=15)
        self.contacts_listbox.pack(fill='both', expand=True)

        # Contact Details Form
        details_frame = ttk.Frame(self.contacts_tab)
        details_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(details_frame, text="Name:").grid(row=0, column=0)
        self.contact_name_entry = ttk.Entry(details_frame)
        self.contact_name_entry.grid(row=0, column=1)
        ttk.Label(details_frame, text="Email:").grid(row=1, column=0)
        self.contact_email_entry = ttk.Entry(details_frame)
        self.contact_email_entry.grid(row=1, column=1)


        import_button = ttk.Button(self.contacts_tab, text="Import Contacts", command=self.import_contacts)
        import_button.pack(side='top', pady=5)

        # Contact Management Buttons
        buttons_frame = ttk.Frame(self.contacts_tab)
        buttons_frame.pack(fill='x', pady=5)
        self.add_contact_button = ttk.Button(buttons_frame, text="Add", command=self.add_contact)
        self.add_contact_button.grid(row=0, column=0)
        self.edit_contact_button = ttk.Button(buttons_frame, text="Edit", command=self.edit_contact)
        self.edit_contact_button.grid(row=0, column=1)
        self.delete_contact_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_contact)
        self.delete_contact_button.grid(row=0, column=2)

        self.contacts_listbox.bind('<<ListboxSelect>>', self.on_contact_select)

    # Load the initial contacts list
        self.load_contacts()

    def import_contacts(self):
        filepath = filedialog.askopenfilename(
            title="Import Contacts",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filepath:
            success = self.controller.import_contacts_from_csv(filepath)
            if success:
                messagebox.showinfo("Success", "Contacts imported successfully.")
                self.load_contacts()  # Refresh the contacts list
            else:
                messagebox.showerror("Error", "Failed to import contacts.")

    # Define the load_contacts method to populate the contacts listbox
    
    def add_contact(self):
        contact_details = {
            'name': self.contact_name_entry.get(),
            'email': self.contact_email_entry.get(),
        }
        self.controller.add_contact(contact_details)
        self.load_contacts()  # Refresh the contacts list

    def edit_contact(self):
        selected = self.contacts_listbox.curselection()
        if selected:
            original_name = self.contacts_listbox.get(selected[0]).split(':')[0]
            contact_details = {
                'name': self.contact_name_entry.get(),
                'email': self.contact_email_entry.get(),
            }
            self.controller.edit_contact(original_name, contact_details)
            self.load_contacts()  # Refresh the contacts list

    def delete_contact(self):
        selected = self.contacts_listbox.curselection()
        if selected:
            contact_name = self.contacts_listbox.get(selected[0]).split(':')[0]
            self.controller.delete_contact(contact_name)
            self.load_contacts()  # Refresh the contacts list

    def load_contacts(self):
        self.contacts_listbox.delete(0, tk.END)  # Clear the listbox
        contacts = self.controller.get_all_contacts()
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, contact)
        # Load the last selected contact if there's one saved
        last_selected_contact = self.controller.config_manager.get('last_selected_contact')
        if last_selected_contact:
            index = contacts.index(last_selected_contact)
            self.contacts_listbox.select_set(index)
            self.contacts_listbox.event_generate("<<ListboxSelect>>")
    
    def save_contacts(self):
        self.controller.save_contacts()

    def on_contact_select(self, event):
        # Get the index of the selected line in the listbox
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)

            # Assuming data is in the format 'DEPTCodeName: Email'
            details = data.split(': ')
            if len(details) == 2:
                dept_code_name, email = details
                # Further split 'DEPTCodeName' if necessary to populate fields
                # ... Your split logic here ...

                # Populate the entry fields with the contact's details
                self.contact_name_entry.delete(0, tk.END)
                self.contact_name_entry.insert(0, dept_code_name)
                self.contact_email_entry.delete(0, tk.END)
                self.contact_email_entry.insert(0, email)

    def setup_departments_tab(self):
        # Departments List
        departments_list_label = ttk.Label(self.departments_tab, text="Departments List")
        departments_list_label.pack(anchor='nw')
        self.departments_listbox = tk.Listbox(self.departments_tab, height=15)
        self.departments_listbox.pack(fill='both', expand=True)

        # Department Details Form
        details_frame = ttk.Frame(self.departments_tab)
        details_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(details_frame, text="Code:").grid(row=0, column=0)
        self.department_code_entry = ttk.Entry(details_frame)
        self.department_code_entry.grid(row=0, column=1)
        ttk.Label(details_frame, text="Name:").grid(row=1, column=0)
        self.department_name_entry = ttk.Entry(details_frame)
        self.department_name_entry.grid(row=1, column=1)

        import_button = ttk.Button(self.departments_tab, text="Import Departments", command=self.import_departments)
        import_button.pack(side='top', pady=5)

        # Department Management Buttons
        buttons_frame = ttk.Frame(self.departments_tab)
        buttons_frame.pack(fill='x', pady=5)
        self.add_department_button = ttk.Button(buttons_frame, text="Add", command=self.add_department)
        self.add_department_button.grid(row=0, column=0)
        self.edit_department_button = ttk.Button(buttons_frame, text="Edit", command=self.edit_department)
        self.edit_department_button.grid(row=0, column=1)
        self.delete_department_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_department)
        self.delete_department_button.grid(row=0, column=2)

        self.departments_listbox.bind('<<ListboxSelect>>', self.on_department_select)

        # Load the initial departments list
        self.load_departments()
    
    def import_departments(self):
        filepath = filedialog.askopenfilename(
            title="Import Departments",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filepath:
            success = self.controller.import_departments_from_csv(filepath)
            if success:
                messagebox.showinfo("Success", "Departments imported successfully.")
                self.load_departments()  # Refresh the contacts list
            else:
                messagebox.showerror("Error", "Failed to import Departments.")

    def load_departments(self):
        self.departments_listbox.delete(0, tk.END)  # Clear the listbox
        departments = self.controller.get_all_departments()
        for department in departments:
            self.departments_listbox.insert(tk.END, department)

    def add_department(self):
        department_details = {
            'code': self.department_code_entry.get(),
            'name': self.department_name_entry.get(),
        }
        self.controller.add_department(department_details)
        self.load_departments()  # Refresh the departments list

    def edit_department(self):
        selected = self.departments_listbox.curselection()
        if selected:
            original_name = self.departments_listbox.get(selected[0]).split(':')[0]
            department_details = {
                'code': self.department_code_entry.get(),
                'name': self.department_name_entry.get(),
            }
            self.controller.edit_department(original_name, department_details)
            self.load_departments()  # Refresh the contacts list

    def delete_department(self):
        selected = self.departments_listbox.curselection()
        if selected:
            contact_name = self.departments_listbox.get(selected[0]).split(':')[0]
            self.controller.delete_department(contact_name)
            self.load_departments()  # Refresh the contacts list
        
        
    def save_departments(self):
        # Calls the controller to save all departments
        self.controller.save_department()

    def clear_department_entries(self):
        self.department_code_entry.delete(0, tk.END)
        self.department_name_entry.delete(0, tk.END)

    def on_department_select(self, event):
    # Get the index of the selected line in the listbox
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)

            # Assuming data is in the format 'DEPTCodeName: Email'
            details = data.split(': ')
            if len(details) == 2:
                dept_code_name, email = details
                # Further split 'DEPTCodeName' if necessary to populate fields
                # ... Your split logic here ...

                # Populate the entry fields with the contact's details
                self.department_code_entry.delete(0, tk.END)
                self.department_code_entry.insert(0, dept_code_name)
                self.department_name_entry.delete(0, tk.END)
                self.department_name_entry.insert(0, email)
    # ... rest of the class remains the same ...

    def show_smtp_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("SMTP Configuration")

        # SMTP server entry
        tk.Label(config_window, text="SMTP Server:").grid(row=0, column=0, sticky="e")
        smtp_server_entry = tk.Entry(config_window)
        smtp_server_entry.grid(row=0, column=1)

        # SMTP port entry
        tk.Label(config_window, text="SMTP Port:").grid(row=1, column=0, sticky="e")
        smtp_port_entry = tk.Entry(config_window)
        smtp_port_entry.grid(row=1, column=1)

        # SMTP user entry
        tk.Label(config_window, text="SMTP User:").grid(row=2, column=0, sticky="e")
        smtp_user_entry = tk.Entry(config_window)
        smtp_user_entry.grid(row=2, column=1)

        # SMTP password entry
        tk.Label(config_window, text="SMTP Password:").grid(row=3, column=0, sticky="e")
        smtp_password_entry = tk.Entry(config_window, show="*")
        smtp_password_entry.grid(row=3, column=1)

        # Load existing configuration
        smtp_config = self.controller.config_manager.get_email_config()
        smtp_server_entry.insert(0, smtp_config.get("smtp_server", ""))
        smtp_port_entry.insert(0, smtp_config.get("smtp_port", ""))
        smtp_user_entry.insert(0, smtp_config.get("smtp_user", ""))
        smtp_password_entry.insert(0, smtp_config.get("smtp_password", ""))

        # Save button
        save_button = tk.Button(config_window, text="Save",
                                command=lambda: self.save_smtp_config(
                                    smtp_server_entry.get(),
                                    smtp_port_entry.get(),
                                    smtp_user_entry.get(),
                                    smtp_password_entry.get(),
                                    config_window))
        save_button.grid(row=4, column=1, sticky="ew")

        # Cancel button
        cancel_button = tk.Button(config_window, text="Cancel", command=config_window.destroy)
        cancel_button.grid(row=4, column=0, sticky="ew")


    def save_smtp_config(self, server, port, user, password, window):
        # Basic validation for the SMTP settings
        if not server:
            messagebox.showerror("Error", "SMTP server is required.")
            return
        if not port.isdigit():
            messagebox.showerror("Error", "SMTP port must be a number.")
            return
        if not user:
            messagebox.showerror("Error", "SMTP user is required.")
            return
        if not password:
            messagebox.showerror("Error", "SMTP password is required.")
            return

        # Save the SMTP settings using the ConfigurationManager
        try:
            self.controller.config_manager.set("smtp_server", server)
            self.controller.config_manager.set("smtp_port", int(port))  # Port should be saved as an integer
            self.controller.config_manager.set("smtp_user", user)
            self.controller.config_manager.set_email_credentials(user, password)  # Save password securely
            self.controller.config_manager.save_config()

            # Give user feedback and close the configuration window
            messagebox.showinfo("SMTP Configuration", "SMTP settings saved successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save SMTP settings: {e}")

    def log_message(self, message):
        """ Thread-safe way to log a message. """
        self.root.after(0, lambda: self.update_log(message))

    def update_log(self, message):
        """ Append a message to the log viewer. """
        self.log_viewer.config(state='normal')
        self.log_viewer.insert('end', message + '\n')
        self.log_viewer.config(state='disabled')
        self.log_viewer.see('end')  # Auto-scroll to the end

class TkinterLogHandler(logging.Handler):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def emit(self, record):
        log_entry = self.format(record)
        self.app.log_message(log_entry)

if __name__ == "__main__":
    root = tk.Tk()
    logger = Logger("./log")
    controller = ApplicationController(config_path, logger)
    app = EmailAutomationApp(root, controller, logger)
    app.run()