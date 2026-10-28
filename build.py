"""Generate every page of the Knowledge Club 3D site into site/.

All pages share css/site.css, js/scene.js (Three.js world) and js/site.js (UI).
Run: python3 build.py
"""
import html
import json
import pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "site"
DATA = ROOT / "data"
E = html.escape

SITE = "https://knowledgeclub.com"
BROCHURE = f"{SITE}/wp-content/uploads/Knowledge-Club-2026-2027-General-Brochure-1.pdf"
MAILCHIMP = "https://vigorenterprise.us4.list-manage.com/subscribe/post?u=23bc4b5f25b39de14d1df31e9&id=23d6e75483"
HONEYPOT = "b_23bc4b5f25b39de14d1df31e9_23d6e75483"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About Us"),
    ("speakers.html", "Speakers"),
    ("events.html", "Events"),
    ("highlights.html", "Highlights"),
    ("contact.html", "Contact"),
]
SOCIALS = [
    ("https://x.com/GasEvents", "Twitter"),
    ("https://www.facebook.com/ALGASEVENTS", "Facebook"),
    ("https://www.instagram.com/gasevents/", "Instagram"),
    ("https://www.youtube.com/@Gasevents", "YouTube"),
    ("https://www.linkedin.com/company/gasevents/", "LinkedIn"),
]
STATS = [(170, "+", "Speakers"), (72, "+", "Participating organisations"), (12, "K+", "Upskilled participants"), (91, "+", "Events")]
WHY = [
    ("Certificate-of-Attendance.png", "Certificate of Attendance"),
    ("Increase-your-network.png", "Increase your network"),
    ("Be-Engaged.png", "Be Engaged"),
    ("Explore-More.png", "Explore More"),
    ("Meet-the-Expert.png", "Meet the Expert"),
    ("KC-Community.png", "KC Community"),
]
ATTENDEE_BENEFITS = [
    "Insights from industry pioneers",
    "New strategies and a broader knowledge base",
    "Networking with like-minded professionals",
    "Staying ahead of industry trends",
    "Keynotes that inspire action",
    "Hands-on workshops and training",
    "Personal and professional growth",
    "Access to exclusive resources",
]
SPONSOR_BENEFITS = [
    "Brand visibility with an influential audience",
    "Direct reach to executives and industry leaders",
    "Networking with decision makers",
    "Association with excellence and growth",
    "Media exposure through partnerships and coverage",
    "Custom brand activations",
    "Measurable return through data and analytics",
]
CATEGORIES = [("all", "All"), ("conferences", "Conferences"), ("corporate-olympics", "Corporate Olympics"), ("seminars", "Seminars"), ("workshops", "Workshops")]
CAT_LABEL = {"seminars": "Seminar", "workshops": "Workshop", "conferences": "Conference", "corporate-olympics": "Corporate Olympics"}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

SPEAKERS = {
    "antonio-rodriguez": dict(
        name="Antonio Nieto-Rodriguez", photo="03-ANTONIO-RODRIGUEZ.webp", event="powered-by-projects",
        intro="A leading authority on project management, strategy execution and organisational transformation.",
        points=[
            "Called “the father of modern project management” by Harvard Business Review; twice ranked on Thinkers50",
            "Author of Powered by Projects and The HBR Project Management Handbook",
            "Founder and CEO of Projects & Co; former Chairman of the Project Management Institute",
            "600+ keynotes delivered and 10,000+ leaders trained worldwide",
        ]),
    "chris-nel": dict(
        name="Chris Nel", photo="02-CHRIS-NEL.webp", event="adaptive-leadership",
        intro="An internationally recognised expert on Adaptive Leadership and co-founder of Quest Leadership.",
        points=[
            "One of four Europe-based Master Facilitators of The Leadership Challenge®",
            "Former British Army officer and senior executive in two FTSE 100 companies",
            "Has worked with Rolls-Royce, Hitachi, Lufthansa, Virgin Money and the UK Ministry of Defence",
            "Helps organisations build adaptive capability through change and transformation",
        ]),
    "alexander-bell": dict(
        name="Alexander Bell", photo="Alexander-Bell.webp", event="leading-with-attention-intelligence",
        intro="A global keynote speaker on technology, productivity and human connection.",
        points=[
            "Creator of the Attention Intelligence® and Tech Rules® frameworks",
            "Serial entrepreneur: built his first company into a PLC by his twenties",
            "Partnered with Google to bring Street View indoors",
            "Led VR studio Reality Media Group, working with clients such as Warner Bros.",
        ]),
    "warren-cass": dict(
        name="Warren Cass", photo="Warren-Cass.webp", event="building-high-performing-teams",
        intro="A leadership and influence expert with more than 30 years of business experience.",
        points=[
            "Best-selling author of Influence and the upcoming Deep Influence",
            "Co-founder of Hivemind Group, delivering leadership programmes worldwide",
            "Entrepreneur who founded, scaled and exited multiple businesses",
            "Advises organisations across Europe, the Middle East, Asia and Africa",
        ]),
    "hec": dict(
        name="Happiness Effect Conference", photo="HEC.webp", event="hec",
        intro="The 8th edition of HEC brings keynote speakers, authors, executives and HR leaders together around workplace wellbeing.",
        points=[
            "Wellbeing as a strategic driver of performance and retention",
            "Case studies, panels and keynotes from international experts",
            "Practical strategies for culture, engagement and employee experience",
            "Networking with senior executives and HR leaders",
        ]),
    "shakil-butt": dict(
        name="Shakil Butt", photo="06-SHAKIL-BUTT.webp", event="leading-with-impact",
        intro="An award-winning leadership and organisational development expert with 30+ years in HR and leadership.",
        points=[
            "Chartered Fellow of the CIPD and Fellow of the ACCA",
            "Former HR Director of a global humanitarian organisation active in 40+ countries",
            "Named one of the UK’s Most Influential HR Thinkers five times by HR Magazine",
            "Clients include the Government of Oman, Zain, Warba Bank and UK government departments",
        ]),
    "corporate-olympics": dict(
        name="Corporate Olympics™", photo="CO-1.webp", event="corporate-olympics",
        intro="The 5th edition of a team-building day that mixes physical challenges with business simulation games.",
        points=[
            "Leadership and strategic decision-making under pressure",
            "Communication and problem-solving in teams",
            "Trust, collaboration and healthy competition",
            "Engagement that carries back into the workplace",
        ]),
    "deborah-henley": dict(
        name="Deborah Henley", photo="08-DEBORAH-HENLEY.webp", event="the-human-advantage",
        intro="An executive coach and award-winning speaker on leadership communication and emotional intelligence.",
        points=[
            "Creator of the REAL Leadership Framework for leading in an AI-driven world",
            "Author of Your Leadership Story, a Business Book Awards finalist",
            "Trusted by Microsoft, Accenture, Cisco, Goldman Sachs and the UK MOD",
            "Blends psychology, neuroscience and storytelling",
        ]),
    "alastair-greener": dict(
        name="Alastair Greener", photo="09-ALASTAIR-GREENER-1.webp", event="the-communicating-leader",
        intro="An award-winning communication expert, author and former TV presenter with 30+ years of experience.",
        points=[
            "President (2025–2026) and Fellow of the Professional Speaking Association UK & Ireland",
            "Author of Generationally Speaking, shortlisted for the 2026 Business Book Awards",
            "Specialist in leadership communication and multigenerational teams",
            "Podcast host and media skills consultant",
        ]),
    "sanita-pukite": dict(
        name="Sanita Pukite", photo="10-SANITA-PUKITE.webp", event="the-capacity-edge",
        intro="An executive coach and leadership development expert focused on performance and resilience.",
        points=[
            "Creator of The Capacity Edge® framework",
            "INSEAD faculty member and former leader of its Women in Business Club",
            "Former Johnson & Johnson EMEA senior leader",
            "Author of the forthcoming book The Capacity Edge",
        ]),
}

