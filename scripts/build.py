#!/usr/bin/env python3
"""
Build a fully self-contained static mirror of www.memory.org.ua from the raw
wget mirror, restructured as path/index.html with every Webflow-CDN and
Webflow-jQuery-CDN reference rewritten to local relative paths.
"""
import os, re, shutil, sys, urllib.parse, urllib.request

BASE = os.path.expanduser('~/memory-org-ua')
RAW  = os.path.join(BASE, 'raw')
WWW  = os.path.join(RAW, 'www.memory.org.ua')
SITE = os.path.join(BASE, 'site')
UA   = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120 Safari/537.36')

ASSET_HOSTS = [
    'cdn.prod.website-files.com',
    'uploads-ssl.webflow.com',
    'assets.website-files.com',
    'assets-global.website-files.com',
]
HOST_DIR = {
    'cdn.prod.website-files.com': 'cdn',
    'uploads-ssl.webflow.com': 'uploads',
    'assets.website-files.com': 'assets-wf',
    'assets-global.website-files.com': 'assets-global-wf',
}
HOSTS_RE = '(?:' + '|'.join(h.replace('.', r'\.') for h in ASSET_HOSTS) + ')'
JQUERY_URL   = 'https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js'
JQUERY_LOCAL = os.path.join('assets', 'js', 'jquery-3.5.1.min.js')  # site-relative

log = lambda *a: print(*a, flush=True)

# ---------------------------------------------------------------- page mapping
def discover_pages():
    """Return list of (raw_file, urlpath, out_file, page_dir_abs)."""
    pages = []
    for root, _, files in os.walk(WWW):
        for fn in files:
            raw = os.path.join(root, fn)
            rel = os.path.relpath(raw, WWW)
            if rel == 'index.html':
                urlpath, out = '/', os.path.join(SITE, 'index.html')
            else:
                urlpath = '/' + rel.replace(os.sep, '/')
                out = os.path.join(SITE, rel, 'index.html')
            pages.append((raw, urlpath, out, os.path.dirname(out)))
    return pages

def asset_local_abs(host, decoded_path):
    return os.path.join(SITE, 'assets', HOST_DIR.get(host, host), decoded_path.lstrip('/'))

def rel_from(page_dir_abs, target_abs, urlencode=True):
    r = os.path.relpath(target_abs, page_dir_abs)
    return urllib.parse.quote(r) if urlencode else r

# ---------------------------------------------------------------- downloads
def download(url, dest_abs):
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(dest_abs, 'wb') as f:
        f.write(data)
    return len(data)

def collect_asset_urls(text, css=False):
    urls = set()
    if css:
        for m in re.finditer(r'url\(((?:[^()\\]|\\.)*)\)', text):
            inner = m.group(1).strip().strip('"\'')
            if inner.startswith('data:'):
                continue
            inner = inner.replace('\\(', '(').replace('\\)', ')').replace('\\ ', ' ')
            if re.match(r'https?://' + HOSTS_RE, inner):
                urls.add(inner)
    else:
        for m in re.finditer(r'https?://' + HOSTS_RE + r'/[^"\'\s,]*', text):
            urls.add(m.group(0))
    return urls

# ---------------------------------------------------------------- rewriters
def rewrite_html(text, page_dir_abs, pageset):
    # 0) drop preconnect/dns-prefetch resource hints to bare Webflow hosts
    text = re.sub(r'<link\b[^>]*href="https?://' + HOSTS_RE + r'"[^>]*>', '', text)

    # 1) asset URLs (absolute cdn) -> relative local
    def asset_sub(m):
        url = m.group(0)
        p = urllib.parse.urlparse(url)
        decoded = urllib.parse.unquote(p.path)
        return rel_from(page_dir_abs, asset_local_abs(p.netloc, decoded))
    text = re.sub(r'https?://' + HOSTS_RE + r'/[^"\'\s,]*', asset_sub, text)

    # 2) jQuery cloudfront -> local  (+ strip integrity/crossorigin on that tag)
    jq_rel = rel_from(page_dir_abs, os.path.join(SITE, JQUERY_LOCAL))
    def jq_script_sub(m):
        tag = m.group(0)
        tag = re.sub(r'https?://d3e54v103j8qbb\.cloudfront\.net/js/jquery[^"\']*', jq_rel, tag)
        tag = re.sub(r'\s+integrity="[^"]*"', '', tag)
        tag = re.sub(r'\s+crossorigin="[^"]*"', '', tag)
        return tag
    text = re.sub(r'<script[^>]*d3e54v103j8qbb\.cloudfront\.net[^>]*>', jq_script_sub, text)

    # 3) internal root-relative links -> relative dir links
    def link_sub(m):
        q, path = m.group('q'), m.group('path')
        key = path.split('#')[0].split('?')[0].rstrip('/')
        frag = path[len(path.split('#')[0].split('?')[0]):]  # preserve #.. or ?..
        norm = key if key else '/'
        if norm not in pageset:
            return m.group(0)
        target_dir = SITE if norm == '/' else os.path.join(SITE, norm.strip('/'))
        r = rel_from(page_dir_abs, target_dir, urlencode=False)
        link = ('./' if r == '.' else r.rstrip('/') + '/')
        return f'{q}{link}{frag}{q}'
    text = re.sub(r'(?P<q>["\'])(?P<path>/(?!/)[^"\']*)(?P=q)', link_sub, text)

    return text

