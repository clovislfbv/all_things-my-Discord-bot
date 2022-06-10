import requests as r
import json
from datetime import datetime
import pytz

lastdlday = None
lastedt = None

def edt():
    global lastdlday, lastedt

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if lastdlday is not None and (today-lastdlday).days <= 0:
        return lastedt

    resp = r.post(
        "https://zeus.ionis-it.com/api/reservation/filter/displayable",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbG92aXMubGVmZWJ2cmUiLCJ1bmlxdWVfbmFtZSI6ImNsb3Zpcy5sZWZlYnZyZSIsImp0aSI6ImIwMDUyMTMxLTk3Y2ItNGQxNC04ZGQ5LWYzYTRkMjExN2Q2NSIsImlhdCI6MTYzNjA0MjY0NCwibmJmIjoxNjM2MDQyNjQ0LCJyb2wiOiJWSVNJVE9SIiwiZ3JvdXBzIjoiW10iLCJpZF9zY2hvb2wiOiIxIiwiZXhwIjoxNjM2MTI5MDQ0LCJpc3MiOiJaZXVzIiwiYXVkIjoiemV1cy1hcHAifQ.gdWKeQIXtKI-lWBWSp0IXD4ve4XVgmyzl2mevsSBX-s",
            "Content-Type": "application/json",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "referrer": "https://zeus.ionis-it.com/home",
        },
        data=json.dumps(
            {
                "groups": [55],
                "rooms": [],
                "teachers": [],
                "startDate": today.isoformat(),
                "endDate": today.replace(
                    hour=23, minute=59
                ).isoformat(),
            }
        ),
    )

    result = resp.json()
    text = ""

    for course in result:
        text += course["name"] + "\n"
        text += (
            datetime.fromisoformat(course["startDate"][:-1]).strftime("%H:%M")
            + " - "
            + datetime.fromisoformat(course["endDate"][:-1]).strftime("%H:%M")
            + "\n"
        )
        text += (
            "Salles: " + ", ".join(map((lambda x: x["name"]), course["rooms"])) + "\n\n"
        )

    lastedt = text
    lastdlday = today

    return text

