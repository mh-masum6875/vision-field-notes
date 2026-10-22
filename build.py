#!/usr/bin/env python3
"""Static site builder. Reads content/ and writes the site to docs/."""
import json, re, shutil, math, html
from pathlib import Path
from datetime import date
import yaml, markdown
from jinja2 import Environment, BaseLoader

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
S = json.loads((ROOT / "site.json").read_text())
AFF = json.loads((ROOT / "affiliates.json").read_text())
BASE = S["base_url"].rstrip("/")
BP = "/" + BASE.split("/", 3)[3] if BASE.count("/") > 2 else ""

def split_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("missing front matter")
    return yaml.safe_load(m.group(1)), m.group(2)

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

posts, slugs = [], set()
for f in sorted((ROOT / "content/posts").glob("*.md")):
    fm, body = split_fm(f.read_text())
    fm["slug"] = f.stem
    fm["body"] = body
    fm["date"] = str(fm["date"])
    posts.append(fm)
    slugs.add(f.stem)
by_slug = {p["slug"]: p for p in posts}

def render_body(p):
    used_aff = [False]
    def aff(m):
        text, key = m.group(1), m.group(2)
        a = AFF.get(key)
        if not a:
            return text
        if a.get("aff_url"):
            used_aff[0] = True
            return f'[{text}]({a["aff_url"]}){{: rel="sponsored nofollow noopener" target="_blank"}}'
        if a.get("url"):
            return f'[{text}]({a["url"]}){{: rel="noopener" target="_blank"}}'
        return text
    body = re.sub(r"\[([^\]]+)\]\(aff:([a-z0-9_]+)\)", aff, p["body"])
    def link(m):
        text, slug = m.group(1), m.group(2)
        if slug not in slugs:
            return text
        return f"[{text}]({BP}/posts/{slug}/)"
    body = re.sub(r"\[([^\]]+)\]\(post:([a-z0-9-]+)\)", link, body)
    md = markdown.Markdown(extensions=["extra", "toc", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}})
    h = md.convert(body)
    return h, md.toc_tokens, used_aff[0]

def words(t): return len(re.findall(r"\w+", re.sub(r"```.*?```", "", t, flags=re.S)))

for p in posts:
    p["html"], p["toc"], p["has_aff"] = render_body(p)
    p["words"] = words(p["body"])
    p["minutes"] = max(1, round(p["words"] / 220))
    p["cat_slug"] = slugify(p["category"])
cats = {}
for p in posts: cats.setdefault(p["category"], []).append(p)
posts.sort(key=lambda p: (p["date"], p["title"]), reverse=True)

pages = {}
for f in (ROOT / "content/pages").glob("*.md"):
    fm, body = split_fm(f.read_text())
    fm["html"] = markdown.markdown(body, extensions=["extra"])
    pages[f.stem] = fm

