from datetime import datetime, timedelta

# Define the events
events = [
    {"title": "Meeting A", "start": "09:00", "end": "10:30"},
    {"title": "Workshop B", "start": "10:00", "end": "11:30"},
    {"title": "Presentation C", "start": "10:30", "end": "12:00"},
    {"title": "Lunch Break", "start": "12:00", "end": "13:00"},
]

# Helper to convert time strings to datetime objects
def parse_time(t):
    return datetime.strptime(t, "%H:%M")

# Sort events by start time
sorted_events = sorted(events, key=lambda e: parse_time(e["start"]))

# Detect conflicts
def detect_conflicts(events):
    conflicts = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            start_i = parse_time(events[i]["start"])
            end_i = parse_time(events[i]["end"])
            start_j = parse_time(events[j]["start"])
            end_j = parse_time(events[j]["end"])
            if start_j < end_i:
                conflicts.append((events[i]["title"], events[j]["title"]))
    return conflicts

# Suggest alternative time slot for a conflicting event
def suggest_slot(event, all_events, day_start="08:00", day_end="18:00"):
    duration = parse_time(event["end"]) - parse_time(event["start"])
    occupied = [(parse_time(e["start"]), parse_time(e["end"])) for e in all_events if e["title"] != event["title"]]
    occupied.sort()
    current = parse_time(day_start)
    end_of_day = parse_time(day_end)

    for start, end in occupied:
        if current + duration <= start:
            return current.strftime("%H:%M"), (current + duration).strftime("%H:%M")
        current = max(current, end)

    if current + duration <= end_of_day:
        return current.strftime("%H:%M"), (current + duration).strftime("%H:%M")
    return None

# Display sorted schedule
print("📅 Sorted Schedule:")
for e in sorted_events:
    print(f"- {e['title']}: {e['start']} - {e['end']}")

# Display conflicts
conflicts = detect_conflicts(sorted_events)
print("\n⚠ Conflicting Events:")
for c1, c2 in conflicts:
    print(f"- {c1} and {c2}")

# Suggest resolution for "Workshop B"
workshop = next(e for e in events if e["title"] == "Workshop B")
new_slot = suggest_slot(workshop, events)
print("\n✅ Suggested Resolution:")
if new_slot:
    print(f"- Reschedule 'Workshop B' to Start: {new_slot[0]}, End: {new_slot[1]}")
else:
    print("- No available slot found for 'Workshop B'")