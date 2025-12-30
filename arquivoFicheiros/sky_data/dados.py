from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from datetime import date, timedelta


eph = load('de421.bsp')
ts = load.timescale()

# Anniversary date
next_anniversary = date(year = 2026, month = 3, day = 18)
previous_anniversary = date(year = 2025, month = 3, day = 18)

# Planets
planets = {
    'Mercury': eph['mercury'],
    'Venus': eph['venus'],
    'Earth': eph['earth'],
    'Mars': eph['mars'],
    'Jupiter': eph['jupiter barycenter'],
    'Saturn': eph['saturn barycenter']
}

# Store data
all_positions = []

delta = timedelta(days=1)
current = previous_anniversary

all_positions = {}
while current <= next_anniversary:
    t = ts.utc(current.year, current.month, current.day)
    day_data = {}
    for name, planet in planets.items():
        pos = eph['sun'].at(t).observe(planet).frame_latlon(ecliptic_frame)
        day_data[name] = pos[1].degrees  # ecliptic longitude
    all_positions[str(current)] = day_data
    current += delta

# Save to JSON for p5.js
import json
with open('planet_positions.json', 'w') as f:
    json.dump(all_positions, f, indent=2)
