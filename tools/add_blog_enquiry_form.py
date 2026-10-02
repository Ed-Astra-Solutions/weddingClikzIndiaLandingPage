"""
Adds the post-footer enquiry form to every blog article.

Readers reaching the end of a post can enquire there instead of navigating to
the homepage contact section. Styling lives in blog/post.css and the submit
logic in blog/contact-form.js, so each page only gains markup plus two tags.

Idempotent: a post that already has the form is skipped.

Run: python3 add_blog_enquiry_form.py [--dry]
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DRY = '--dry' in sys.argv
KEY = '6LevLlIsAAAAACA4B0mAG0wvTCNnubTNA-OgUgai'

FORM = """
<section class="post-enquiry" id="enquire" aria-label="Enquire about your shoot">
  <div class="pe-inner">
    <span class="pe-eyebrow">Talk to us</span>
    <h2>Tell Us About Your <em>Shoot</em></h2>
    <p class="pe-sub">Send your date and what you have in mind. We reply within 24 hours
       with availability and an itemised quote &mdash; no call required first.</p>
    <form id="postEnquiryForm" novalidate>
      <div class="pe-grid">
        <div class="pe-field">
          <label for="pe-name">Name <span>*</span></label>
          <input id="pe-name" type="text" name="name" required placeholder="Your full name">
        </div>
        <div class="pe-field">
          <label for="pe-phone">Phone <span>*</span></label>
          <input id="pe-phone" type="tel" name="phone" required placeholder="+91 98765 43210">
        </div>
        <div class="pe-field">
          <label for="pe-email">Email <span>*</span></label>
          <input id="pe-email" type="email" name="email" required placeholder="your@email.com">
        </div>
        <div class="pe-field">
          <label for="pe-date">Shoot or wedding date</label>
          <input id="pe-date" type="date" name="date">
        </div>
        <div class="pe-field pe-full">
          <label for="pe-location">Location or venue</label>
          <input id="pe-location" type="text" name="location" placeholder="City, venue or the area you have in mind">
        </div>
        <div class="pe-field pe-full">
          <label for="pe-message">Anything else</label>
          <textarea id="pe-message" name="message" placeholder="Events, guest count, the kind of pictures you like&hellip;"></textarea>
        </div>
        <p class="pe-msg" role="status" aria-live="polite"></p>
        <div class="pe-actions">
          <span class="pe-note">Or WhatsApp <a href="https://wa.me/919740222927" style="color:inherit;">+91 97402 22927</a></span>
          <button type="submit" class="pe-submit">Send Enquiry</button>
        </div>
      </div>
    </form>
  </div>
</section>
"""

SCRIPTS = ('<script src="https://www.google.com/recaptcha/api.js?render=%s" defer></script>\n'
           '<script src="/blog/contact-form.js" defer></script>\n') % KEY

posts = sorted(glob.glob(os.path.join(ROOT, 'blog', '*.html')))
added = skipped = failed = 0
for path in posts:
    s = open(path, encoding='utf-8').read()
    if 'postEnquiryForm' in s:
        skipped += 1
        continue
    # Place the form immediately before the site footer.
    # Two footer variants exist across the archive.
    m = re.search(r'<footer class="(?:site-footer|post-footer)">', s)
    if not m:
        print('  no footer, skipped:', os.path.basename(path)); failed += 1; continue
    s = s[:m.start()] + FORM + '\n' + s[m.start():]
    # Scripts just before </body>
    b = s.rfind('</body>')
    s = s[:b] + SCRIPTS + s[b:]
    if not DRY:
        open(path, 'w', encoding='utf-8').write(s)
    added += 1

print(f"{'DRY: ' if DRY else ''}{added} posts got the form | {skipped} already had it | {failed} failed")