CSS = """
:root{--bg:#fbfbf9;--fg:#1c1f23;--mut:#5b6470;--line:#e3e4df;--card:#fff;--acc:#0b6b5c;--acc2:#e8f3f0;--code:#f1f2ee}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#101315;--fg:#e6e8e6;--mut:#9aa3aa;--line:#262b2f;--card:#171b1e;--acc:#5fd0b9;--acc2:#16282a;--code:#1b2023}}
:root[data-theme=dark]{--bg:#101315;--fg:#e6e8e6;--mut:#9aa3aa;--line:#262b2f;--card:#171b1e;--acc:#5fd0b9;--acc2:#16282a;--code:#1b2023}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.7 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--acc)}a:hover{text-decoration-thickness:2px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header.site{border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:5}
header.site .wrap{display:flex;align-items:center;gap:20px;min-height:58px;flex-wrap:wrap}
.brand{font-weight:700;font-size:19px;color:var(--fg);text-decoration:none;letter-spacing:-.01em}
.brand span{color:var(--acc)}
nav.main{display:flex;gap:16px;flex:1;flex-wrap:wrap}
nav.main a{color:var(--mut);text-decoration:none;font-size:15px}nav.main a:hover{color:var(--fg)}
.search{position:relative}
.search input{font:inherit;font-size:15px;padding:7px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);width:210px;max-width:100%}
#results{position:absolute;right:0;top:42px;width:min(420px,92vw);background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,.12);display:none;max-height:60vh;overflow:auto}
#results a{display:block;padding:10px 14px;text-decoration:none;color:var(--fg);border-bottom:1px solid var(--line);font-size:15px;line-height:1.4}
#results a small{display:block;color:var(--mut)}#results a:last-child{border:0}#results a:hover{background:var(--acc2)}
.hero{padding:56px 0 30px}.hero h1{font-size:clamp(30px,5vw,46px);line-height:1.12;margin:0 0 14px;letter-spacing:-.025em}
.hero p{font-size:19px;color:var(--mut);max-width:640px;margin:0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0 8px}
.chips a{font-size:14px;padding:6px 13px;border:1px solid var(--line);border-radius:99px;text-decoration:none;color:var(--fg);background:var(--card)}
.chips a:hover{border-color:var(--acc);color:var(--acc)}
h2.sec{font-size:22px;margin:42px 0 16px;letter-spacing:-.01em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 18px 16px;text-decoration:none;color:var(--fg);transition:border-color .15s}
.card:hover{border-color:var(--acc)}
.card .cat{font-size:12.5px;font-weight:600;color:var(--acc);text-transform:uppercase;letter-spacing:.05em}
.card h3{font-size:18px;line-height:1.3;margin:8px 0 8px}
.card p{font-size:15px;color:var(--mut);margin:0 0 10px;line-height:1.55}
.card .meta{font-size:13px;color:var(--mut)}
article{max-width:720px;margin:0 auto;padding:40px 20px 30px}
article h1{font-size:clamp(28px,4.4vw,40px);line-height:1.15;margin:8px 0 14px;letter-spacing:-.025em}
.byline{color:var(--mut);font-size:14.5px;margin-bottom:26px}
.crumb{font-size:14px;color:var(--mut)}.crumb a{color:var(--mut)}
article h2{font-size:25px;margin:2.1em 0 .5em;line-height:1.25;letter-spacing:-.015em}
article h3{font-size:20px;margin:1.7em 0 .4em}
article p,article li{margin:0 0 1em}article ul,article ol{padding-left:1.3em}
article img{max-width:100%}
pre{background:var(--code);border:1px solid var(--line);border-radius:10px;padding:14px 16px;overflow:auto;font-size:14.5px;line-height:1.55}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;background:var(--code);padding:.1em .35em;border-radius:5px}pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;font-size:15.5px;margin:1.2em 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left;vertical-align:top}th{background:var(--acc2)}
blockquote{margin:1.2em 0;padding:.2em 1.1em;border-left:3px solid var(--acc);color:var(--mut)}
.toc{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:12px 18px;margin:0 0 28px;font-size:15px}
.toc b{display:block;margin-bottom:4px}.toc ul{margin:0;padding-left:1.1em}.toc li{margin:2px 0}
.note{background:var(--acc2);border-radius:10px;padding:11px 15px;font-size:14.5px;margin:0 0 26px;color:var(--fg)}
.ad{margin:30px 0;min-height:90px;text-align:center}
.related{max-width:1040px;margin:10px auto 0;padding:0 20px}
footer.site{margin-top:70px;border-top:1px solid var(--line);padding:30px 0 40px;color:var(--mut);font-size:14.5px}
footer.site .wrap{display:flex;flex-wrap:wrap;gap:12px 28px;justify-content:space-between}
footer.site a{color:var(--mut)}
.cookie{position:fixed;left:12px;right:12px;bottom:12px;max-width:560px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;font-size:14px;box-shadow:0 8px 30px rgba(0,0,0,.15);display:none;z-index:9}
.cookie button{font:inherit;font-size:14px;padding:6px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;margin-right:8px}
.cookie button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
.pager{display:flex;gap:10px;flex-wrap:wrap;margin:30px 0}
@media (max-width:600px){body{font-size:16.5px}.search input{width:150px}}
"""

JS_SEARCH = """
(function(){var i=document.getElementById('q'),r=document.getElementById('results'),d=null;
function load(){if(d)return Promise.resolve(d);return fetch(window.BP+'/search.json').then(function(x){return x.json()}).then(function(j){d=j;return j})}
i.addEventListener('focus',load);
i.addEventListener('input',function(){var q=i.value.trim().toLowerCase();if(q.length<2){r.style.display='none';return}
load().then(function(a){var t=q.split(/\\s+/);var m=a.map(function(p){var h=(p.t+' '+p.d+' '+p.g).toLowerCase(),s=0;t.forEach(function(w){if(p.t.toLowerCase().indexOf(w)>-1)s+=3;if(h.indexOf(w)>-1)s+=1;else s-=10});return[s,p]}).filter(function(x){return x[0]>0}).sort(function(a,b){return b[0]-a[0]}).slice(0,8);
r.innerHTML=m.length?m.map(function(x){return'<a href="'+window.BP+'/posts/'+x[1].s+'/">'+x[1].t+'<small>'+x[1].c+'</small></a>'}).join(''):'<a>No matches</a>';r.style.display='block'})});
document.addEventListener('click',function(e){if(!e.target.closest('.search'))r.style.display='none'})})();
"""