EVENTS = [
    dict(slug="powered-by-projects", title="Powered By Projects", cat="seminars", start="2026-09-08", end="2026-09-08", time=("09:00", "16:00"),
         speaker="antonio-rodriguez", img="03-ANTONIO-RODRIGUEZ-POWERED-BY-PROJECTS-750x465.webp", eid=None,
         summary=["Strategy, innovation and transformation are now delivered through projects, yet many initiatives miss their goals because of weak prioritisation, sponsorship and execution.",
                  "In this interactive seminar Antonio Nieto-Rodriguez shares executive frameworks for choosing the right projects and turning strategy into results."],
         outcomes=["The principles of the Project Economy", "Closing the gap between strategy and execution", "Prioritising the initiatives with the most value",
                   "Stronger executive sponsorship", "Frameworks that speed up delivery", "Building an agile, project-driven organisation"]),
    dict(slug="adaptive-leadership", title="Adaptive Leadership", cat="workshops", start="2026-09-29", end="2026-09-30", time=("09:00", "15:00"),
         speaker="chris-nel", img="02-CHRIS-NEL-ADAPTIVE-LEADERSHIP-750x465.webp",
         summary=["Leadership used to rest on expertise and predictability. Today the edge comes from adapting, learning and responding to constant change.",
                  "This two-day workshop introduces the Adaptive Capability Framework with practical tools, group exercises and reflection for leading through uncertainty."],
         outcomes=["Why disruption demands a different leadership approach", "The core capabilities for adapting with confidence", "Applying the Adaptive Capability Framework to real challenges",
                   "Spotting the opportunities and risks change creates", "A personal action plan for team and organisational adaptability"]),
    dict(slug="leading-with-attention-intelligence", title="Leading with Attention Intelligence", cat="seminars", start="2026-10-20", end="2026-10-20", time=("09:00", "16:00"),
         speaker="alexander-bell", img="9-Alexander-Bell.webp",
         summary=["Constant notifications and digital noise make it hard to focus on what matters, at work and at home.",
                  "Alexander Bell shows leaders and teams how to build Attention Intelligence®: staying focused, intentional and resilient in a connected world."],
         outcomes=["The 7 rules behind our tech habits", "The science linking attention, leadership and productivity", "Practical strategies for digital focus",
                   "Running a personal Attention Audit™", "Tech tips and a tool to multiply productivity"]),
    dict(slug="building-high-performing-teams", title="Building High-performing Teams", cat="workshops", start="2026-11-10", end="2026-11-11", time=("09:00", "15:00"),
         speaker="warren-cass", img="04-WARREN-CASS-BUILDING-HIGH-PERFORMING-TEAMS-750x465.webp",
         summary=["Exceptional teams grow from strong leadership, trust and a shared purpose.",
                  "In this practical workshop Warren Cass gives leaders frameworks and exercises to build motivated, resilient, high-performing teams."],
         outcomes=["What drives motivation and team performance", "Leadership and communication that build trust", "Identifying individual and team motivators",
                   "Handling conflict while keeping accountability", "A culture of ownership and improvement", "Aligning team goals with the organisation"]),
    dict(slug="hec", title="Happiness Effect Conference", cat="conferences", start="2026-11-25", end="2026-11-25", time=("09:00", "15:00"),
         speaker="hec", img="event-05-750x465.webp",
         summary=["HEC returns for its 8th edition, bringing international speakers, authors, executives and HR leaders together around one question: how do people, purpose and performance thrive together?",
                  "Keynotes, case studies and panels give participants proven strategies for healthier cultures, stronger leadership and higher engagement."],
         outcomes=["Learn from renowned speakers and workplace experts", "Build a culture of wellbeing and high performance", "Lead with trust, resilience and purpose",
                   "Improve employee experience and retention", "Connect with executives shaping the future of work"]),
    dict(slug="leading-with-impact", title="Leading With Impact", cat="workshops", start="2026-12-15", end="2026-12-16", time=("09:00", "15:00"),
         speaker="shakil-butt", img="06-SHAKIL-BUTT-LEADING-WITH-IMPACT-750x465.webp",
         summary=["Great leadership goes beyond technical skill: it means inspiring people, making sound decisions, managing change and delivering results.",
                  "This interactive workshop gives leaders practical frameworks for self-awareness, decisions, conflict, projects and lasting change."],
         outcomes=["Greater leadership effectiveness and self-awareness", "Approaches that engage and inspire teams", "Managing stress and resolving conflict",
                   "Better decisions on complex problems", "Projects that deliver strategic value", "Leading high-performing teams through change"]),
    dict(slug="corporate-olympics", title="Corporate Olympics", cat="corporate-olympics", start="2027-01-26", end="2027-01-26", time=("09:00", "16:00"),
         speaker="corporate-olympics", img="Corporate_Olympics_Binnakle_1471x913-750x465.webp",
         summary=["The Corporate Olympics™ returns for its 5th edition: a team-building day combining physical challenges with immersive business simulations.",
                  "Teams compete through realistic scenarios that test strategy, communication, leadership and collaboration under pressure."],
         outcomes=["Leadership and strategic decision-making", "Communication and problem-solving", "Teamwork, collaboration and trust",
                   "Resilience and a healthy competitive mindset", "Engagement and shared celebration"]),
    dict(slug="the-human-advantage", title="The Human Advantage", cat="seminars", start="2027-04-06", end="2027-04-06", time=("09:00", "15:00"),
         speaker="deborah-henley", img="08-DEBORAH-HENLEY-THE-HUMAN-ADVANTAGE-750x465.webp",
         summary=["AI is changing how we work, but it cannot replace what makes leaders exceptional: confidence, purposeful communication and real relationships.",
                  "Deborah Henley combines behavioural insight and practical technique to strengthen the human side of leadership."],
         outcomes=["Leading with confidence and authenticity", "Communicating with clarity that drives action", "Building trust and stronger relationships",
                   "Influence without relying on authority", "Resilience and decisions under pressure", "A culture where people do their best work"]),
    dict(slug="the-communicating-leader", title="The Communicating Leader", cat="workshops", start="2027-04-27", end="2027-04-28", time=("09:00", "15:00"),
         speaker="alastair-greener", img="09-ALASTAIR-GREENER-THE-COMMUNICATING-LEADER-750x465.webp",
         summary=["Leaders are defined by how they communicate, from meetings and presentations to difficult conversations and multigenerational teams.",
                  "This workshop builds confidence, executive presence and impact, and shows how to adapt a message to any audience."],
         outcomes=["Confidence and clarity", "Impactful presentations", "Executive presence and influence",
                   "Handling difficult conversations", "Communicating across generations", "Stronger collaboration and engagement"]),
    dict(slug="the-capacity-edge", title="The Capacity Edge", cat="seminars", start="2027-05-11", end="2027-05-11", time=("09:00", "15:00"),
         speaker="sanita-pukite", img="10-SANITA-PUKITE-THE-CAPACITY-EDGE-750x465.webp",
         summary=["Leadership is tested in moments of uncertainty and sustained pressure, when staying clear and steady is hardest.",
                  "Sanita Pukite introduces The Capacity Edge®, a framework for expanding a leader’s capacity to handle pressure and lead with confidence."],
         outcomes=["Leadership capability versus leadership capacity", "The hidden factors that erode effectiveness under pressure", "Resilience, decisions and presence in uncertainty",
                   "Strategies to expand personal capacity", "An action plan for leading teams with clarity and purpose"]),
]

