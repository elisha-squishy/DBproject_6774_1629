import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import numpy as np


class DatabaseConnection:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def execute_query(self, query, params=None):
        """Execute a query and return results (if any)"""
        try:
            with self.Session() as session:
                result = session.execute(text(query), params or {})
                # Commit only if it's not a SELECT query
                if query.strip().lower().startswith("insert") or query.strip().lower().startswith("delete"):
                    session.commit()
                    return None
                return result.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def execute_procedure(self, procedure_name, params=None):
        """Execute a stored procedure"""
        try:
            with self.Session() as session:
                if params:
                    query = f"CALL {procedure_name}({', '.join([':' + str(k) for k in params.keys()])})"
                    session.execute(text(query), params)
                else:
                    session.execute(text(f"CALL {procedure_name}()"))
                session.commit()
                return True
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return False


class ModernStyle:
    """Modern styling configuration"""
    PRIMARY_COLOR = "#2E3440"
    SECONDARY_COLOR = "#3B4252"
    ACCENT_COLOR = "#5E81AC"
    SUCCESS_COLOR = "#A3BE8C"
    WARNING_COLOR = "#EBCB8B"
    ERROR_COLOR = "#BF616A"
    TEXT_COLOR = "#ECEFF4"
    BG_COLOR = "#2E3440"
    CARD_BG = "#434C5E"

    @staticmethod
    def configure_ttk_style():
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('Modern.TFrame', background=ModernStyle.BG_COLOR)
        style.configure('Card.TFrame', background=ModernStyle.CARD_BG, relief='raised', borderwidth=1)
        style.configure('Modern.TLabel', background=ModernStyle.BG_COLOR, foreground=ModernStyle.TEXT_COLOR,
                        font=('Segoe UI', 10))
        style.configure('Header.TLabel', background=ModernStyle.BG_COLOR, foreground=ModernStyle.TEXT_COLOR,
                        font=('Segoe UI', 16, 'bold'))
        style.configure('Modern.TButton', font=('Segoe UI', 10))
        style.configure('Modern.TEntry', font=('Segoe UI', 10))
        style.configure('Modern.Treeview', font=('Segoe UI', 9))
        style.configure('Modern.Treeview.Heading', font=('Segoe UI', 10, 'bold'))



