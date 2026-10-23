#!/usr/bin/env python3
"""Collect regulator RSS/Atom feeds into updates.json for the IND AMICUS LEGAL website.
Standard library only. Runs daily via GitHub Actions (see README.md).
"""
import json, re, sys, html, time, urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# (label shown on website, feed URL)
FEEDS = [
    ("SEBI", "https://www.sebi.gov.in/sebirss.xml"),
    ("RBI", "https://www.rbi.org.in/notifications_rss.xml"),
    ("RBI", "https://www.rbi.org.in/pressreleases_rss.xml"),
]
MAX_ITEMS = 40
UA = {"User-Agent": "Mozilla/5.0 (compatible; IndAmicusLegal-UpdateBot/1.0; +mailto:info@indamicus.com)",
      "Accept": "application/rss+xml, application/xml, text/xml, */*"}

def fetch(url, tries=3):
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(5 * (n + 1))
    raise last
# SEBI: keep circulars, regulations, master circulars and press releases; skip enforcement/recovery/appeal orders.
SEBI_KEEP = ("/legal/", "/media-and-notifications/press-releases/")
# RBI press releases: skip routine market operations and bank-specific enforcement notices.
NOISE = re.compile(
    r"money market operations|variable rate|repo|underwriting|auction|reserve money|treasury bill|"
    r"sovereign gold bond|result of|government securities|ways and means|monetary penalty|imposes|"
    r"cancellation of licen|directions under section 35a|weekly statistical|forex reserves|money supply|liquidity",
    re.I)

def text(el, *names):
    for n in names:
        f = el.find(n)
        if f is not None and (f.text or "").strip():
            return f.text.strip()
    return ""

def parse_date(s):
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

def clean(s, n=240):
    s = html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(s or "")))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"

def read_feed(label, url):
    root = ET.fromstring(fetch(url))
    atom, out = "{http://www.w3.org/2005/Atom}", []
    for it in list(root.iter("item")) + list(root.iter(atom + "entry")):
        title = text(it, "title", atom + "title")
        link = text(it, "link")
        if not link:
            l = it.find(atom + "link")
            link = l.get("href", "") if l is not None else ""
        when = parse_date(text(it, "pubDate", atom + "updated", atom + "published"))
        t = clean(title, 200)
        summ = clean(text(it, "description", atom + "summary"))
        if summ.lower() == t.lower() or t.lower().startswith(summ.lower().rstrip("…")):
            summ = ""
        if t and link:
            out.append({"source": label, "title": t, "url": link,
                        "date": when.date().isoformat() if when else "", "summary": summ})
    return out

def keep(i):
    path = urlparse(i["url"]).path
    if path in ("", "/"):            # curated seed items that link to a portal home page
        return True
    if i["source"] == "SEBI":
        return any(p in i["url"] for p in SEBI_KEEP) and "last amended" not in i["title"].lower()
    if i["source"] == "RBI":
        return not NOISE.search(i["title"])
    return True

def main():
    fresh, errors = [], []
    for label, url in FEEDS:
        try:
            fresh += read_feed(label, url)
        except Exception as e:
            errors.append(f"{label} {url}: {e}")
    for e in errors:
        print("::warning::Feed problem - " + e)
    if errors and len(errors) == len(FEEDS):
        print("::warning::All feeds failed this time; keeping the previous updates.json.")
        return
    try:
        with open("updates.json", encoding="utf-8") as f:
            existing = json.load(f).get("items", [])
    except Exception:
        existing = []
    today = datetime.now(timezone.utc).date().isoformat()
    merged, seen = [], set()
    for i in existing + fresh:        # existing first, so first-seen dates are kept
        if i["url"] in seen:
            continue
        seen.add(i["url"])
        if not i.get("date"):
            i["date"] = today
        if keep(i):
            merged.append(i)
    merged.sort(key=lambda x: x["date"], reverse=True)
    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": merged[:MAX_ITEMS]}
    with open("updates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(data['items'])} items.", ("Errors: " + "; ".join(errors)) if errors else "")

if __name__ == "__main__":
    main()
