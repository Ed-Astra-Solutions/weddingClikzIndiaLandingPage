"""
Wraps bare <table> elements in blog posts with .data-table-wrap.

Without the wrapper a wide table pushes the whole page sideways on phones --
the page body scrolls horizontally, which Google counts against mobile
usability. The wrapper gives the table its own scroll area instead.

Run: python3 wrap_blog_tables.py [--dry]
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DRY = '--dry' in sys.argv

def already_wrapped(s, start):
    return 'data-table-wrap' in s[max(0, start - 220):start] or \
           'table-scroll' in s[max(0, start - 220):start]

total = files = 0
for path in sorted(glob.glob(os.path.join(ROOT, 'blog', '*.html'))):
    s = open(path, encoding='utf-8').read()
    out, cursor, n = [], 0, 0
    for m in re.finditer(r'<table[^>]*>', s):
        if already_wrapped(s, m.start()):
            continue
        close = s.find('</table>', m.end())
        if close == -1:
            continue
        close += len('</table>')
        out.append((m.start(), close))
    # apply back to front so earlier offsets stay valid
    for start, end in reversed(out):
        s = s[:start] + '<div class="data-table-wrap">' + s[start:end] + '</div>' + s[end:]
        n += 1
    if n:
        files += 1; total += n
        if not DRY:
            open(path, 'w', encoding='utf-8').write(s)
print(f"{'DRY: ' if DRY else ''}wrapped {total} tables across {files} posts")