JS_CONSENT = """
(function(){var k='vfn-consent',b=document.getElementById('cookie');if(!b)return;var v;try{v=localStorage.getItem(k)}catch(e){}
function load(){var s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+window.ADS;document.head.appendChild(s);
(document.querySelectorAll('.adsbygoogle')||[]).forEach(function(){try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}})}
if(v==='yes'){load()}else if(!v){b.style.display='block'}
b.querySelector('.p').onclick=function(){try{localStorage.setItem(k,'yes')}catch(e){}b.style.display='none';load()};
b.querySelector('.n').onclick=function(){try{localStorage.setItem(k,'no')}catch(e){}b.style.display='none'}})();
"""

LAYOUT = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }}</title>
<meta name="description" content="{{ desc }}">
<link rel="canonical" href="{{ canon }}">
<meta property="og:type" content="{{ 'article' if is_post else 'website' }}">
<meta property="og:title" content="{{ title }}"><meta property="og:description" content="{{ desc }}">
<meta property="og:url" content="{{ canon }}"><meta property="og:site_name" content="{{ s.name }}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{{ s.name }}" href="{{ bp }}/feed.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230b6b5c'/%3E%3Ccircle cx='16' cy='16' r='7' fill='none' stroke='white' stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='2.5' fill='white'/%3E%3C/svg%3E">
{% if s.adsense_publisher_id %}<meta name="google-adsense-account" content="ca-pub-{{ s.adsense_publisher_id }}">{% endif %}
<style>{{ css|safe }}</style>
{% if jsonld %}<script type="application/ld+json">{{ jsonld|safe }}</script>{% endif %}
</head><body>
<header class="site"><div class="wrap">
<a class="brand" href="{{ bp }}/">Vision <span>Field Notes</span></a>
<nav class="main">{% for c in cats %}<a href="{{ bp }}/category/{{ c.slug }}/">{{ c.short }}</a>{% endfor %}<a href="{{ bp }}/about/">About</a></nav>
<div class="search"><input id="q" type="search" placeholder="Search articles" aria-label="Search articles" autocomplete="off"><div id="results"></div></div>
</div></header>
<main>{{ content|safe }}</main>
<footer class="site"><div class="wrap">
<div>© {{ year }} {{ s.author }}. <a href="{{ bp }}/about/">About</a> · <a href="{{ bp }}/contact/">Contact</a> · <a href="{{ bp }}/privacy/">Privacy</a> · <a href="{{ bp }}/disclosure/">Affiliate disclosure</a></div>
<div><a href="{{ s.author_url }}">Portfolio</a> · <a href="{{ s.github }}">GitHub</a> · <a href="{{ bp }}/feed.xml">RSS</a></div>
</div></footer>
{% if s.adsense_client %}<div class="cookie" id="cookie" role="dialog" aria-label="Cookie notice"><p style="margin:0 0 10px">This site uses cookies for advertising. You can accept or decline. <a href="{{ bp }}/privacy/">Privacy policy</a></p><button class="p">Accept</button><button class="n">Decline</button></div>
<script>window.ADS="{{ s.adsense_client }}";{{ js_consent|safe }}</script>{% endif %}
<script>window.BP="{{ bp }}";{{ js_search|safe }}</script>
</body></html>"""

env = Environment(loader=BaseLoader(), autoescape=True)
layout = env.from_string(LAYOUT)

SHORT = {"YOLO and Detection Basics": "YOLO Basics", "Datasets and Training": "Training",
         "Edge Hardware and Deployment": "Edge", "Video Analytics": "Video",
         "Tools and Workflow": "Tools", "Career and Freelancing": "Career"}
catlist = [{"name": c, "slug": slugify(c), "short": SHORT.get(c, c)} for c in
           ["YOLO and Detection Basics", "Datasets and Training", "Edge Hardware and Deployment",
            "Video Analytics", "Tools and Workflow", "Career and Freelancing"] if c in cats]

def page(path, title, desc, content, canon_path, is_post=False, jsonld=None):
    full_title = title if title.startswith(S["name"]) else f"{title} | {S['name']}"
    out = layout.render(s=S, bp=BP, cats=catlist, css=CSS, js_search=JS_SEARCH, js_consent=JS_CONSENT,
                        title=full_title, desc=desc, canon=BASE + canon_path, content=content,
                        is_post=is_post, jsonld=jsonld, year=date.today().year)
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(out)

def card(p):
    return (f'<a class="card" href="{BP}/posts/{p["slug"]}/"><div class="cat">{html.escape(p["category"])}</div>'
            f'<h3>{html.escape(p["title"])}</h3><p>{html.escape(p["description"])}</p>'
            f'<div class="meta">{p["minutes"]} min read</div></a>')

if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()

# home
chips = "".join(f'<a href="{BP}/category/{c["slug"]}/">{html.escape(c["name"])}</a>' for c in catlist)
home = (f'<div class="wrap"><section class="hero"><h1>{html.escape(S["tagline"])}</h1>'
        f'<p>Guides on training detectors, running them on small devices and keeping video analytics reliable. Written by a computer vision engineer, with no hype.</p>'
        f'<div class="chips">{chips}</div></section>')
home += '<h2 class="sec">Latest articles</h2><div class="grid">' + "".join(card(p) for p in posts[:9]) + "</div>"
for c in catlist:
    cp = cats[c["name"]]
    home += f'<h2 class="sec">{html.escape(c["name"])}</h2><div class="grid">' + "".join(card(p) for p in cp[:3]) + "</div>"
    home += f'<p><a href="{BP}/category/{c["slug"]}/">All {len(cp)} articles in {html.escape(c["name"])}</a></p>'
home += "</div>"
page("index.html", S["name"] + ": " + "computer vision and edge AI in practice",
     "Practical guides on YOLO, datasets, edge deployment and video analytics from a computer vision engineer.", home, "/")

# categories
for c in catlist:
    cp = cats[c["name"]]
    body = (f'<div class="wrap"><section class="hero" style="padding-bottom:10px"><h1>{html.escape(c["name"])}</h1>'
            f'<p>{len(cp)} articles</p></section><div class="grid" style="margin-top:20px">' + "".join(card(p) for p in cp) + "</div></div>")
    page(f"category/{c['slug']}/index.html", c["name"], f"Articles about {c['name'].lower()} on {S['name']}.", body, f"/category/{c['slug']}/")

# posts
by_cat_order = {c["name"]: cats[c["name"]] for c in catlist}
for p in posts:
    rel = [q for q in by_cat_order[p["category"]] if q["slug"] != p["slug"]][:3]
    toc = ""
    if len([t for t in p["toc"]]) >= 3:
        items = "".join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a></li>' for t in p["toc"])
        toc = f'<nav class="toc"><b>In this article</b><ul>{items}</ul></nav>'
    note = (f'<div class="note">This article contains affiliate links. If you buy through them I may earn a commission at no extra cost to you. <a href="{BP}/disclosure/">Details</a></div>'
            if p["has_aff"] else "")
    ad = ('<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="%s" data-ad-format="auto" data-full-width-responsive="true"></ins></div>' % S["adsense_client"]) if S["adsense_client"] else ""
    content = (f'<article><div class="crumb"><a href="{BP}/">Home</a> / <a href="{BP}/category/{slugify(p["category"])}/">{html.escape(p["category"])}</a></div>'
               f'<h1>{html.escape(p["title"])}</h1><div class="byline">By {html.escape(S["author"])} · {p["date"]} · {p["minutes"]} min read</div>'
               f'{note}{toc}{p["html"]}{ad}</article>'
               f'<div class="related"><h2 class="sec">More in {html.escape(p["category"])}</h2><div class="grid">{"".join(card(q) for q in rel)}</div></div>')
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p["title"],
                     "description": p["description"], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
                     "author": {"@type": "Person", "name": S["author"], "url": S["author_url"]},
                     "publisher": {"@type": "Organization", "name": S["name"]},
                     "mainEntityOfPage": f'{BASE}/posts/{p["slug"]}/'})
    page(f"posts/{p['slug']}/index.html", p["title"], p["description"], content, f"/posts/{p['slug']}/", True, ld)

# static pages
for k, v in pages.items():
    page(f"{k}/index.html", v["title"], v["description"],
         f'<article><h1>{html.escape(v["title"])}</h1>{v["html"]}</article>', f"/{k}/")
page("404.html", "Page not found", "Page not found.",
     f'<article><h1>Page not found</h1><p>That page does not exist. <a href="{BP}/">Go to the home page</a> or use the search box.</p></article>', "/404.html")

# machine files
urls = ["/"] + [f"/category/{c['slug']}/" for c in catlist] + [f"/posts/{p['slug']}/" for p in posts] + [f"/{k}/" for k in pages]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
(OUT / ".nojekyll").write_text("")
if S["adsense_publisher_id"]:
    (OUT / "ads.txt").write_text(f"google.com, pub-{S['adsense_publisher_id']}, DIRECT, f08c47fec0942fa0\n")
(OUT / "search.json").write_text(json.dumps([{"s": p["slug"], "t": p["title"], "d": p["description"], "c": p["category"], "g": " ".join(map(str, p.get("tags", [])))} for p in posts]))
items = "".join(f'<item><title>{html.escape(p["title"])}</title><link>{BASE}/posts/{p["slug"]}/</link><guid>{BASE}/posts/{p["slug"]}/</guid><pubDate>{date.fromisoformat(p["date"]).strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate><description>{html.escape(p["description"])}</description></item>' for p in posts[:30])
(OUT / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{S["name"]}</title><link>{BASE}/</link><description>{html.escape(S["tagline"])}</description>{items}</channel></rss>')
print(f"built {len(posts)} posts, {len(pages)} pages -> {OUT}")