POSTS = [
    dict(slug="are-hr-project-teams-dead", title="Are HR project teams dead?", author="Perry Timms", date="2020-08-11", img="Are-HR-project-teams-dead.jpg",
         summary="Perry Timms argues that HR must work in a far more agile way to deliver on the modern working proposition, and looks at how often “agile” is misunderstood outside software."),
    dict(slug="6-fundamental-reasons-why-companies-need-to-transform", title="6 Fundamental Reasons Why Companies Need to Transform", author="Christian Rangen", date="2020-07-14",
         img="6-Fundamental-Reasons-Why-Companies-Need-to-Transform-1.jpg",
         summary="Christian Rangen sets out six triggers for transformation, from declining profits and industry shifts to fast technology change, and asks whether one reason or several are at play."),
    dict(slug="5-ways-to-sustain-yourself-and-others", title="5 Ways to Sustain Yourself and Others", author="Sally Foley-Lewis", date="2020-07-14",
         img="5-Ways-to-Sustain-Yourself-and-Others-1.jpg",
         summary="Sally Foley-Lewis offers a five-step approach, Link, Lend, Limber, Look and Learn, for supporting yourself and your team through long periods of uncertainty."),
]

OFFICES = [
    dict(name="ALGAS Events — Kuwait", lines=["Floor 13, Al-Gas Tower, Ahmad Al-Jaber St, Sharq, Kuwait City", "P.O. Box 5044, Safat"],
         tel=[("Tel", "+965 6968 8000")], email="info@gasevents.com"),
    dict(name="GCC — Kuwait", lines=["Floor 13, Al-Gas Tower, Ahmad Al-Jaber St, Sharq, Kuwait City", "P.O. Box 5044, Safat"],
         tel=[("Tel", "+965 2246 1445"), ("Fax", "+965 2246 1446"), ("Cell", "+965 5531 8844")], email="info@vigorenterprise.com"),
    dict(name="North Africa — Egypt", lines=["Building 113, Al Hekma St., District 7, Neighborhood 3", "Sheikh Zayed City, Giza"],
         tel=[("Tel / Fax", "+20 2 3851 5243"), ("Cell", "+20 112 751 6502")], email="info@vigorenterprise.com"),
    dict(name="Canada", lines=["2572 Daniel-Johnson Boulevard, 2nd Floor", "Laval, Quebec H7T 2R3"],
         tel=[("Tel", "+1 450 902 2525"), ("Cell", "+1 438 227 8285")], email="info@vigorenterprise.com"),
]
ARCHIVE = [("2013", "https://vigorevents.com/knowledge-club-2013/"), ("2014", "https://vigorevents.com/knowledge-club/"),
           ("2015", "https://vigorevents.com/knowledge-club-2015/"), ("2016", "https://vigorevents.com/knowledge-club-2016/"),
           ("2017", "https://vigorevents.com/knowledge-club-2017/"), ("2018", "http://vigorevents.com/knowledge-club-2018/")]
SEASONS = [("2025–2026", "Highlights-click.png", f"{SITE}/knowledge-club-2025-2026/"),
           ("2024–2025", "2024-2025-click.webp", f"{SITE}/knowledge-club-2024-2025/"),
           ("2023–2024", "2023-2024-1.png", f"{SITE}/knowledge-club-2023-2024/")]
SHOTS = ["348A7478-Large.webp", "257A5999-Large.webp", "DSC00309-Large.webp", "257A5914-Large.webp", "102-Large.webp", "257A4668-Large.webp", "DSC_9605-Large.webp"]

EV = {e["slug"]: e for e in EVENTS}


# ---------------------------------------------------------------- helpers

def ext(url):
    return 'target="_blank" rel="noopener"' if url.startswith("http") else ""


def fmt_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def date_range(e):
    if e["start"] == e["end"]:
        return fmt_date(e["start"])
    a, b = e["start"].split("-"), e["end"].split("-")
    if a[:2] == b[:2]:
        return f"{int(a[2])}–{int(b[2])} {MONTHS[int(a[1]) - 1]} {a[0]}"
    return f"{fmt_date(e['start'])} – {fmt_date(e['end'])}"


def time_12(t):
    h, m = map(int, t.split(":"))
    return f"{(h - 1) % 12 + 1}:{m:02d} {'am' if h < 12 else 'pm'}"


