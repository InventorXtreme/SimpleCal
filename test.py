from icalendar_light.toolbox import Calendar
from datetime import datetime
today = datetime.today().date()
for event in Calendar.iter_events_from_file('calc.ics'):
    if event[5].date() == today:
        print(" ")
        print(event[5].date())
        print(Calendar.event_stringify(event))

print("h")