class MainApplication:
    def __init__(self, root, db_connection):
        self.root = root
        self.db = db_connection
        self.current_frame = None

        # Configure main window
        self.root.title("Old Age Home Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernStyle.BG_COLOR)

        # Configure styles
        ModernStyle.configure_ttk_style()

        # Show main menu
        self.show_main_menu()

    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        """Display main menu with navigation buttons"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(self.current_frame, text="Old Age Home Management System",
                                style='Header.TLabel', font=('Segoe UI', 24, 'bold'))
        title_label.pack(pady=(0, 50))

        # Button frame
        button_frame = ttk.Frame(self.current_frame, style='Modern.TFrame')
        button_frame.pack(expand=True)

        # Navigation buttons
        buttons = [
            ("Resident View", self.show_resident_view, ModernStyle.ACCENT_COLOR),
            ("Janitor View", self.show_janitor_view, ModernStyle.SUCCESS_COLOR),
            ("Family View", self.show_family_view, ModernStyle.WARNING_COLOR),
            ("Manager Dashboard", self.show_manager_dashboard, ModernStyle.ERROR_COLOR)
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                            font=('Segoe UI', 14, 'bold'), fg='white', bg=color,
                            width=20, height=3, relief='flat', cursor='hand2')
            btn.pack(pady=10)

            # Hover effects
            def on_enter(e, btn=btn, color=color):
                btn.configure(bg=self.lighten_color(color))

            def on_leave(e, btn=btn, color=color):
                btn.configure(bg=color)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def lighten_color(self, color):
        """Lighten a hex color for hover effect"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.1)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def create_back_button(self, parent):
        """Create a back button"""
        back_btn = tk.Button(parent, text="← Back to Main Menu", command=self.show_main_menu,
                             font=('Segoe UI', 10), bg=ModernStyle.SECONDARY_COLOR, fg=ModernStyle.TEXT_COLOR,
                             relief='flat', cursor='hand2')
        back_btn.pack(anchor='nw', padx=10, pady=10)
        return back_btn

    def show_resident_view(self):
        """Display resident view page"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.current_frame.pack(fill='both', expand=True)

        self.create_back_button(self.current_frame)

        # Title
        title_label = ttk.Label(self.current_frame, text="Resident Portal",
                                style='Header.TLabel', font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 20))

        # Main container
        main_container = ttk.Frame(self.current_frame, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Left panel - Sign in and events
        left_panel = ttk.Frame(main_container, style='Card.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Sign in section
        signin_frame = ttk.LabelFrame(left_panel, text="Sign In", style='Modern.TFrame')
        signin_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(signin_frame, text="Resident ID:", style='Modern.TLabel').pack(anchor='w', padx=5, pady=2)
        self.resident_entry = ttk.Entry(signin_frame, style='Modern.TEntry', width=30)
        self.resident_entry.pack(fill='x', padx=5, pady=5)

        signin_btn = tk.Button(signin_frame, text="Sign In", command=self.resident_signin,
                               bg=ModernStyle.ACCENT_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        signin_btn.pack(pady=5)

        # Current resident display
        self.current_resident_label = ttk.Label(signin_frame, text="Not signed in",
                                                style='Modern.TLabel', font=('Segoe UI', 10, 'italic'))
        self.current_resident_label.pack(pady=5)

        # Events section
        events_frame = ttk.LabelFrame(left_panel, text="All Events", style='Modern.TFrame')
        events_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Search bar
        search_frame = ttk.Frame(events_frame, style='Modern.TFrame')
        search_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(search_frame, text="Search:", style='Modern.TLabel').pack(side='left')
        self.event_search = ttk.Entry(search_frame, style='Modern.TEntry')
        self.event_search.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.event_search.bind('<KeyRelease>', self.filter_events)

        # Events listbox
        self.events_listbox = tk.Listbox(events_frame, font=('Segoe UI', 10),
                                         bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_COLOR)
        self.events_listbox.pack(fill='both', expand=True, padx=5, pady=5)

        # Join/Unjoin button
        join_btn = tk.Button(events_frame, text="Join/Unjoin Event", command=self.toggle_event_participation,
                             bg=ModernStyle.SUCCESS_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        join_btn.pack(pady=5)

        # Right panel - Statistics and recommendations
        right_panel = ttk.Frame(main_container, style='Card.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Top 5 events
        top_events_frame = ttk.LabelFrame(right_panel, text="Top 5 Most Popular Events", style='Modern.TFrame')
        top_events_frame.pack(fill='x', padx=10, pady=10)

        self.top_events_tree = ttk.Treeview(top_events_frame, columns=('Event', 'Visitors'), show='headings', height=6)
        self.top_events_tree.heading('Event', text='Event Name')
        self.top_events_tree.heading('Visitors', text='Visitors')
        self.top_events_tree.pack(fill='x', padx=5, pady=5)

        # Recommended events
        recommended_frame = ttk.LabelFrame(right_panel, text="Recommended Events", style='Modern.TFrame')
        recommended_frame.pack(fill='x', padx=10, pady=10)

        self.recommended_table = ttk.Treeview(recommended_frame, columns=('Date', 'Location', 'Residents'),
                                              show='headings', height=6)
        # Define column headings
        self.recommended_table.heading('Date', text='Date')
        self.recommended_table.heading('Location', text='Location')
        self.recommended_table.heading('Residents', text='Residents in Your Age Group Going')

        # Set column widths and alignment (optional)
        self.recommended_table.column('Date', width=100, anchor='center')
        self.recommended_table.column('Location', width=150, anchor='center')
        self.recommended_table.column('Residents', width=200, anchor='center')
        self.recommended_table.pack(fill='both', expand=True)

        # Joined events
        joined_frame = ttk.LabelFrame(right_panel, text="Your Joined Events", style='Modern.TFrame')
        joined_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.joined_listbox = tk.Listbox(joined_frame, font=('Segoe UI', 10),
                                         bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_COLOR)
        self.joined_listbox.pack(fill='both', expand=True, padx=5, pady=5)

        # Load initial data
        self.load_top_events()
        self.load_all_events()

        self.current_resident_id = None

    def resident_signin(self):
        """Handle resident sign in"""
        identifier = self.resident_entry.get().strip()
        if not identifier:
            messagebox.showwarning("Warning", "Please enter a resident ID or name")
            return

        # Try to find resident by ID or name
        if identifier.isdigit():
            query = "SELECT residentid, firstname, lastname FROM resident WHERE residentid = :id"
            params = {'id': int(identifier)}
        # else:
        #     query = "SELECT residentid, firstname, lastname FROM resident WHERE firstname ILIKE :name OR lastname ILIKE :name OR (firstname || ' ' || lastname) ILIKE :name"
        #     params = {'name': f'%{identifier}%'}

        results = self.db.execute_query(query, params)

        if results:
            resident = results[0]
            self.current_resident_id = resident[0]
            self.current_resident_label.config(text=f"Signed in as: {resident[1]} {resident[2]}")
            self.load_resident_events()
            self.load_recommend_events()
        else:
            messagebox.showerror("Error", "Resident not found")

    def load_top_events(self):
        """Load top 5 most visited events"""
        query = """
        SELECT 
            e.event_name,
            COUNT(ve.resident_id) AS num_visitors
        FROM 
            event e
        JOIN 
            visiting_event ve ON e.event_id = ve.event_id
        GROUP BY 
            e.event_id, e.event_name
        ORDER BY 
            num_visitors DESC
        LIMIT 5
        """

        results = self.db.execute_query(query)

        # Clear existing items
        for item in self.top_events_tree.get_children():
            self.top_events_tree.delete(item)

        # Add new items
        for row in results:
            self.top_events_tree.insert('', 'end', values=row)

    def load_all_events(self):
        """Load all events for the listbox"""
        query = "SELECT event_id, event_name, event_date, event_location FROM event ORDER BY event_date"
        results = self.db.execute_query(query)

        self.all_events = results
        self.display_events(results)

    def display_events(self, events):
        """Display events in the listbox"""
        self.visible_events = events  # NEW LINE
        self.events_listbox.delete(0, tk.END)
        for event in events:
            display_text = f"{event[1]} - {event[2]} at {event[3]}"
            self.events_listbox.insert(tk.END, display_text)

    def filter_events(self, event=None):
        """Filter events based on search term"""
        search_term = self.event_search.get().lower()
        if not search_term:
            self.display_events(self.all_events)
        else:
            filtered_events = [e for e in self.all_events if search_term in e[1].lower()]
            self.display_events(filtered_events)

    def toggle_event_participation(self):
        """Join or unjoin an event"""
        if not self.current_resident_id:
            messagebox.showwarning("Warning", "Please sign in first")
            return

        selection = self.events_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an event")
            return

        # Get the selected event
        search_term = self.event_search.get().lower()
        if search_term:
            filtered_events = [e for e in self.all_events if search_term in e[1].lower()]
            selected_event = filtered_events[selection[0]]
        else:
            selected_event = self.all_events[selection[0]]

        event_id = selected_event[0]

        # Check if already joined
        check_query = "SELECT * FROM visiting_event WHERE resident_id = :rid AND event_id = :eid"
        existing = self.db.execute_query(check_query, {'rid': self.current_resident_id, 'eid': event_id})

        if existing:
            # Unjoin
            delete_query = "DELETE FROM visiting_event WHERE resident_id = :rid AND event_id = :eid"
            self.db.execute_query(delete_query, {'rid': self.current_resident_id, 'eid': event_id})
            messagebox.showinfo("Success", "Left the event successfully!")
        else:
            # Join
            insert_query = "INSERT INTO visiting_event (resident_id, event_id) VALUES (:rid, :eid)"
            self.db.execute_query(insert_query, {'rid': self.current_resident_id, 'eid': event_id})
            messagebox.showinfo("Success", "Joined the event successfully!")

        self.load_resident_events()
        self.load_top_events()

    def load_resident_events(self):
        """Load events that the current resident has joined"""
        if not self.current_resident_id:
            return

        query = """
        SELECT e.event_name, e.event_date, e.event_location
        FROM event e
        JOIN visiting_event ve ON e.event_id = ve.event_id
        WHERE ve.resident_id = :rid
        ORDER BY e.event_date
        """

        results = self.db.execute_query(query, {'rid': self.current_resident_id})

        self.joined_listbox.delete(0, tk.END)
        for event in results:
            display_text = f"{event[0]} - {event[1]} at {event[2]}"
            self.joined_listbox.insert(tk.END, display_text)

    def load_recommend_events(self):
        """Load recommended events for the current resident"""
        if not self.current_resident_id:
            return

        # Try to call the stored function
        try:
            query = "SELECT * FROM recommend_events(:rid)"
            results = self.db.execute_query(query, {'rid': self.current_resident_id})

            for row in self.recommended_table.get_children():
                self.recommended_table.delete(row)
            for event in results:
                self.recommended_table.insert('', 'end', values=(event[0], event[1], event[2]))
        except:
            # If function doesn't exist, show a placeholder
            self.recommended_table.delete(0, tk.END)

    def show_janitor_view(self):
        """Display janitor view page"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.current_frame.pack(fill='both', expand=True)

        self.create_back_button(self.current_frame)

        # Title
        title_label = ttk.Label(self.current_frame, text="Janitor Portal",
                                style='Header.TLabel', font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 20))

        # Main container
        main_container = ttk.Frame(self.current_frame, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Top section - Sign in and stats
        top_section = ttk.Frame(main_container, style='Modern.TFrame')
        top_section.pack(fill='x', pady=(0, 10))

        # Sign in section
        signin_frame = ttk.LabelFrame(top_section, text="Sign In", style='Modern.TFrame')
        signin_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        ttk.Label(signin_frame, text="Caregiver ID:", style='Modern.TLabel').pack(anchor='w', padx=5, pady=2)
        self.janitor_entry = ttk.Entry(signin_frame, style='Modern.TEntry', width=30)
        self.janitor_entry.pack(fill='x', padx=5, pady=5)

        signin_btn = tk.Button(signin_frame, text="Sign In", command=self.janitor_signin,
                               bg=ModernStyle.SUCCESS_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        signin_btn.pack(pady=5)

        self.current_janitor_label = ttk.Label(signin_frame, text="Not signed in",
                                               style='Modern.TLabel', font=('Segoe UI', 10, 'italic'))
        self.current_janitor_label.pack(pady=5)

        # Stats section
        stats_frame = ttk.LabelFrame(top_section, text="Task Statistics", style='Modern.TFrame')
        stats_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        self.finished_tasks_label = ttk.Label(stats_frame, text="Finished Tasks: 0",
                                              style='Modern.TLabel', font=('Segoe UI', 12, 'bold'))
        self.finished_tasks_label.pack(pady=10)

        # Status ratio bar
        self.status_canvas = tk.Canvas(stats_frame, height=30, bg=ModernStyle.CARD_BG)
        self.status_canvas.pack(fill='x', padx=10, pady=10)

        # Bottom section - Requests and Inventory
        bottom_section = ttk.Frame(main_container, style='Modern.TFrame')
        bottom_section.pack(fill='both', expand=True)

        # Requests section
        requests_frame = ttk.LabelFrame(bottom_section, text="Maintenance Requests", style='Modern.TFrame')
        requests_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        self.requests_tree = ttk.Treeview(requests_frame, columns=('ID', 'Description', 'Status'), show='headings')
        self.requests_tree.heading('ID', text='Request ID')
        self.requests_tree.heading('Description', text='Description')
        self.requests_tree.heading('Status', text='Status')
        self.requests_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Status update button
        update_status_btn = tk.Button(requests_frame, text="Update Status", command=self.update_request_status,
                                      bg=ModernStyle.WARNING_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        update_status_btn.pack(pady=5)

        # Inventory section
        inventory_frame = ttk.LabelFrame(bottom_section, text="Inventory Management", style='Modern.TFrame')
        inventory_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Search bar for inventory
        inv_search_frame = ttk.Frame(inventory_frame, style='Modern.TFrame')
        inv_search_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(inv_search_frame, text="Search Item:", style='Modern.TLabel').pack(side='left')
        self.inventory_search = ttk.Entry(inv_search_frame, style='Modern.TEntry')
        self.inventory_search.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.inventory_search.bind('<KeyRelease>', self.filter_inventory)

        # Inventory tree
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=('ID', 'Name', 'Quantity'), show='headings')
        self.inventory_tree.heading('ID', text='Item ID')
        self.inventory_tree.heading('Name', text='Item Name')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Decrease quantity button
        decrease_btn = tk.Button(inventory_frame, text="Decrease Quantity", command=self.decrease_item_quantity,
                                 bg=ModernStyle.ERROR_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        decrease_btn.pack(pady=5)

        self.current_janitor_id = None
        self.load_inventory()

    def janitor_signin(self):
        """Handle janitor sign in"""
        identifier = self.janitor_entry.get().strip()
        if not identifier:
            messagebox.showwarning("Warning", "Please enter a caregiver ID or name")
            return

        # Try to find caregiver by ID or name
        if identifier.isdigit():
            query = "SELECT caregiverid, firstname, lastname FROM caregiver WHERE caregiverid = :id"
            params = {'id': int(identifier)}
        else:
            query = "SELECT caregiverid, firstname, lastname FROM caregiver WHERE firstname ILIKE :name OR lastname ILIKE :name OR (firstname || ' ' || lastname) ILIKE :name"
            params = {'name': f'%{identifier}%'}

        results = self.db.execute_query(query, params)

        if results:
            janitor = results[0]
            self.current_janitor_id = janitor[0]
            self.current_janitor_label.config(text=f"Signed in as: {janitor[1]} {janitor[2]}")
            self.load_janitor_requests()
            self.load_janitor_stats()
        else:
            messagebox.showerror("Error", "Caregiver not found")

    def load_janitor_requests(self):
        """Load maintenance requests for the current janitor"""
        if not self.current_janitor_id:
            return

        query = """
        SELECT request_id, req_description, req_status
        FROM caregiver_maintenance
        WHERE caregiverid = :cid
        ORDER BY request_id
        """

        results = self.db.execute_query(query, {'cid': self.current_janitor_id})

        # Clear existing items
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)

        # Add new items
        for row in results:
            self.requests_tree.insert('', 'end', values=(row[0], row[1], row[2]))

    def load_janitor_stats(self):
        """Load statistics for the current janitor"""
        if not self.current_janitor_id:
            return

        # Count finished tasks
        finished_query = """
        SELECT COUNT(*) FROM caregiver_maintenance 
        WHERE caregiverid = :cid AND req_status = 'taken care of'
        """
        finished_result = self.db.execute_query(finished_query, {'cid': self.current_janitor_id})
        finished_count = finished_result[0][0] if finished_result else 0

        self.finished_tasks_label.config(text=f"Finished Tasks: {finished_count}")

        # Load status ratio
        status_query = """
        SELECT req_status, COUNT(*) as count
        FROM caregiver_maintenance 
        WHERE caregiverid = :cid
        GROUP BY req_status
        """
        status_results = self.db.execute_query(status_query, {'cid': self.current_janitor_id})

        # Create status ratio bar
        self.draw_status_ratio(status_results)

    def draw_status_ratio(self, status_data):
        """Draw horizontal status ratio bar"""
        self.status_canvas.delete("all")

        if not status_data:
            return

        total = sum(row[1] for row in status_data)
        if total == 0:
            return

        canvas_width = self.status_canvas.winfo_width()
        canvas_height = 30

        colors = {
            'processed': ModernStyle.WARNING_COLOR,
            'received': ModernStyle.ACCENT_COLOR,
            'taken care of': ModernStyle.SUCCESS_COLOR
        }

        x = 0
        for status, count in status_data:
            width = (count / total) * canvas_width
            color = colors.get(status, ModernStyle.SECONDARY_COLOR)

            self.status_canvas.create_rectangle(x, 0, x + width, canvas_height,
                                                fill=color, outline='')

            # Add text if section is wide enough
            if width > 50:
                self.status_canvas.create_text(x + width / 2, canvas_height / 2,
                                               text=f"{status}\n{count}",
                                               fill='white', font=('Segoe UI', 8))
            x += width

    def update_request_status(self):
        """Update the status of a selected request"""
        if not self.current_janitor_id:
            messagebox.showwarning("Warning", "Please sign in first")
            return

        selection = self.requests_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a request")
            return

        item = self.requests_tree.item(selection[0])
        request_id = item['values'][0]

        # Try to call the stored procedure
        try:
            new_status = simpledialog.askstring("Request Status", "Enter the updated status")
            success = self.db.execute_procedure('update_maintenance_status',
                                                {'request_id': request_id, 'new_status': new_status})
            if success:
                messagebox.showinfo("Success", "Request status updated successfully!")
                self.load_janitor_requests()
                self.load_janitor_stats()
        except Exception as e:
            messagebox.showwarning("Warning", str(e))

    def load_inventory(self):
        """Load inventory items"""
        query = "SELECT item_id, item_name, quantity FROM inventory ORDER BY item_name"
        results = self.db.execute_query(query)

        self.all_inventory = results
        self.display_inventory(results)

    def display_inventory(self, items):
        """Display inventory items in the tree"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        # Add new items
        for row in items:
            self.inventory_tree.insert('', 'end', values=(row[0], row[1], row[2]))

    def filter_inventory(self, event=None):
        """Filter inventory based on search term"""
        search_term = self.inventory_search.get().lower()
        if not search_term:
            self.display_inventory(self.all_inventory)
        else:
            filtered_items = [item for item in self.all_inventory if search_term in item[1].lower()]
            self.display_inventory(filtered_items)

    def decrease_item_quantity(self):
        """Decrease quantity of selected inventory item"""
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return

        item = self.inventory_tree.item(selection[0])
        item_id = item['values'][0]
        current_quantity = item['values'][2]

        amount = simpledialog.askinteger("Decrease Quantity",
                                         f"Current quantity: {current_quantity}\nEnter amount to decrease:",
                                         minvalue=1, maxvalue=current_quantity)
        if amount:
            try:
                # Try to call the stored procedure
                success = self.db.execute_procedure('decrease_item_quantity',
                                                    {'item_id': item_id, 'amount': amount})
                if success:
                    messagebox.showinfo("Success", "Quantity decreased successfully!")
                    self.load_inventory()
            except:
                # Manual update
                new_quantity = current_quantity - amount
                update_query = "UPDATE inventory SET quantity = :qty WHERE item_id = :id"
                self.db.execute_query(update_query, {'qty': new_quantity, 'id': item_id})
                messagebox.showinfo("Success", "Quantity decreased successfully!")
                self.load_inventory()

    def show_family_view(self):
        """Display family view page"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.current_frame.pack(fill='both', expand=True)

        self.create_back_button(self.current_frame)

        # Title
        title_label = ttk.Label(self.current_frame, text="Family Portal",
                                style='Header.TLabel', font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 20))

        # Main container
        main_container = ttk.Frame(self.current_frame, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Top section - Sign in and resident info
        top_section = ttk.Frame(main_container, style='Modern.TFrame')
        top_section.pack(fill='x', pady=(0, 20))

        # Sign in section
        signin_frame = ttk.LabelFrame(top_section, text="Family Member Sign In", style='Modern.TFrame')
        signin_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        ttk.Label(signin_frame, text="Visitor Name:", style='Modern.TLabel').pack(anchor='w', padx=5, pady=2)
        self.family_entry = ttk.Entry(signin_frame, style='Modern.TEntry', width=30)
        self.family_entry.pack(fill='x', padx=5, pady=5)

        signin_btn = tk.Button(signin_frame, text="Sign In", command=self.family_signin,
                               bg=ModernStyle.WARNING_COLOR, fg='white', font=('Segoe UI', 10, 'bold'))
        signin_btn.pack(pady=5)

        # Resident info section
        resident_info_frame = ttk.LabelFrame(top_section, text="Resident Information", style='Modern.TFrame')
        resident_info_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        self.resident_name_label = ttk.Label(resident_info_frame, text="No resident selected",
                                             style='Header.TLabel', font=('Segoe UI', 14, 'bold'))
        self.resident_name_label.pack(pady=20)

        # Medical history section
        medical_frame = ttk.LabelFrame(main_container, text="Medical History", style='Modern.TFrame')
        medical_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Create a canvas for custom styling
        self.medical_canvas = tk.Canvas(medical_frame, bg=ModernStyle.CARD_BG, highlightthickness=0)
        medical_scrollbar = ttk.Scrollbar(medical_frame, orient="vertical", command=self.medical_canvas.yview)
        self.medical_scrollable_frame = ttk.Frame(self.medical_canvas, style='Modern.TFrame')

        self.medical_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.medical_canvas.configure(scrollregion=self.medical_canvas.bbox("all"))
        )

        self.medical_canvas.create_window((0, 0), window=self.medical_scrollable_frame, anchor="nw")
        self.medical_canvas.configure(yscrollcommand=medical_scrollbar.set)

        self.medical_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        medical_scrollbar.pack(side="right", fill="y")

        # Doctor information section
        doctor_frame = ttk.LabelFrame(main_container, text="Healthcare Team", style='Modern.TFrame')
        doctor_frame.pack(fill='x', pady=(10, 0))

        self.doctor_info_frame = ttk.Frame(doctor_frame, style='Modern.TFrame')
        self.doctor_info_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.current_visitor = None
        self.current_resident_name = None

    def family_signin(self):
        """Handle family member sign in"""
        visitor_name = self.family_entry.get().strip()
        if not visitor_name:
            messagebox.showwarning("Warning", "Please enter visitor name")
            return

        # Find resident associated with this visitor
        query = """
        SELECT DISTINCT resident_name
        FROM family_view
        WHERE visitorname ILIKE :visitor
        """

        results = self.db.execute_query(query, {'visitor': f'%{visitor_name}%'})

        if results:
            self.current_visitor = visitor_name
            self.current_resident_name = results[0][0]
            self.resident_name_label.config(text=f"Resident: {self.current_resident_name}")
            self.load_medical_history()
            self.load_doctor_info()
        else:
            messagebox.showerror("Error", "No resident found for this visitor")

    def load_medical_history(self):
        """Load and display medical history in a styled format"""
        if not self.current_resident_name:
            return

        query = """
        SELECT treatmentdate, treatmenttype
        FROM family_view
        WHERE resident_name = :resident
        ORDER BY treatmentdate DESC
        """

        results = self.db.execute_query(query, {'resident': self.current_resident_name})

        # Clear existing content
        for widget in self.medical_scrollable_frame.winfo_children():
            widget.destroy()

        if not results:
            no_data_label = ttk.Label(self.medical_scrollable_frame, text="No medical history available",
                                      style='Modern.TLabel', font=('Segoe UI', 12, 'italic'))
            no_data_label.pack(pady=20)
            return

        # Create styled medical history cards
        for i, (date, treatment) in enumerate(results):
            # Create a card frame
            card_frame = tk.Frame(self.medical_scrollable_frame, bg=ModernStyle.ACCENT_COLOR,
                                  relief='raised', borderwidth=1)
            card_frame.pack(fill='x', padx=10, pady=5)

            # Inner frame for padding
            inner_frame = tk.Frame(card_frame, bg=ModernStyle.ACCENT_COLOR)
            inner_frame.pack(fill='both', expand=True, padx=15, pady=10)

            # Date label
            date_label = tk.Label(inner_frame, text=str(date),
                                  bg=ModernStyle.ACCENT_COLOR, fg='white',
                                  font=('Segoe UI', 10, 'bold'))
            date_label.pack(anchor='w')

            # Treatment label
            treatment_label = tk.Label(inner_frame, text=treatment,
                                       bg=ModernStyle.ACCENT_COLOR, fg='white',
                                       font=('Segoe UI', 12), wraplength=400)
            treatment_label.pack(anchor='w', pady=(5, 0))

    def load_doctor_info(self):
        """Load and display doctor information"""
        if not self.current_resident_name:
            return

        query = """
        SELECT caregiver_name, caregiver_phone, treatmenttype
        FROM family_view
        WHERE resident_name = :resident
        GROUP BY caregiver_name, caregiver_phone, treatmenttype
        ORDER BY caregiver_name
        """

        results = self.db.execute_query(query, {'resident': self.current_resident_name})

        # Clear existing content
        for widget in self.doctor_info_frame.winfo_children():
            widget.destroy()

        if not results:
            no_data_label = ttk.Label(self.doctor_info_frame, text="No healthcare team information available",
                                      style='Modern.TLabel', font=('Segoe UI', 12, 'italic'))
            no_data_label.pack(pady=20)
            return

        # Group by caregiver
        caregivers = {}
        for name, phone, treatment in results:
            if name not in caregivers:
                caregivers[name] = {'phone': phone, 'treatments': []}
            caregivers[name]['treatments'].append(treatment)

        # Create styled doctor cards
        for i, (name, info) in enumerate(caregivers.items()):
            # Create a card frame
            card_frame = tk.Frame(self.doctor_info_frame, bg=ModernStyle.SUCCESS_COLOR,
                                  relief='raised', borderwidth=1)
            card_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

            # Inner frame for padding
            inner_frame = tk.Frame(card_frame, bg=ModernStyle.SUCCESS_COLOR)
            inner_frame.pack(fill='both', expand=True, padx=15, pady=15)

            # Doctor name
            name_label = tk.Label(inner_frame, text=name,
                                  bg=ModernStyle.SUCCESS_COLOR, fg='white',
                                  font=('Segoe UI', 12, 'bold'))
            name_label.pack(anchor='w')

            # Phone number
            phone_label = tk.Label(inner_frame, text=f"📞 {info['phone']}",
                                   bg=ModernStyle.SUCCESS_COLOR, fg='white',
                                   font=('Segoe UI', 10))
            phone_label.pack(anchor='w', pady=(5, 0))

            # Treatments
            treatments_text = "Specialties:\n" + "\n• ".join(info['treatments'])
            treatments_label = tk.Label(inner_frame, text=treatments_text,
                                        bg=ModernStyle.SUCCESS_COLOR, fg='white',
                                        font=('Segoe UI', 9), justify='left', wraplength=200)
            treatments_label.pack(anchor='w', pady=(10, 0))



    def show_manager_dashboard(self):
        """Display manager dashboard with statistics and charts"""
        # Simple authentication
        username, password = simple_login_dialog(self.root)
        print(username, password)
        if username != "dsibony" or password != "123":
            messagebox.showerror("Access Denied", "Invalid credentials")
            return
        print("hi")

        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, style='Modern.TFrame')
        self.current_frame.pack(fill='both', expand=True)

        self.create_back_button(self.current_frame)

        # Title
        title_label = ttk.Label(self.current_frame, text="Manager Dashboard",
                                style='Header.TLabel', font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 20))

        # Create main container with scrolling
        canvas = tk.Canvas(self.current_frame, bg=ModernStyle.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.current_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Top row - Event popularity pie chart and occupancy
        top_row = ttk.Frame(scrollable_frame, style='Modern.TFrame')
        top_row.pack(fill='x', padx=20, pady=10)

        # Event popularity pie chart
        event_frame = ttk.LabelFrame(top_row, text="Event Participation Distribution", style='Modern.TFrame')
        event_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        self.create_event_popularity_chart(event_frame)

        # Occupancy percentage
        occupancy_frame = ttk.LabelFrame(top_row, text="Occupancy Rate", style='Modern.TFrame')
        occupancy_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        self.create_occupancy_display(occupancy_frame)

        # Middle row - Event popularity over time
        middle_row = ttk.Frame(scrollable_frame, style='Modern.TFrame')
        middle_row.pack(fill='x', padx=20, pady=10)

        timeline_frame = ttk.LabelFrame(middle_row, text="Event Popularity Over Time", style='Modern.TFrame')
        timeline_frame.pack(fill='both', expand=True)

        self.create_event_timeline_chart(timeline_frame)

        # Bottom row - Problematic rooms and leaderboard
        bottom_row = ttk.Frame(scrollable_frame, style='Modern.TFrame')
        bottom_row.pack(fill='x', padx=20, pady=10)

        # Problematic rooms bar
        rooms_frame = ttk.LabelFrame(bottom_row, text="Rooms With Maintenance Requests", style='Modern.TFrame')
        rooms_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        self.create_problematic_rooms_display(rooms_frame)

        # Janitor leaderboard
        leaderboard_frame = ttk.LabelFrame(bottom_row, text="Maintenance Leaderboard", style='Modern.TFrame')
        leaderboard_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        self.create_janitor_leaderboard(leaderboard_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

    def create_event_popularity_chart(self, parent):
        """Create pie chart for event popularity"""
        query = """
        WITH event_counts AS (
    SELECT 
        resident_id,
        COUNT(event_id) AS events_visited
    FROM visiting_event
    GROUP BY resident_id
)
SELECT 
    CASE 
        WHEN COALESCE(events_visited, 0) = 0 THEN '0 events'
        WHEN COALESCE(events_visited, 0) = 1 THEN '1 event'
        WHEN COALESCE(events_visited, 0) = 2 THEN '2 events'
        ELSE '3+ events'
    END AS event_category,
    COUNT(*) AS resident_count
FROM resident r
LEFT JOIN event_counts ec ON r.residentid = ec.resident_id
GROUP BY 
    CASE 
        WHEN COALESCE(events_visited, 0) = 0 THEN '0 events'
        WHEN COALESCE(events_visited, 0) = 1 THEN '1 event'
        WHEN COALESCE(events_visited, 0) = 2 THEN '2 events'
        ELSE '3+ events'
    END
order by resident_count
        """

        results = self.db.execute_query(query)

        if not results:
            ttk.Label(parent, text="No data available", style='Modern.TLabel').pack(expand=True)
            return

        # Prepare data for pie chart
        labels = [f"{row[0]} events" for row in results]
        sizes = [row[1] for row in results]
        colors = plt.cm.Set3(np.linspace(0, 1, len(results)))

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(ModernStyle.BG_COLOR)
        ax.set_facecolor(ModernStyle.BG_COLOR)

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90)

        # Style the text
        for text in texts:
            text.set_color(ModernStyle.TEXT_COLOR)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')

        ax.set_title('Resident Event Participation', color=ModernStyle.TEXT_COLOR, fontsize=12, fontweight='bold')

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

    def create_occupancy_display(self, parent):
        """Create occupancy percentage display with circular progress"""
        query = """
        SELECT 
            ROUND(100.0 * SUM(CASE WHEN r.residentid IS NOT NULL THEN 1 ELSE 0 END)
            / COUNT(rm.roomid), 2) AS avg_occupancy_percentage
        FROM room rm
        LEFT JOIN resident r ON rm.roomid = r.roomid
        """

        results = self.db.execute_query(query)
        occupancy = results[0][0] if results else 0

        # Create canvas for circular progress
        canvas = tk.Canvas(parent, width=200, height=200, bg=ModernStyle.CARD_BG, highlightthickness=0)
        canvas.pack(expand=True, pady=20)

        # Draw circular progress
        center_x, center_y = 100, 100
        radius = 70

        # Background circle
        canvas.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           outline=ModernStyle.SECONDARY_COLOR, width=8, fill='')

        # Progress arc
        if occupancy > 0:
            extent = (occupancy / 100) * 360
            canvas.create_arc(center_x - radius, center_y - radius,
                              center_x + radius, center_y + radius,
                              start=90, extent=-extent, outline=ModernStyle.SUCCESS_COLOR,
                              width=8, style='arc')

        # Percentage text
        canvas.create_text(center_x, center_y, text=f"{occupancy}%",
                           fill=ModernStyle.TEXT_COLOR, font=('Segoe UI', 24, 'bold'))
        canvas.create_text(center_x, center_y + 30, text="Occupied",
                           fill=ModernStyle.TEXT_COLOR, font=('Segoe UI', 12))

    def create_event_timeline_chart(self, parent):
        """Create line chart for event popularity over time"""
        # Note: The original query has some issues, using a corrected version
        query = """
        SELECT
            e.event_date,
            COUNT(DISTINCT ve.resident_id) AS resident_count
        FROM event e
        LEFT JOIN visiting_event ve ON e.event_id = ve.event_id
        GROUP BY e.event_date
        ORDER BY e.event_date
        """

        results = self.db.execute_query(query)

        if not results:
            ttk.Label(parent, text="No timeline data available", style='Modern.TLabel').pack(expand=True)
            return

        # Prepare data
        dates = [row[0] for row in results]
        counts = [row[1] for row in results]

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor(ModernStyle.BG_COLOR)
        ax.set_facecolor(ModernStyle.BG_COLOR)

        ax.plot(dates, counts, color=ModernStyle.ACCENT_COLOR, linewidth=2, marker='o')
        ax.set_title('Event Participation Over Time', color=ModernStyle.TEXT_COLOR, fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', color=ModernStyle.TEXT_COLOR)
        ax.set_ylabel('Number of Participants', color=ModernStyle.TEXT_COLOR)

        # Style the axes
        ax.tick_params(colors=ModernStyle.TEXT_COLOR)
        ax.spines['bottom'].set_color(ModernStyle.TEXT_COLOR)
        ax.spines['left'].set_color(ModernStyle.TEXT_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

    def create_problematic_rooms_display(self, parent):
        """Create horizontal bar for problematic rooms"""
        query = """
        WITH req_counts AS (
            SELECT 
                room_id,
                COUNT(*) AS req_count
            FROM maintenance_req
            GROUP BY room_id
        )
        SELECT 
            CASE 
                WHEN req_count IS NULL THEN 'Less or equal 2'
                WHEN req_count <= 2 THEN 'Less or equal 2'
                WHEN req_count > 2 THEN 'More than 2'
            END AS category,
            COUNT(*) AS room_count
        FROM req_counts 
        RIGHT OUTER JOIN room ON req_counts.room_id = room.roomid
        GROUP BY category
        """

        results = self.db.execute_query(query)

        if not results:
            ttk.Label(parent, text="No room data available", style='Modern.TLabel').pack(expand=True)
            return

        # Create canvas for horizontal bar
        canvas = tk.Canvas(parent, height=100, bg=ModernStyle.CARD_BG, highlightthickness=0)
        canvas.pack(fill='x', padx=10, pady=20)

        # Calculate proportions
        total_rooms = sum(row[1] for row in results)
        if total_rooms == 0:
            return

        colors = {
            'Less or equal 2': ModernStyle.SUCCESS_COLOR,
            'More than 2': ModernStyle.ERROR_COLOR
        }

        canvas_width = canvas.winfo_reqwidth()
        x = 0

        for category, count in results:
            width = (count / total_rooms) * canvas_width
            color = colors.get(category, ModernStyle.SECONDARY_COLOR)

            canvas.create_rectangle(x, 20, x + width, 80, fill=color, outline='')

            # Add text
            if width > 50:
                canvas.create_text(x + width / 2, 50, text=f"{category}\n{count} rooms",
                                   fill='white', font=('Segoe UI', 10, 'bold'))
            x += width

    def create_janitor_leaderboard(self, parent):
        """Create janitor leaderboard display"""
        query = """
        WITH staff_requests AS (
            SELECT 
                c.caregiverid,
                c.firstname || ' ' || c.lastname as staff_name,
                d.name as department,
                COUNT(mr.request_id) AS handled_requests
            FROM caregiver c
            LEFT JOIN maintenance_req mr ON c.caregiverid = mr.staff_member_id
            LEFT JOIN department d ON c.departmentid = d.departmentid
            WHERE d.name NOT ILIKE '%Care%' AND d.name NOT ILIKE '%nursing%'
            GROUP BY c.caregiverid, c.firstname, c.lastname, d.name
        ),
        max_by_dept AS (
            SELECT department, MAX(handled_requests) as max_requests
            FROM staff_requests
            GROUP BY department
        )
        SELECT sr.staff_name, sr.department, sr.handled_requests
        FROM staff_requests sr
        JOIN max_by_dept md ON sr.department = md.department 
        AND sr.handled_requests = md.max_requests
        ORDER BY sr.handled_requests DESC, sr.department
        LIMIT 10
        """

        results = self.db.execute_query(query)

        if not results:
            ttk.Label(parent, text="No leaderboard data available", style='Modern.TLabel').pack(expand=True)
            return

        # Create scrollable frame for leaderboard
        leaderboard_canvas = tk.Canvas(parent, bg=ModernStyle.CARD_BG, highlightthickness=0)
        leaderboard_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=leaderboard_canvas.yview)
        leaderboard_scrollable = ttk.Frame(leaderboard_canvas, style='Modern.TFrame')

        leaderboard_scrollable.bind(
            "<Configure>",
            lambda e: leaderboard_canvas.configure(scrollregion=leaderboard_canvas.bbox("all"))
        )

        leaderboard_canvas.create_window((0, 0), window=leaderboard_scrollable, anchor="nw")
        leaderboard_canvas.configure(yscrollcommand=leaderboard_scrollbar.set)

        # Create leaderboard entries
        for i, (name, department, requests) in enumerate(results):
            # Determine medal/rank
            if i == 0:
                rank_symbol = "🥇"
                bg_color = "#FFD700"
            elif i == 1:
                rank_symbol = "🥈"
                bg_color = "#C0C0C0"
            elif i == 2:
                rank_symbol = "🥉"
                bg_color = "#CD7F32"
            else:
                rank_symbol = f"#{i + 1}"
                bg_color = ModernStyle.SECONDARY_COLOR

            # Create entry frame
            entry_frame = tk.Frame(leaderboard_scrollable, bg=bg_color, relief='raised', borderwidth=1)
            entry_frame.pack(fill='x', padx=5, pady=2)

            # Entry content
            content_frame = tk.Frame(entry_frame, bg=bg_color)
            content_frame.pack(fill='x', padx=10, pady=5)

            # Rank
            rank_label = tk.Label(content_frame, text=rank_symbol, bg=bg_color,
                                  font=('Segoe UI', 14, 'bold'))
            rank_label.pack(side='left')

            # Name and details
            details_frame = tk.Frame(content_frame, bg=bg_color)
            details_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))

            name_label = tk.Label(details_frame, text=name, bg=bg_color,
                                  font=('Segoe UI', 12, 'bold'), anchor='w')
            name_label.pack(fill='x')

            dept_label = tk.Label(details_frame, text=f"{department} • {requests} requests",
                                  bg=bg_color, font=('Segoe UI', 10), anchor='w')
            dept_label.pack(fill='x')

        leaderboard_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        leaderboard_scrollbar.pack(side="right", fill="y")