def speaker_name(e):
    return SPEAKERS[e["speaker"]]["name"]


def title_html(text, em=None):
    if em and em in text:
        a, b = text.split(em, 1)
        return f"{E(a)}<em>{E(em)}</em>{E(b)}"
    return E(text)


def section(sid, label, body, cls="stage", stage=True):
    attr = f' data-stage data-label="{E(label)}"' if stage else ""
    return f'<section id="{sid}" class="{cls}"{attr}>{body}</section>'


def eyebrow(text, d=""):
    return f'<p class="eyebrow reveal {d}">{E(text)}</p>'


def event_card(e):
    y, m, d = e["start"].split("-")
    return f"""<a class="ev glass" data-cat="{e['cat']}" data-end="{e['end']}T{e['time'][1]}:00+03:00" href="event-{e['slug']}.html">
      <div class="ph"><img src="assets/{e['img']}" alt="{E(speaker_name(e))}" loading="lazy">
        <span class="cat {e['cat']}">{CAT_LABEL[e['cat']]}</span>
        <time class="date" datetime="{e['start']}"><b>{d}</b><small>{MONTHS[int(m) - 1]} {y[2:]}</small></time></div>
      <div class="body"><h3>{E(e['title'])}</h3><span class="who">{E(speaker_name(e))}</span>
        <div class="meta"><span>Kuwait · {date_range(e)}</span><span class="go">Details →</span></div></div>
    </a>"""


def events_carousel(sid, heading_html, intro_eyebrow, events, filters=False, foot_link=True):
    filt = ""
    if filters:
        filt = '<div class="filters" role="group" aria-label="Filter events by category">' + "".join(
            f'<button aria-pressed="{str(k == "all").lower()}" data-f="{k}">{v}</button>' for k, v in CATEGORIES) + "</div>"
    foot = '<a class="btn sm ghost" href="events.html">Full calendar →</a>' if foot_link else '<a class="btn sm primary" href="join.html">Book your seat →</a>'
    return section(sid, "Events", f"""<div class="sticky">
      <div class="pin-head"><div><p class="eyebrow">{E(intro_eyebrow)}</p><h2>{heading_html}</h2></div>{filt}</div>
      <div class="track-view"><div class="track">{''.join(event_card(e) for e in events)}</div></div>
      <div class="pin-foot"><span data-count-label>{len(events)} events · Kuwait</span><div class="scrub"><i></i></div>{foot}</div>
    </div>""", cls="pinned")


def stats_html():
    return '<div class="stats">' + "".join(
        f'<div class="stat glass reveal d{i + 2}"><b data-count="{n}" data-suffix="{s}">0</b><span>{E(l)}</span></div>'
        for i, (n, s, l) in enumerate(STATS)) + "</div>"


def why_html():
    return '<div class="grid g3">' + "".join(
        f'<div class="why glass reveal d{i % 3 + 1}" data-tilt><img src="assets/{img}" alt=""><h3>{E(t)}</h3></div>'
        for i, (img, t) in enumerate(WHY)) + "</div>"


def benefits_html():
    li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
    return f"""<div class="grid g2" style="margin-top:16px">
      <div class="card glass reveal d2"><h3>Benefits for attendees</h3><ul class="ticks">{li(ATTENDEE_BENEFITS)}</ul></div>
      <div class="card glass reveal d3"><h3>Elevate your brand as a sponsor</h3><ul class="ticks blue">{li(SPONSOR_BENEFITS)}</ul></div>
    </div>"""


def join_cta(sid="book", heading="Book your <em>seat</em>"):
    return section(sid, "Join", f"""<div class="glass pad narrow" style="margin:0 auto">
      <img class="reveal" src="assets/kc-symbol.png" alt="" style="width:72px;height:72px;margin:0 auto 22px">
      {eyebrow("Season 2026–2027", "d1")}
      <h2 class="reveal d2">{heading}</h2>
      <p class="lead reveal d3">Join Kuwait’s leadership development programme as a member or sponsor and learn alongside 12,700+ professionals.</p>
      <div class="cta reveal d4"><a class="btn primary" href="join.html">Become a member →</a>
        <a class="btn blue" href="{BROCHURE}" {ext(BROCHURE)}>Download Brochure</a>
        <a class="btn ghost" href="contact.html">Contact us</a></div>
    </div>""", cls="stage center")


def sub_hero(crumb, title, em, lead, extra=""):
    return section("top", "Top", f"""<div class="wrap"><div class="copy" style="max-width:720px">
      <nav class="crumbs reveal" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{E(crumb)}</span></nav>
      <h1 class="title" data-split>{title_html(title, em)}</h1>
      <p class="lead reveal d3">{lead}</p>{extra}
    </div></div><div class="scroll-hint">Scroll<i></i></div>""", cls="stage hero sub")


def page(filename, title, description, body, current=None, emblem="corner"):
    current_attr = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{href}"{current_attr if href == current else ""}>{label}</a></li>' for href, label in NAV)
    socials = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for u, n in SOCIALS)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta name="theme-color" content="#060818">
<link rel="icon" href="assets/kc-symbol.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@500;700;800&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body data-emblem="{emblem}">
<canvas id="scene" aria-hidden="true"></canvas>
<div class="vignette"></div>
<div class="warp" aria-hidden="true"><img src="assets/kc-symbol.png" alt=""></div>
<div class="bar" id="bar"></div>
<header class="nav" id="nav">
  <a class="brand" href="index.html" aria-label="Knowledge Club home"><img class="sym" src="assets/kc-symbol.png" alt=""><img class="word" src="assets/kc-wordmark.png" alt="Knowledge Club™"></a>
  <ul id="menu">{nav}</ul>
  <div class="nav-right">
    <a class="btn sm ghost" href="{BROCHURE}" target="_blank" rel="noopener">Download Brochure</a>
    <a class="btn sm primary" href="join.html">Join</a>
    <button class="menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false" aria-controls="menu">☰</button>
  </div>
</header>
<div class="rail" id="rail"></div>
<main>
{body}
</main>
<footer>
  <div class="foot">
    <a class="brand" href="index.html"><img class="sym" src="assets/kc-symbol.png" alt="" style="width:30px;height:30px"><img class="word" src="assets/kc-wordmark.png" alt="Knowledge Club™"></a>
    <nav aria-label="Footer">{"".join(f'<a href="{h}">{l}</a>' for h, l in NAV[1:])}<a href="join.html">Become a Member</a></nav>
    <div class="socials">{socials}</div>
  </div>
  <p class="copy-line">© 2026 Knowledge Club™. All rights reserved. Organised by ALGAS Events.</p>
