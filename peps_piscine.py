#!/usr/bin/env python3
"""
PEPS (Université Laval) bains libres  ->  fichier .ics pour Google Agenda

用法 / Usage
  python peps_piscine.py                      # 直接从网站抓取，默认只要 13 岁以上的游泳时段
  python peps_piscine.py --type tous          # 只要 "Bains pour tous"（家庭场）
  python peps_piscine.py --type all           # 两种都要
  python peps_piscine.py --pool olympique     # 只要奥林匹克泳池
  python peps_piscine.py --min-length 25      # 只要 25m 及以上的泳道
  python peps_piscine.py --shallow            # 只要有浅水区的时段
  python peps_piscine.py --length 21          # 只要 21m 的泳道
  python peps_piscine.py --file page.html     # 网站打不开时，用浏览器另存的网页文件

依赖: pip install requests beautifulsoup4
"""

import argparse
import hashlib
import re
import sys
from datetime import date, datetime, timezone

URL = "https://peps.ulaval.ca/activite/bains-libres"
TZ = "America/Toronto"
LOCATION = "PEPS, 2300 rue de la Terrasse, Québec, QC G1V 0A6"

MOIS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9,
    "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}
JOUR_RE = re.compile(
    r"^(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\s+(\d{1,2})\s+([a-zéû]+)$",
    re.I,
)
HEURE_RE = re.compile(r"^(\d{1,2}):(\d{2})\s*à\s*(\d{1,2}):(\d{2})$")
SECTION_MARK = "l'horaire des bains libres est diffusé"
END_MARK = "plus d'informations"


def fetch():
    # 1) 先用 requests 正常抓取
    import requests
    ua = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(URL, timeout=30, headers=ua)
        r.raise_for_status()
        return r.text
    except requests.exceptions.SSLError:
        pass
    # 2) 证书出问题时，改用系统自带的 curl（它信任系统里的证书，Mac 和 Windows 都有）
    import shutil
    import subprocess
    try:
        curl = shutil.which("curl") or "/usr/bin/curl"
        out = subprocess.run(
            [curl, "-sSL", "--max-time", "30", "-A", "Mozilla/5.0", URL],
            capture_output=True, check=True,
        )
        return out.stdout.decode("utf-8", errors="replace")
    except Exception:
        pass
    # 3) 最后一招: 跳过证书验证（这只是公开的课表页面，风险很小）
    import urllib3
    urllib3.disable_warnings()
    print("提示: 证书验证未通过，已跳过验证继续抓取。")
    r = requests.get(URL, timeout=30, headers=ua, verify=False)
    r.raise_for_status()
    return r.text


def get_text(args):
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            raw = fh.read()
    else:
        raw = fetch()
    if "<html" in raw.lower() or "<div" in raw.lower():
        from bs4 import BeautifulSoup
        raw = BeautifulSoup(raw, "html.parser").get_text("\n")
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip().lstrip("#").strip().strip("*").strip()
        ln = ln.replace("\u2019", "'")
        if ln:
            lines.append(ln)
    return lines


def guess_year(month, today):
    # 网页只写日期不写年份。按离今天最近的年份来猜（跨年时也正确）
    y = today.year
    if month - today.month > 6:
        return y - 1
    if today.month - month > 6:
        return y + 1
    return y


