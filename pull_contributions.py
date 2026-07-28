"""
Pulls the public contribution calendar HTML fragment GitHub itself uses,
parses day cells into a week-by-week level grid, and writes contributions.json
for render_graph.py to draw.

No token needed - this is the same public endpoint the profile page uses.
Runs inside GitHub Actions where outbound internet is available.
"""
import json
import re
import httpx
from lxml import html

USERNAME = "yash9283"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = "assets/contributions.json"

resp = httpx.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
resp.raise_for_status()
tree = html.fromstring(resp.text)

# Each day is a <td> with class "ContributionCalendar-day" and a
# data-level attribute (0-4) plus a date in the id/data attributes.
days = tree.xpath('//td[contains(@class,"ContributionCalendar-day")]')

records = []
for d in days:
    date = d.get("data-date")
    level = d.get("data-level")
    if date is None or level is None:
        continue
    records.append({"date": date, "level": int(level)})

records.sort(key=lambda r: r["date"])

# group into weeks of 7 (GitHub's grid runs Sun-Sat, already ordered that way
# in the source markup column by column, but we resort by date then rebucket)
weeks = []
current_week = []
for i, r in enumerate(records):
    current_week.append(r["level"])
    if len(current_week) == 7:
        weeks.append(current_week)
        current_week = []
if current_week:
    weeks.append(current_week)

total = sum(r["level"] > 0 for r in records)  # active days, adjust as desired
total_contribs = None  # GitHub doesn't put the raw count on this fragment;
                        # if you want the exact number, scrape it from the
                        # profile page's h2 text separately.

# streaks
longest = cur = 0
for r in records:
    if r["level"] > 0:
        cur += 1
        longest = max(longest, cur)
    else:
        cur = 0

# current streak = trailing run of active days
streak = 0
for r in reversed(records):
    if r["level"] > 0:
        streak += 1
    else:
        break

data = {
    "weeks": weeks,
    "stats": {
        "total": total,
        "streak": streak,
        "longest": longest,
    },
}

with open(OUT, "w") as f:
    json.dump(data, f)

print(f"wrote {OUT}: {len(weeks)} weeks, streak={streak}, longest={longest}")