</footer>
<script src="vendor/three.min.js"></script>
<script src="js/scene.js"></script>
<script src="js/site.js"></script>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")
    return filename


# ---------------------------------------------------------------- pages

def home():
    hero = section("top", "Home", f"""<div class="wrap"><div class="copy">
      <img class="wordmark reveal" src="assets/kc-wordmark.png" alt="Knowledge Club™">
      <img class="tagline reveal d1" src="assets/kc-tagline.png" alt="The leadership excellence hub for leaders and executives">
      <div><span class="chip reveal d2"><i></i>Season 2026–2027 now open</span></div>
      <h1 class="title" data-split>Where Leaders Learn <em>Before the World Changes</em></h1>
      <p class="lead reveal d3">Join the 2026–2027 Season of Premier Leadership Community. Ten world-class seminars, workshops and conferences in Kuwait.</p>
      <div class="cta reveal d4"><a class="btn primary" href="join.html">Join the 2026–2027 Season →</a><a class="btn ghost" href="events.html">View events calendar</a></div>
    </div></div><div class="scroll-hint">Scroll<i></i></div>""", cls="stage hero")
    impact = section("impact", "Impact", f"""<div class="wrap">{eyebrow("Since 2013")}
      <h2 class="reveal d1">A community that <em>keeps growing</em></h2>
      <p class="lead reveal d2">The leadership excellence hub for leaders and executives, trusted by Kuwait’s leading organisations.</p>
      {stats_html()}<div class="cta reveal d5"><a class="btn ghost" href="about.html">About the club →</a></div></div>""")
    events = events_carousel("events", "The <em>season</em> ahead", "Events Calendar · 2026–2027", EVENTS, filters=True)
    sp = section("speakers", "Speakers", f"""<div class="sticky">
      <div class="pin-head"><div><p class="eyebrow">Speakers &amp; Experts 2026–2027</p><h2>Learn from the <em>best</em></h2></div></div>
      <div class="track-view"><div class="track">{''.join(speaker_card(k) for k in SPEAKERS)}</div></div>
      <div class="pin-foot"><span>{len(SPEAKERS)} programmes</span><div class="scrub"><i></i></div><a class="btn sm ghost" href="speakers.html">All speakers →</a></div>
    </div>""", cls="pinned")
    why = section("why", "Why join", f"""<div class="wrap">{eyebrow("Why Join")}
      <h2 class="reveal d1">The Knowledge Club 2026–2027. <em>Live the experience.</em></h2>{why_html()}{benefits_html()}</div>""", cls="stage center")
    partners = section("partners", "Partners", f"""<div class="wrap">{eyebrow("Organizers")}
      <h2 class="reveal d1">Featured <em>organizers &amp; partners</em></h2>
      <div class="logo-card reveal d2" data-tilt="4"><img src="assets/sponsors.webp" alt="2026/2027 partners: Gold member NBK; Silver members KNET and Burgan Bank; Official airline Turkish Airlines; Members Al-Tijari and IBK; Media partner Source Media Solutions" loading="lazy"></div>
      <div class="logo-card reveal d3" data-tilt="4"><img src="assets/Knowledge-Club-journey-since-2013-trusted-by.webp" alt="A curated list of Knowledge Club participants over the years" loading="lazy"></div></div>""", cls="stage center")
    blog = section("blog", "Blog", f"""<div class="wrap">{eyebrow("From the Blog")}
      <h2 class="reveal d1">Ideas from our <em>experts</em></h2>
      <div class="grid g3">{''.join(post_card(p, i) for i, p in enumerate(POSTS))}</div></div>""", cls="stage center")
    body = hero + impact + events + sp + why + partners + blog + join_cta("join", "Join as a <em>member</em> or <em>sponsor</em>")
    return page("index.html", "Knowledge Club™ | Leadership Development Events 2026–2027",
                "Kuwait’s leadership development programme. 10 world-class seminars, workshops and conferences. Season 2026–2027 now open.",
                body, "index.html", emblem="hero")


def speaker_card(key):
    s = SPEAKERS[key]
    e = EV[s["event"]]
    return f"""<a class="sp glass" href="speakers.html#{key}">
      <div class="portrait"><img src="assets/speakers/{s['photo']}" alt="{E(s['name'])}" loading="lazy"></div>
      <div class="body"><h3>{E(s['name'])}</h3><p class="role">{E(e['title'])} · {fmt_date(e['start'])}</p><p>{E(s['intro'])}</p></div></a>"""


def post_card(p, i):
    return f"""<a class="post glass reveal d{i + 1}" data-tilt href="blog-{p['slug']}.html">
      <div class="ph"><img src="assets/{p['img']}" alt="" loading="lazy"></div>
      <div class="body"><time datetime="{p['date']}">{fmt_date(p['date'])}</time><h3>{E(p['title'])}</h3><span class="by">Article by {E(p['author'])}</span><span class="more">Read →</span></div></a>"""


