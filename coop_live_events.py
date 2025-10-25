import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import pytz

url = "https://www.cooplive.com/events"
tz = pytz.timezone("Europe/London")

r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

cal = Calendar()
cal.add("prodid", "-//Co-Op Live Events Calendar//mxm.dk//")
cal.add("version", "2.0")

# You may need to inspect the website and adjust these selectors
events = soup.select(".event-item")
for ev in events:
    title_tag = ev.select_one(".event-title")
    date_tag = ev.select_one(".event-date")
    time_tag = ev.select_one(".event-time")
    
    if not title_tag or not date_tag:
        continue
    
    title = title_tag.get_text(strip=True)
    date_str = date_tag.get_text(strip=True)
    time_str = time_tag.get_text(strip=True) if time_tag else "20:00"
    
    dt = datetime.strptime(f"{date_str} {time_str}", "%d %b %Y %H:%M")
    dt = tz.localize(dt)
    
    event = Event()
    event.add("summary", title)
    event.add("dtstart", dt)
    event.add("dtend", dt)
    cal.add_component(event)

with open("Co-op_Live_Events.ics", "wb") as f:
    f.write(cal.to_ical())

print("Co-Op Live calendar generated.")
