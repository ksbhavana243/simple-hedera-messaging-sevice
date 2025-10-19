import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Sample events
events = [
    {"title": "Meeting A", "start": "09:00", "end": "10:30"},
    {"title": "Workshop B", "start": "10:00", "end": "11:30"},
    {"title": "Presentation C", "start": "10:30", "end": "12:00"},
    {"title": "Lunch Break", "start": "12:00", "end": "13:00"},
]

# Default working hours
WORK_START = "08:00"
WORK_END = "18:00"

def parse_time(t):
    return datetime.strptime(t, "%H:%M")

def format_time(t):
    return t.strftime("%H:%M")

def detect_conflicts(events):
    conflicts = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            start_i = parse_time(events[i]["start"])
            end_i = parse_time(events[i]["end"])
            start_j = parse_time(events[j]["start"])
            end_j = parse_time(events[j]["end"])
            if start_j < end_i and end_j > start_i:
                conflicts.append((events[i], events[j]))
    return conflicts

def suggest_slot(event, all_events, work_start, work_end):
    duration = parse_time(event["end"]) - parse_time(event["start"])
    occupied = [(parse_time(e["start"]), parse_time(e["end"])) for e in all_events if e["title"] != event["title"]]
    occupied.sort()
    current = parse_time(work_start)
    end_of_day = parse_time(work_end)

    for start, end in occupied:
        if current + duration <= start:
            return format_time(current), format_time(current + duration)
        current = max(current, end)

    if current + duration <= end_of_day:
        return format_time(current), format_time(current + duration)
    return None

# GUI setup
root = tk.Tk()
root.title("Event Scheduler")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

event_widgets = {}

def draw_schedule():
    canvas.delete("all")
    y = 20
    for event in events:
        label = tk.Label(canvas, text=f"{event['title']}: {event['start']} - {event['end']}", bg="lightblue")
        canvas.create_window(300, y, window=label)
        event_widgets[event["title"]] = label
        y += 40

def show_conflicts():
    conflicts = detect_conflicts(events)
    if conflicts:
        msg = "Conflicts detected:\n"
        for e1, e2 in conflicts:
            msg += f"- {e1['title']} and {e2['title']}\n"
        messagebox.showwarning("Conflicts", msg)
    else:
        messagebox.showinfo("No Conflicts", "No conflicts detected.")

def resolve_conflict():
    for e1, e2 in detect_conflicts(events):
        slot = suggest_slot(e2, events, WORK_START, WORK_END)
        if slot:
            e2["start"], e2["end"] = slot
    draw_schedule()
    messagebox.showinfo("Resolved", "Conflicts resolved with suggested slots.")

def set_working_hours():
    global WORK_START, WORK_END
    start = start_entry.get()
    end = end_entry.get()
    try:
        parse_time(start)
        parse_time(end)
        WORK_START, WORK_END = start, end
        messagebox.showinfo("Updated", f"Working hours set to {start} - {end}")
    except:
        messagebox.showerror("Invalid Time", "Please enter time in HH:MM format.")

# Controls
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="Show Conflicts", command=show_conflicts).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="Resolve Conflicts", command=resolve_conflict).grid(row=0, column=1, padx=5)

tk.Label(control_frame, text="Work Start:").grid(row=1, column=0)
start_entry = tk.Entry(control_frame)
start_entry.insert(0, WORK_START)
start_entry.grid(row=1, column=1)

tk.Label(control_frame, text="Work End:").grid(row=2, column=0)
end_entry = tk.Entry(control_frame)
end_entry.insert(0, WORK_END)
end_entry.grid(row=2, column=1)

tk.Button(control_frame, text="Set Working Hours", command=set_working_hours).grid(row=3, column=0, columnspan=2, pady=5)

draw_schedule()
root.mainloop()