def about():
    pillars = [
        ("The path to professional excellence", "Since 2013 the club has been the meeting point for Kuwait’s most committed leaders: 12 seasons, 160+ international speakers and one belief, that investing in people is the highest-return decision an organisation can make."),
        ("Access to elite speakers and trainers", "Members learn directly from leading speakers, authors, experts and trainers, with knowledge and skills that carry straight into personal and professional life."),
        ("Position your company for success", "Aligning your brand with the Knowledge Club™ places you alongside the best in business, with recognition, business development and networking inside and outside your organisation."),
    ]
    p = "".join(f'<div class="card glass reveal d{i + 1}" data-tilt><p class="num">0{i + 1}</p><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(pillars))
    algas = ["Training and development", "Entertainment", "Media production", "Creative services", "Sports and eSports", "Talent management"]
    archive = "".join(f'<a class="season glass reveal d{i % 3 + 1}" href="{u}" target="_blank" rel="noopener"><b>{y}</b><span>Season archive</span><span class="go">Open →</span></a>' for i, (y, u) in enumerate(ARCHIVE))
    body = (
        sub_hero("About Us", "12 Seasons of Leadership Excellence", "Leadership Excellence",
                 "The Knowledge Club™ has brought Kuwait’s leaders together with the world’s best speakers since 2013.")
        + section("pillars", "Pillars", f"""<div class="wrap">{eyebrow("About The Knowledge Club™")}<h2 class="reveal d1">Why the club <em>exists</em></h2><div class="grid g3">{p}</div></div>""")
        + section("impact", "Impact", f"""<div class="wrap">{eyebrow("By the numbers")}<h2 class="reveal d1">A decade of <em>impact</em></h2>{stats_html()}</div>""")
        + section("why", "Why join", f"""<div class="wrap">{eyebrow("Why Join")}<h2 class="reveal d1">Live the <em>experience</em></h2>{why_html()}</div>""", cls="stage center")
        + section("algas", "ALGAS", f"""<div class="wrap"><div class="grid g2" style="align-items:center;margin-top:0">
            <div>{eyebrow("Organised by")}<h2 class="reveal d1">ALGAS <em>Events</em></h2>
              <div class="prose reveal d2"><p>A Kuwaiti agency delivering events since 2010, ALGAS Events has worked with influential leaders, speakers, authors and clients across the region.</p>
              <p>Its work is built on creativity, professionalism and transparency, with open collaboration at every stage.</p></div></div>
            <div class="card glass reveal d3" data-tilt><h3>What ALGAS delivers</h3><ul class="ticks">{''.join(f'<li>{x}</li>' for x in algas)}</ul></div>
          </div></div>""")
        + section("archive", "Archive", f"""<div class="wrap">{eyebrow("Past seasons")}<h2 class="reveal d1">Where it <em>started</em></h2>
            <div class="seasons">{archive}</div><div class="cta reveal d4"><a class="btn ghost" href="highlights.html">See all highlights →</a></div></div>""", cls="stage center")
        + join_cta()
    )
    return page("about.html", "About Us | Knowledge Club™", "Since 2013 the Knowledge Club™ has connected Kuwait’s leaders with world-class speakers.", body, "about.html")


def speakers_page():
    profiles = ""
    for i, (key, s) in enumerate(SPEAKERS.items()):
        e = EV[s["event"]]
        profiles += f"""<article id="{key}" class="profile glass pad reveal" data-tilt="3"><div class="speaker-block">
          <div class="portrait"><img src="assets/speakers/{s['photo']}" alt="{E(s['name'])}" loading="lazy"></div>
          <div><span class="cat {e['cat']}">{CAT_LABEL[e['cat']]}</span><h3 style="margin-top:12px">{E(s['name'])}</h3>
            <p class="role">{E(e['title'])} · {date_range(e)}</p>
            <div class="prose"><p>{E(s['intro'])}</p></div><ul class="ticks">{''.join(f'<li>{E(x)}</li>' for x in s['points'])}</ul>
            <div class="cta" style="margin-top:22px"><a class="btn blue sm" href="event-{e['slug']}.html">View event →</a><a class="btn ghost sm" href="join.html">Book a seat</a></div></div>
        </div></article>"""
    carousel = section("lineup", "Line-up", f"""<div class="sticky">
      <div class="pin-head"><div><p class="eyebrow">Speakers &amp; Experts 2026–2027</p><h2>The <em>line-up</em></h2></div></div>
      <div class="track-view"><div class="track">{''.join(speaker_card(k) for k in SPEAKERS)}</div></div>
      <div class="pin-foot"><span>{len(SPEAKERS)} programmes</span><div class="scrub"><i></i></div><a class="btn sm ghost" href="#profiles">Full profiles ↓</a></div>
    </div>""", cls="pinned")
    body = (
        sub_hero("Speakers", "Speakers & Experts of Knowledge Club™ 2026–2027", "2026–2027",
                 "International authors, coaches and thought leaders, each leading one programme of the season.")
        + carousel
        + section("profiles", "Profiles", f'<div class="wrap">{eyebrow("Profiles")}<h2 class="reveal d1">Meet the <em>experts</em></h2><div style="margin-top:36px">{profiles}</div></div>', cls="stage auto")
        + section("numbers", "Impact", f'<div class="wrap">{eyebrow("Knowledge Club™")}<h2 class="reveal d1">Since <em>2013</em></h2>{stats_html()}</div>')
        + join_cta()
    )
    return page("speakers.html", "Speakers | Knowledge Club™", "Speakers and experts of the Knowledge Club™ 2026–2027 season.", body, "speakers.html")


def events_page():
    rows = ""
    for i, e in enumerate(EVENTS):
        rows += f"""<a class="card glass reveal d{i % 3 + 1}" data-tilt href="event-{e['slug']}.html" style="display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:center">
          <time class="date" datetime="{e['start']}"><b>{e['start'][8:]}</b><small>{MONTHS[int(e['start'][5:7]) - 1]} {e['start'][2:4]}</small></time>
          <div><span class="cat {e['cat']}">{CAT_LABEL[e['cat']]}</span><h3 style="margin:8px 0 4px">{E(e['title'])}</h3><p>{E(speaker_name(e))} · {date_range(e)} · {time_12(e['time'][0])}–{time_12(e['time'][1])}</p></div>
          <span class="go" style="color:var(--blue-2)">→</span></a>"""
    body = (
        sub_hero("Events", "Events Calendar 2026–2027", "2026–2027",
                 "Ten seminars, workshops, a conference and the Corporate Olympics™, all in Kuwait.",
                 '<div class="cta reveal d4"><a class="btn primary" href="join.html">Book your seat →</a><a class="btn ghost" href="#list">Jump to list</a></div>')
        + events_carousel("calendar", "Browse by <em>category</em>", "Events Calendar", EVENTS, filters=True, foot_link=False)
        + section("list", "List", f'<div class="wrap">{eyebrow("At a glance")}<h2 class="reveal d1">The full <em>season</em></h2><div class="grid" style="gap:12px">{rows}</div></div>', cls="stage auto")
        + join_cta()
    )
    return page("events.html", "Events Calendar 2026–2027 | Knowledge Club™", "All Knowledge Club™ events for the 2026–2027 season in Kuwait.", body, "events.html")


def event_page(e, idx):
    s = SPEAKERS[e["speaker"]]
    start, end = e["start"].replace("-", ""), e["end"].replace("-", "")
    t0, t1 = e["time"][0].replace(":", "") + "00", e["time"][1].replace(":", "") + "00"
    desc = " ".join(e["summary"])
    gcal = f"https://calendar.google.com/calendar/r/eventedit?text={quote(e['title'])}&dates={start}T{t0}/{end}T{t1}&ctz=Asia/Kuwait&location=Kuwait"
    outlook = f"https://outlook.live.com/calendar/0/deeplink/compose?subject={quote(e['title'])}&startdt={e['start']}T{e['time'][0]}:00&enddt={e['end']}T{e['time'][1]}:00&location=Kuwait"
    ics = E(json.dumps({"uid": e["slug"], "start": f"{start}T{t0}", "end": f"{end}T{t1}", "title": e["title"], "location": "Kuwait", "desc": desc[:200]}))
    related = [x for x in EVENTS if x is not e]
    related = related[idx:] + related[:idx]
    hero = section("top", "Event", f"""<div class="wrap"><div class="event-hero">
      <div>
        <nav class="crumbs reveal" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="events.html">Events</a><span aria-hidden="true">/</span><a href="events.html?category={e['cat']}">{CAT_LABEL[e['cat']]}s</a></nav>
        <h1 class="title" data-split>{E(e['title'])}</h1>
        <p class="lead reveal d2" style="margin-top:14px">with <a href="speakers.html#{e['speaker']}" style="color:#fff;font-weight:600">{E(s['name'])}</a></p>
        <div class="facts">
          <div class="fact glass reveal d2"><span>Date</span><b>{date_range(e)}</b></div>
          <div class="fact glass reveal d3"><span>Time</span><b>{time_12(e['time'][0])} – {time_12(e['time'][1])}</b></div>
          <div class="fact glass reveal d4"><span>Venue</span><b>Kuwait</b></div>
        </div>
        <div class="countdown reveal d4" data-countdown="{e['start']}T{e['time'][0]}:00+03:00" data-end="{e['end']}T{e['time'][1]}:00+03:00">
          <div class="glass"><b>00</b><small>Days</small></div><div class="glass"><b>00</b><small>Hrs</small></div><div class="glass"><b>00</b><small>Min</small></div><div class="glass"><b>00</b><small>Sec</small></div></div>
        <div class="cta reveal d5"><a class="btn primary" data-book href="join.html">Book your seat →</a><a class="btn ghost" href="#about">Programme</a></div>
      </div>
      <div class="poster reveal d2"><img src="assets/{e['img']}" alt="{E(s['name'])}"></div>
    </div></div>""", cls="stage hero sub")
    about_s = section("about", "About", f"""<div class="wrap narrow">{eyebrow(CAT_LABEL[e['cat']] + " · Overview")}
      <h2 class="reveal d1">About the <em>programme</em></h2><div class="prose reveal d2">{''.join(f'<p>{E(x)}</p>' for x in e['summary'])}</div>
      <ol class="stack">{''.join(f'<li class="glass reveal d{min(i + 2, 6)}" data-tilt="6">{E(x)}</li>' for i, x in enumerate(e['outcomes']))}</ol></div>""")
    speaker_s = section("speaker", "Speaker", f"""<div class="wrap"><div class="glass pad speaker-block reveal" data-tilt="3">
      <div class="portrait"><img src="assets/speakers/{s['photo']}" alt="{E(s['name'])}" loading="lazy"></div>
      <div>{eyebrow("Your speaker")}<h2 style="font-size:clamp(30px,4vw,52px)">{E(s['name'])}</h2>
        <div class="prose"><p>{E(s['intro'])}</p></div><ul class="ticks">{''.join(f'<li>{E(x)}</li>' for x in s['points'])}</ul>
        <div class="cta" style="margin-top:22px"><a class="btn ghost sm" href="speakers.html#{e['speaker']}">Full profile →</a></div></div></div></div>""")
    cal = section("calendar", "Save the date", f"""<div class="glass pad narrow" style="margin:0 auto">
      {eyebrow("Save the date")}<h2 class="reveal d1">{date_range(e)}</h2>
      <p class="lead reveal d2">{time_12(e['time'][0])} – {time_12(e['time'][1])} (Kuwait time) · Kuwait</p>
      <div class="cal reveal d3" style="justify-content:center"><a class="btn sm ghost" href="{gcal}" target="_blank" rel="noopener">Google</a>
        <a class="btn sm ghost" href="{outlook}" target="_blank" rel="noopener">Outlook</a>
        <a class="btn sm ghost" data-ics="{ics}" download="{e['slug']}.ics" href="#">Apple / .ics</a></div>
      <div class="cta reveal d4"><a class="btn primary" href="join.html">Book your seat →</a><a class="btn blue" href="{BROCHURE}" target="_blank" rel="noopener">Download Brochure</a></div>
    </div>""", cls="stage center")
    rel = events_carousel("related", "More from the <em>season</em>", "Related events", related[:6])
    body = hero + about_s + speaker_s + cal + rel
    return page(f"event-{e['slug']}.html", f"{e['title']} | Knowledge Club™",
                f"{e['title']} with {s['name']}, {date_range(e)} in Kuwait. {e['summary'][0]}", body, "events.html", emblem="none")


def highlights():
    gallery = json.loads((DATA / "gallery.json").read_text())
    years = {}
    for g in gallery:
        years.setdefault(g["year"], []).append(g)
    timeline = "".join(
        f'<div class="year reveal"><b>{y}</b><div class="gal">' + "".join(
            f'<a class="glass" href="{g["url"]}" target="_blank" rel="noopener"><img src="assets/gallery/{g["file"]}" alt="" loading="lazy">{E(g["title"].lower())}</a>' for g in items)
        + "</div></div>" for y, items in years.items())
    seasons = "".join(
        f'<a class="season glass reveal d{i + 1}" data-tilt href="{u}" target="_blank" rel="noopener"><img src="assets/highlights/{img}" alt="" style="width:100%;border-radius:14px;aspect-ratio:2/1;object-fit:cover;background:#fff"><b>{y}</b><span>Season highlights</span><span class="go">Open gallery →</span></a>'
        for i, (y, img, u) in enumerate(SEASONS))
    shots = "".join(f'<figure class="shot"><img src="assets/highlights/{f}" alt="Knowledge Club event" loading="lazy"></figure>' for f in SHOTS)
    body = (
        sub_hero("Highlights", "More Than a Decade of Changing Minds", "Changing Minds", "Since 2013, and still counting.")
        + section("moments", "Moments", f"""<div class="sticky">
          <div class="pin-head"><div><p class="eyebrow">Moments</p><h2>Inside the <em>room</em></h2></div></div>
          <div class="track-view"><div class="track">{shots}</div></div>
          <div class="pin-foot"><span>{len(SHOTS)} photos</span><div class="scrub"><i></i></div><a class="btn sm ghost" href="#timeline">Galleries ↓</a></div></div>""", cls="pinned")
        + section("seasons", "Seasons", f'<div class="wrap">{eyebrow("Recent seasons")}<h2 class="reveal d1">Season <em>highlights</em></h2><div class="seasons">{seasons}</div></div>', cls="stage center")
        + section("timeline", "Galleries", f'<div class="wrap">{eyebrow("Galleries 2013–2020")}<h2 class="reveal d1">Every <em>edition</em></h2><div class="timeline">{timeline}</div></div>', cls="stage auto")
        + join_cta()
    )
    return page("highlights.html", "Highlights | Knowledge Club™", "Photos and galleries from every Knowledge Club™ season since 2013.", body, "highlights.html")


def contact():
    offices = ""
    for i, o in enumerate(OFFICES):
        tel = "".join(f'<p><span class="k">{k}</span><br><a href="tel:{v.replace(" ", "")}">{v}</a></p>' for k, v in o["tel"])
        offices += f'<div class="office glass reveal d{i + 1}" data-tilt="6"><h3>{E(o["name"])}</h3><p>{"<br>".join(E(x) for x in o["lines"])}</p>{tel}<p><span class="k">Email</span><br><a href="mailto:{o["email"]}">{o["email"]}</a></p></div>'
    body = (
        sub_hero("Contact", "We’re Here. Let’s Talk.", "Let’s Talk.", "Questions about membership, sponsorship or a specific event? Reach the ALGAS Events team.",
                 '<div class="cta reveal d4"><a class="btn primary" href="tel:+96569688000">Call +965 6968 8000</a><a class="btn ghost" href="mailto:info@gasevents.com">info@gasevents.com</a></div>')
        + section("offices", "Offices", f"""<div class="wrap">{eyebrow("Get information")}<h2 class="reveal d1">Our <em>offices</em></h2>
            <div class="grid g4">{offices}</div>
            <div class="map reveal d3"><iframe title="Map: Al-Gas Tower, Sharq, Kuwait City" loading="lazy" src="https://maps.google.com/maps?q=Al-Gas%20Tower%2C%20Ahmad%20Al-Jaber%20St%2C%20Sharq%2C%20Kuwait%20City&t=m&z=16&output=embed&iwloc=near"></iframe></div></div>""")
        + section("message", "Message", f"""<div class="wrap narrow"><div class="glass pad">
            {eyebrow("Have questions?")}<h2 class="reveal d1">Send a <em>message</em></h2>
            <form class="form reveal d2" id="contactForm" data-to="info@gasevents.com">
              <label>Name <i>*</i><input name="name" required autocomplete="name"></label>
              <label>Email <i>*</i><input name="email" type="email" required autocomplete="email"></label>
              <label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
              <label>Subject<input name="subject"></label>
              <label class="full">Message <i>*</i><textarea name="message" required></textarea></label>
              <div class="full"><button class="btn primary" type="submit">Send message →</button><p class="note" id="contactNote" role="status"></p></div>
            </form></div></div>""", cls="stage center")
        + join_cta()
    )
    return page("contact.html", "Contact | Knowledge Club™", "Contact ALGAS Events, organiser of the Knowledge Club™, in Kuwait, Egypt and Canada.", body, "contact.html")


def join():
    countries = json.loads((DATA / "countries.json").read_text())
    opts = "".join(f'<option value="{E(v)}"{" selected" if v == "Kuwait" else ""}>{E(t) or "Select a country"}</option>' for v, t in countries)
    body = (
        sub_hero("Become a Member", "Become a Knowledge Club Member", "Member",
                 "Register your interest for the 2026–2027 season and the team will contact you with membership and sponsorship options.",
                 '<div class="cta reveal d4"><a class="btn primary" href="#register">Register now →</a><a class="btn ghost" href="' + BROCHURE + '" target="_blank" rel="noopener">Download Brochure</a></div>')
        + section("register", "Register", f"""<div class="wrap narrow"><div class="glass pad">
            {eyebrow("Become a member · كن عضواً")}<h2 class="reveal d1">Your <em>details</em></h2>
            <form class="form reveal d2" id="joinForm" action="{MAILCHIMP}" method="post" target="_blank">
              <label class="full">Email Address · البريد الإلكتروني <i>*</i><input type="email" name="EMAIL" required autocomplete="email"></label>
              <label>First Name · الإسم الأول <i>*</i><input name="FNAME" required autocomplete="given-name"></label>
              <label>Last Name · الإسم الأخير <i>*</i><input name="LNAME" required autocomplete="family-name"></label>
              <label>Phone Number · رقم الهاتف <i>*</i><input name="PHONE" type="tel" required autocomplete="tel"></label>
              <label>Company · جهة العمل<input name="COMPANY" autocomplete="organization"></label>
              <label>Job Title · المسمى الوظيفي <i>*</i><input name="JOBTITLE" required autocomplete="organization-title"></label>
              <label>Country · الدولة <i>*</i><select name="COUNTRY" required>{opts}</select></label>
              <div class="hp" aria-hidden="true"><input type="text" name="{HONEYPOT}" tabindex="-1" value=""></div>
              <div class="full"><button class="btn primary" type="submit">Become a member →</button><p class="note" id="joinNote" role="status"></p></div>
            </form></div></div>""", cls="stage center")
        + section("why", "Why join", f'<div class="wrap">{eyebrow("Why Join")}<h2 class="reveal d1">What members <em>get</em></h2>{why_html()}{benefits_html()}</div>', cls="stage center")
        + events_carousel("season", "Your <em>season</em>", "2026–2027 programme", EVENTS)
    )
    return page("join.html", "Become a Member | Knowledge Club™", "Register for the Knowledge Club™ 2026–2027 season.", body, None)


def blog_page(p, idx):
    others = [x for x in POSTS if x is not p]
    body = (
        sub_hero("Blog", p["title"], None, f"Article by {E(p['author'])} · {fmt_date(p['date'])}")
        + section("article", "Article", f"""<div class="wrap"><div class="event-hero">
            <div class="poster reveal"><img src="assets/{p['img']}" alt=""></div>
            <div>{eyebrow("In short")}<div class="prose reveal d1"><p>{E(p['summary'])}</p></div>
              <div class="cta reveal d2"><a class="btn primary" href="{SITE}/{p['slug']}/" target="_blank" rel="noopener">Read the full article →</a></div></div>
          </div></div>""")
        + section("more", "More", f'<div class="wrap">{eyebrow("More from the blog")}<h2 class="reveal d1">Keep <em>reading</em></h2><div class="grid g2">{"".join(post_card(x, i) for i, x in enumerate(others))}</div></div>', cls="stage center")
        + join_cta()
    )
    return page(f"blog-{p['slug']}.html", f"{p['title']} | Knowledge Club™", p["summary"], body, None, emblem="none")


if __name__ == "__main__":
    built = [home(), about(), speakers_page(), events_page(), highlights(), contact(), join()]
    built += [event_page(e, i) for i, e in enumerate(EVENTS)]
    built += [blog_page(p, i) for i, p in enumerate(POSTS)]
    print(f"{len(built)} pages →", OUT)
