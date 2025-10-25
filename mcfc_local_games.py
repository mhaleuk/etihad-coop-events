import requests
from icalendar import Calendar, Event

feeds = {
    "Mens": "http://api-prod.mancity.com/fixturecalendars/v1/DownloadCalendar?calendar=mens&lang=en",
    "Womens": "http://api-prod.mancity.com/fixturecalendars/v1/DownloadCalendar?calendar=womens&lang=en",
    "Academy": "http://api-prod.mancity.com/fixturecalendars/v1/DownloadCalendar?calendar=academy&lang=en",
    "EDS": "http://api-prod.mancity.com/fixturecalendars/v1/DownloadCalendar?calendar=eds&lang=en",
}

home_locations = {"Etihad Stadium", "Joie Stadium", "City Football Academy", "Old Trafford"}

combined_cal = Calendar()
combined_cal.add("prodid", "-//MCFC Local Games Calendar//mxm.dk//")
combined_cal.add("version", "2.0")

for name, url in feeds.items():
    r = requests.get(url)
    r.raise_for_status()
    cal = Calendar.from_ical(r.text)

    for component in cal.walk():
        if component.name == "VEVENT":
            location = component.get("location")
            if location in home_locations:
                new_event = Event()
                new_event.add("summary", component.get("summary"))
                new_event.add("dtstart", component.get("dtstart").dt)
                new_event.add("dtend", component.get("dtend").dt)
                new_event.add("location", location)
                new_event.add("description", component.get("description"))
                combined_cal.add_component(new_event)

with open("MCFC_Local_Events.ics", "wb") as f:
    f.write(combined_cal.to_ical())

print("MCFC Local Games calendar generated.")