def rewrite_css(text, css_dir_abs):
    def sub(m):
        raw_inner = m.group(1).strip()
        q = ''
        if raw_inner[:1] in '"\'':
            q = raw_inner[0]; raw_inner = raw_inner.strip('"\'')
        if raw_inner.startswith('data:'):
            return m.group(0)
        clean = raw_inner.replace('\\(', '(').replace('\\)', ')').replace('\\ ', ' ')
        if not re.match(r'https?://' + HOSTS_RE, clean):
            return m.group(0)
        p = urllib.parse.urlparse(clean)
        decoded = urllib.parse.unquote(p.path)
        rel = rel_from(css_dir_abs, asset_local_abs(p.netloc, decoded))
        return f'url({q}{rel}{q})'
    return re.sub(r'url\(((?:[^()\\]|\\.)*)\)', sub, text)

def neutralize_js(text):
    # Remove Webflow badge/editor external calls (kill webflow-infra domain refs)
    text = text.replace('https://editor-api.webflow.com', 'about:blank')
    text = text.replace('https://webflow.com/site/third-party-cookie-check.html', 'about:blank')
    text = text.replace('https://webflow.com?utm_campaign=brandjs', '#')
    text = text.replace('https://webflow.com', '#')
    # Webflow "Made in Webflow" badge SVGs served from Webflow's CloudFront
    text = text.replace('https://d3e54v103j8qbb.cloudfront.net', 'about:blank')
    return text

# ---------------------------------------------------------------- main
def main():
    # Remove only generated content; preserve repo meta, docs, scripts, git history.
    PRESERVE = {'.git', '.gitignore', '.nojekyll', 'docs', 'scripts', 'README.md', 'static'}
    os.makedirs(SITE, exist_ok=True)
    for entry in os.listdir(SITE):
        if entry in PRESERVE:
            continue
        p = os.path.join(SITE, entry)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    # copy all asset host trees
    copied = 0
    for host in ASSET_HOSTS:
        src = os.path.join(RAW, host)
        if os.path.isdir(src):
            dst = os.path.join(SITE, 'assets', HOST_DIR.get(host, host))
            shutil.copytree(src, dst)
            copied += sum(len(f) for _, _, f in os.walk(dst))
    log(f'Copied {copied} asset files into site/assets/')

    pages = discover_pages()
    pageset = set(u.rstrip('/') or '/' for _, u, _, _ in pages)
    log(f'Discovered {len(pages)} HTML pages')

    # --- completeness pass: download any referenced-but-missing asset ---
    needed = set()
    for raw, *_ in pages:
        needed |= collect_asset_urls(open(raw, encoding='utf-8', errors='replace').read())
    for root, _, files in os.walk(os.path.join(SITE, 'assets')):
        for fn in files:
            if fn.endswith('.css'):
                needed |= collect_asset_urls(open(os.path.join(root, fn),
                                             encoding='utf-8', errors='replace').read(), css=True)
    dl = 0
    for url in sorted(needed):
        p = urllib.parse.urlparse(url)
        dest = asset_local_abs(p.netloc, urllib.parse.unquote(p.path))
        if not os.path.exists(dest):
            try:
                n = download(url, dest); dl += 1
                log(f'  downloaded missing asset ({n}B): {os.path.basename(dest)}')
            except Exception as e:
                log(f'  !! FAILED to download {url}: {e}')
    log(f'Downloaded {dl} missing assets')

    # --- jQuery ---
    try:
        n = download(JQUERY_URL, os.path.join(SITE, JQUERY_LOCAL))
        log(f'Localized jQuery ({n}B) -> {JQUERY_LOCAL}')
    except Exception as e:
        log(f'!! jQuery download failed: {e}')

    # --- rewrite + neutralize CSS/JS in site/assets ---
    for root, _, files in os.walk(os.path.join(SITE, 'assets')):
        for fn in files:
            fp = os.path.join(root, fn)
            if fn.endswith('.css'):
                t = open(fp, encoding='utf-8', errors='replace').read()
                open(fp, 'w', encoding='utf-8').write(rewrite_css(t, root))
            elif fn.endswith('.js'):
                t = open(fp, encoding='utf-8', errors='replace').read()
                open(fp, 'w', encoding='utf-8').write(neutralize_js(t))

    # --- write pages ---
    for raw, urlpath, out, page_dir in pages:
        t = open(raw, encoding='utf-8', errors='replace').read()
        t = rewrite_html(t, page_dir, pageset)
        os.makedirs(page_dir, exist_ok=True)
        open(out, 'w', encoding='utf-8').write(t)
    log(f'Wrote {len(pages)} pages into site/')
    log('DONE')

if __name__ == '__main__':
    main()
