"""Bundle index.html, assets/ and vendor/three.min.js into one self-contained HTML file."""
import base64
import mimetypes
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "knowledgeclub-3d.html"
mimetypes.add_type("image/webp", ".webp")


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


html = (ROOT / "index.html").read_text(encoding="utf-8")

# three.js from cdnjs keeps the file small enough for in-app viewers
html = html.replace('<script src="vendor/three.min.js"></script>',
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>')

# Logo crops are embedded; photos and partner graphics load from knowledgeclub.com to keep the file small
UPLOADS = "https://knowledgeclub.com/wp-content/uploads/"
REMOTE = {
    "sponsors.webp": "sponsors.png",
    "Knowledge-Club-journey-since-2013-trusted-by.webp": "Knowledge-Club%E2%84%A2-journey-since-2013-trusted-by.webp",
    "Are-HR-project-teams-dead.jpg": "2020/08/Are-HR-project-teams-dead.jpg",
    "6-Fundamental-Reasons-Why-Companies-Need-to-Transform-1.jpg": "2020/07/6-Fundamental-Reasons-Why-Companies-Need-to-Transform-1.jpg",
    "5-Ways-to-Sustain-Yourself-and-Others-1.jpg": "2020/07/5-Ways-to-Sustain-Yourself-and-Others-1.jpg",
}


def asset_url(name):
    if name.startswith("kc-"):
        return data_uri(ROOT / "assets" / name)
    return UPLOADS + REMOTE.get(name, name)


html = re.sub(r'(src|href)="assets/([^"]+)"', lambda m: f'{m.group(1)}="{asset_url(m.group(2))}"', html)

# Event images referenced from JS
html = html.replace("const A = 'assets/';", f"const A = '{UPLOADS}';")

OUT.write_text(html, encoding="utf-8")
print(OUT, f"{OUT.stat().st_size / 1024:.0f} KB")