def parse(lines, today):
    # 按 "Veuillez noter..." 把页面切成两段: 第一段是 13 ans et +，第二段是 pour tous
    starts = [i for i, l in enumerate(lines) if SECTION_MARK in l.lower()]
    end = next((i for i, l in enumerate(lines) if l.lower() == END_MARK), len(lines))
    if len(starts) < 2:
        sys.exit("没找到课表，网页结构可能变了。")
    sections = [("longueurs", starts[0], starts[1]), ("tous", starts[1], end)]

    events = []
    for kind, a, b in sections:
        block = lines[a:b]
        cur_day = None
        i = 0
        while i < len(block):
            l = block[i]
            m = JOUR_RE.match(l)
            if m:
                d, mon = int(m.group(2)), MOIS.get(m.group(3).lower())
                if mon:
                    cur_day = date(guess_year(mon, today), mon, d)
                i += 1
                continue
            if l == "Heure" and cur_day and i + 1 < len(block):
                h = HEURE_RE.match(block[i + 1])
                if not h:
                    i += 1
                    continue
                ev = {
                    "kind": kind,
                    "day": cur_day,
                    "start": (int(h.group(1)), int(h.group(2))),
                    "end": (int(h.group(3)), int(h.group(4))),
                    "note": [], "info": [], "config": [],
                }
                j, field = i + 2, "note"
                while j < len(block):
                    t = block[j]
                    if t == "Heure" or JOUR_RE.match(t) or SECTION_MARK in t.lower():
                        break
                    if t == "Informations":
                        field = "info"
                    elif t == "Configuration":
                        field = "config"
                    else:
                        ev[field].append(t)
                    j += 1
                events.append(ev)
                i = j
                continue
            i += 1
    return events


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    # iCalendar 规定每行不超过 75 字节
    out, b = [], line.encode("utf-8")
    while len(b) > 75:
        cut = 75
        while (b[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(b[:cut].decode("utf-8"))
        b = b" " + b[cut:]
    out.append(b.decode("utf-8"))
    return "\r\n".join(out)


def to_ics(events):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//peps-piscine//FR",
        "CALSCALE:GREGORIAN", "X-WR-CALNAME:PEPS piscine", f"X-WR-TIMEZONE:{TZ}",
    ]
    for e in events:
        pool = e["info"][0] if e["info"] else "Piscine"
        short = "Olympique" if "olympique" in pool.lower() else "Tremplins"
        cfg = " ".join(e["config"])
        if e["kind"] == "longueurs":
            length = next((c for c in e["config"] if re.match(r"^\d+m$", c)), "")
            title = f"🏊 Longueurs {length} {short}".replace("  ", " ")
            if "peu profond" in cfg.lower():
                title += " (peu profond)"
        else:
            title = "🏊 Bain pour tous"
        desc_parts = [" ".join(e["info"]), cfg]
        if e["note"]:
            desc_parts.append("Note: " + " ".join(e["note"]))
        desc_parts.append(URL)
        d = e["day"].strftime("%Y%m%d")
        s = f"{d}T{e['start'][0]:02d}{e['start'][1]:02d}00"
        f = f"{d}T{e['end'][0]:02d}{e['end'][1]:02d}00"
        # 固定的 UID: 以后重新导入时，同一时段不会重复出现
        uid = hashlib.md5(f"{e['kind']}|{s}|{f}|{pool}|{cfg}".encode()).hexdigest()
        out += [
            "BEGIN:VEVENT",
            f"UID:{uid}@peps-piscine",
            f"DTSTAMP:{stamp}",
            f"DTSTART;TZID={TZ}:{s}",
            f"DTEND;TZID={TZ}:{f}",
            fold("SUMMARY:" + esc(title)),
            fold("LOCATION:" + esc(LOCATION)),
            fold("DESCRIPTION:" + esc("\n".join(p for p in desc_parts if p))),
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def main():
    ap = argparse.ArgumentParser(description="PEPS bains libres -> .ics")
    ap.add_argument("--type", choices=["longueurs", "tous", "all"], default="longueurs")
    ap.add_argument("--pool", choices=["olympique", "tremplins", "all"], default="all")
    ap.add_argument("--min-length", type=int, default=0, help="最短泳道长度，比如 25")
    ap.add_argument("--length", type=int, default=0, help="只要某个泳道长度，比如 21")
    ap.add_argument("--shallow", action="store_true", help="只要有浅水区的时段")
    ap.add_argument("--file", help="本地保存的网页文件（可选）")
    ap.add_argument("--out", default=None, help="输出文件名")
    args = ap.parse_args()

    events = parse(get_text(args), date.today())
    if args.type != "all":
        events = [e for e in events if e["kind"] == args.type]
    if args.pool != "all":
        events = [e for e in events if args.pool in " ".join(e["info"]).lower()]
    def length(e):
        m = next((c for c in e["config"] if re.match(r"^\d+m$", c)), "0m")
        return int(m[:-1])
    if args.min_length:
        events = [e for e in events if length(e) >= args.min_length]
    if args.length:
        events = [e for e in events if length(e) == args.length]
    if args.shallow:
        events = [e for e in events if "peu profond" in " ".join(e["config"]).lower()]
    if not events:
        sys.exit("没有符合条件的时段。")

    first, last = events[0]["day"], max(e["day"] for e in events)
    out = args.out or f"peps_piscine_{first:%m%d}-{last:%m%d}.ics"
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(to_ics(events))
    print(f"完成: {len(events)} 个时段 ({first} 至 {last}) -> {out}")


if __name__ == "__main__":
    main()