def main():
    """Main function to run the application"""
    # Database connection - replace with your actual connection string
    connection_string = "postgresql://sibony:ds2006@localhost:5432/backupChaim"

    try:
        db = DatabaseConnection(connection_string)

        root = tk.Tk()
        app = MainApplication(root, db)
        root.mainloop()

    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Please update the connection string with your database credentials")

        # Create a simple error window
        root = tk.Tk()
        root.title("Database Connection Error")
        root.geometry("400x200")

        error_label = tk.Label(root, text="Database Connection Error",
                               font=('Segoe UI', 16, 'bold'), fg='red')
        error_label.pack(pady=20)

        message_label = tk.Label(root, text="Please update the connection string\nwith your database credentials",
                                 font=('Segoe UI', 12), justify='center')
        message_label.pack(pady=10)

        connection_label = tk.Label(root, text="Current: postgresql://username:password@localhost:5432/old_age_home_db",
                                    font=('Segoe UI', 10), wraplength=350)
        connection_label.pack(pady=10)

        root.mainloop()

def simple_login_dialog(parent):
    """Simple login dialog that returns (username, password) or None if cancelled"""
    dialog = tk.Toplevel(parent)
    dialog.transient(parent)
    dialog.grab_set()
    dialog.title("Login")
    dialog.geometry("250x120")
    dialog.resizable(False, False)

    result = {'username': None, 'password': None, 'ok': False}

    # Username
    tk.Label(dialog, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    username_var = tk.StringVar()
    username_entry = tk.Entry(dialog, textvariable=username_var, width=20)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    # Password
    tk.Label(dialog, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    password_var = tk.StringVar()
    password_entry = tk.Entry(dialog, textvariable=password_var, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def ok_clicked():
        result['username'] = username_var.get()
        result['password'] = password_var.get()
        result['ok'] = True
        dialog.destroy()

    def cancel_clicked():
        dialog.destroy()

    button_frame = tk.Frame(dialog)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(button_frame, text="OK", command=ok_clicked).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=cancel_clicked).pack(side=tk.LEFT, padx=5)

    # Bind Enter key
    dialog.bind('<Return>', lambda e: ok_clicked())
    username_entry.focus_set()

    dialog.update_idletasks()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    window_width = dialog.winfo_width()
    window_height = dialog.winfo_height()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2) + 50
    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

    dialog.wait_window()

    return (result['username'], result['password']) if result['ok'] else None

if __name__ == "__main__":
    main()
