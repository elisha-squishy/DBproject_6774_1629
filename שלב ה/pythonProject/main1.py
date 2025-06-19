from tkinter import *
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, select, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ---------- SQLAlchemy Setup ----------
Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    event_location = Column(String)

class VisitingEvent(Base):
    __tablename__ = 'visiting_event'
    resident_id = Column(Integer, ForeignKey('resident.residentid'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.event_id'), primary_key=True)

class Resident(Base):
    __tablename__ = 'resident'
    residentid = Column(Integer, primary_key=True)
    roomid = Column(Integer, ForeignKey('room.room_id'))
    firstname = Column(String(30))
    lastname = Column(String(30))
    dateofbirth = Column(Date)

# Replace with your actual DB credentials
DATABASE_URL = "postgresql://sibony:ds2006@localhost:5432/backupChaim"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# ---------- Tkinter GUI ----------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Resident Event Viewer")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        title = Label(root, text="Welcome to the Elderly Home System", font=("David", 20), bg="#f0f0f0")
        title.pack(pady=30)

        resident_button = Button(root, text="Go to Resident View", font=("David", 14), command=self.open_resident_view)
        resident_button.pack(pady=20)

    def open_resident_view(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Resident View")
        self.new_window.geometry("950x900")
        self.new_window.configure(bg="#e6f2ff")

        Label(self.new_window, text="Enter Resident ID or Name", font=("Helvetica", 14), bg="#e6f2ff").pack(pady=10)

        self.id_entry = Entry(self.new_window, font=("Helvetica", 12))
        self.id_entry.pack(pady=5)

        self.name_entry = Entry(self.new_window, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        search_button = Button(self.new_window, text="Search Resident and View Events", command=self.display_top_events)
        search_button.pack(pady=20)

        # Top 5 Events
        self.top_frame = LabelFrame(self.new_window, text="Top 5 Events", font=("Helvetica", 12), bg="white", padx=10,
                                    pady=10)
        self.top_frame.pack(pady=10, fill='both', expand=True)

        self.top_tree = ttk.Treeview(self.top_frame, columns=("Event Name", "Visitors"), show='headings', height=5)
        self.top_tree.heading("Event Name", text="Event Name")
        self.top_tree.heading("Visitors", text="Number of Visitors")
        self.top_tree.pack(fill='both', expand=True)
        self.top_tree.bind("<<TreeviewSelect>>", lambda e: self.on_event_select(self.top_tree))

        # All Events
        self.all_frame = LabelFrame(self.new_window, text="All Events", font=("Helvetica", 12), bg="white", padx=10,
                                    pady=10)
        self.all_frame.pack(pady=10, fill='both', expand=True)

        self.all_tree = ttk.Treeview(self.all_frame, columns=("Event Name", "Date", "Location"), show='headings',
                                     height=8)
        self.all_tree.heading("Event Name", text="Event Name")
        self.all_tree.heading("Date", text="Date")
        self.all_tree.heading("Location", text="Location")
        self.all_tree.pack(fill='both', expand=True)
        self.all_tree.bind("<<TreeviewSelect>>", lambda e: self.on_event_select(self.all_tree))

        # Joined Events
        self.joined_frame = LabelFrame(self.new_window, text="Events You've Joined", font=("Helvetica", 12), bg="white",
                                       padx=10, pady=10)
        self.joined_frame.pack(pady=10, fill='both', expand=True)

        self.joined_tree = ttk.Treeview(self.joined_frame, columns=("Event Name", "Date", "Location"), show='headings',
                                        height=6)
        self.joined_tree.heading("Event Name", text="Event Name")
        self.joined_tree.heading("Date", text="Date")
        self.joined_tree.heading("Location", text="Location")
        self.joined_tree.pack(fill='both', expand=True)
        self.joined_tree.bind("<<TreeviewSelect>>", lambda e: self.on_event_select(self.joined_tree))

        # Buttons
        self.selected_event_id = None
        btn_frame = Frame(self.new_window, bg="#e6f2ff")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Join Selected Event", command=self.join_event).grid(row=0, column=0, padx=10)
        Button(btn_frame, text="Unjoin Selected Event", command=self.unjoin_event).grid(row=0, column=1, padx=10)

    # def display_top_events(self):
    #     self.resident_id = None
    #     resident_id = self.id_entry.get().strip()
    #     name = self.name_entry.get().strip().lower()
    #
    #     # Validate resident
    #     if resident_id.isdigit():
    #         resident = session.query(Resident).filter_by(residentid=int(resident_id)).first()
    #     elif name:
    #         parts = name.split()
    #         if len(parts) >= 2:
    #             resident = session.query(Resident).filter(
    #                 func.lower(Resident.firstname) == parts[0],
    #                 func.lower(Resident.lastname) == parts[1]
    #             ).first()
    #         else:
    #             resident = None
    #     else:
    #         messagebox.showerror("Input Error", "Please enter either Resident ID or full name (first and last).")
    #         return
    #
    #     if not resident:
    #         messagebox.showerror("Resident Not Found", "No resident found with that ID or name.")
    #         return
    #
    #     self.resident_id = resident.residentid
    #
    #     stmt = (
    #         session.query(
    #             Event.event_id,
    #             Event.event_name,
    #             func.count(VisitingEvent.resident_id).label("num_visitors")
    #         )
    #         .join(VisitingEvent, Event.event_id == VisitingEvent.event_id)
    #         .group_by(Event.event_id, Event.event_name)
    #         .order_by(func.count(VisitingEvent.resident_id).desc())
    #         .limit(5)
    #     )
    #
    #     results = stmt.all()
    #
    #     for row in self.tree.get_children():
    #         self.tree.delete(row)
    #
    #     for event_id, event_name, num_visitors in results:
    #         self.tree.insert("", "end", iid=event_id, values=(event_name, num_visitors))

    def display_top_events(self):
        self.resident_id = None
        resident_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip().lower()

        # Validate resident
        if resident_id.isdigit():
            resident = session.query(Resident).filter_by(residentid=int(resident_id)).first()
        elif name:
            parts = name.split()
            if len(parts) >= 2:
                resident = session.query(Resident).filter(
                    func.lower(Resident.firstname) == parts[0],
                    func.lower(Resident.lastname) == parts[1]
                ).first()
            else:
                resident = None
        else:
            messagebox.showerror("Input Error", "Please enter either Resident ID or full name (first and last).")
            return

        if not resident:
            messagebox.showerror("Resident Not Found", "No resident found with that ID or name.")
            return

        self.resident_id = resident.residentid

        # Top 5 Events
        top_stmt = (
            session.query(
                Event.event_id,
                Event.event_name,
                func.count(VisitingEvent.resident_id).label("num_visitors")
            )
            .join(VisitingEvent, Event.event_id == VisitingEvent.event_id)
            .group_by(Event.event_id, Event.event_name)
            .order_by(func.count(VisitingEvent.resident_id).desc())
            .limit(5)
        )

        for row in self.top_tree.get_children():
            self.top_tree.delete(row)

        for event_id, event_name, num_visitors in top_stmt.all():
            self.top_tree.insert("", "end", iid=event_id, values=(event_name, num_visitors))

        # All Events
        all_events = session.query(Event).order_by(Event.event_date).all()

        for row in self.all_tree.get_children():
            self.all_tree.delete(row)

        for event in all_events:
            self.all_tree.insert("", "end", iid=event.event_id,
                                 values=(event.event_name, event.event_date, event.event_location))
        self.display_top_events()
        self.display_joined_events()

    def display_joined_events(self):
        if self.resident_id is None:
            return

        for row in self.joined_tree.get_children():
            self.joined_tree.delete(row)

        joined_events = (
            session.query(Event)
            .join(VisitingEvent, Event.event_id == VisitingEvent.event_id)
            .filter(VisitingEvent.resident_id == self.resident_id)
            .order_by(Event.event_date)
            .all()
        )

        for event in joined_events:
            self.joined_tree.insert("", "end", iid=event.event_id,
                                    values=(event.event_name, event.event_date, event.event_location))
    def on_event_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_event_id = int(selected[0])
        else:
            self.selected_event_id = None

    def join_event(self):
        if self.selected_event_id is None or self.resident_id is None:
            messagebox.showwarning("Selection Missing", "Please select an event and search for a resident first.")
            return

        # Check if already joined
        existing = session.query(VisitingEvent).filter_by(
            resident_id=self.resident_id, event_id=self.selected_event_id
        ).first()
        if existing:
            messagebox.showinfo("Already Joined", "You are already joined to this event.")
            return

        try:
            new_entry = VisitingEvent(resident_id=self.resident_id, event_id=self.selected_event_id)
            session.add(new_entry)
            session.commit()
            messagebox.showinfo("Success", "You have joined the event.")
            self.display_top_events()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Database Error", str(e))

    def unjoin_event(self):
        if self.selected_event_id is None or self.resident_id is None:
            messagebox.showwarning("Selection Missing", "Please select an event and search for a resident first.")
            return

        entry = session.query(VisitingEvent).filter_by(
            resident_id=self.resident_id, event_id=self.selected_event_id
        ).first()
        if entry:
            try:
                session.delete(entry)
                session.commit()
                messagebox.showinfo("Success", "You have left the event.")
                self.display_top_events()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showinfo("Not Joined", "You are not currently joined to this event.")


# ---------- Run ----------
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()