#!/usr/bin/env python3
"""
Create a customer proof-approval page.

    python3 scripts/new-proof.py --job 1042 \
        --art ~/Desktop/miller-board.png \
        --customer "Dana Miller" --email dana@example.com \
        --item "Engraved Cutting Board" \
        --detail "Personalization: The Miller Family, Est. 2020" \
        --detail "Size: 12x18  ·  Qty: 1"

Writes proof/<job>-<token>.html and copies the artwork alongside it. Send the
customer the printed URL. Their decision arrives by email via Formspree, and
they get an automatic confirmation copy.

The random token keeps the URL unguessable — the pages are public to anyone
holding the link, so don't use this for artwork that must stay confidential.
"""
import argparse, os, re, secrets, shutil, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "proof")

FORM_ENDPOINT = "https://formspree.io/f/mdaqdpao"   # same inbox as shop orders
SITE = "https://www.ccucustom.com"
PHONE = "(404) 967-8028"
EMAIL = "info@ccucustom.com"

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Proof #{job} · Custom Creations Unlimited</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/styles.css?v=9">
<style>
  body{{background:var(--bg-soft)}}
  .pf{{max-width:56rem;margin:0 auto;padding:2rem var(--gutter) 5rem}}
  .pf-head{{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding:1.4rem 0 1.6rem}}
  .pf-brand{{display:inline-flex;align-items:center;gap:.7rem;font-family:var(--font-display);font-size:1.1rem;font-weight:600}}
  .pf-brand img{{height:34px;width:auto;display:block}}
  .pf-job{{font-size:.85rem;color:var(--text-muted)}}
  .pf-job strong{{color:var(--text)}}
  .pf-card{{background:var(--bg-elevated);border:1px solid var(--line);border-radius:var(--radius);
    box-shadow:var(--shadow-sm);overflow:hidden}}
  .pf-art{{background:#f2efe9;display:grid;place-items:center;padding:1rem}}
  .pf-art img{{max-width:100%;max-height:70vh;display:block;border-radius:calc(var(--radius) - 8px)}}
  .pf-body{{padding:clamp(1.4rem,3vw,2.2rem)}}
  .pf-body h1{{font-size:clamp(1.6rem,1.2rem+1.4vw,2.2rem);margin-bottom:.5rem}}
  .pf-lede{{color:var(--text-muted);margin-bottom:1.6rem}}
  .pf-details{{list-style:none;margin:0 0 1.8rem;padding:1rem 1.2rem;background:var(--bg-soft);
    border:1px solid var(--line);border-radius:calc(var(--radius) - 10px)}}
  .pf-details li{{padding:.3rem 0;font-size:.95rem}}
  .pf-check{{display:grid;gap:.7rem;margin:0 0 1.6rem}}
  .pf-check label{{display:flex;gap:.7rem;align-items:flex-start;cursor:pointer;font-size:.98rem}}
  .pf-check input{{width:22px;height:22px;flex:none;margin-top:1px;accent-color:var(--accent)}}
  .pf-note{{font-size:.86rem;color:var(--text-faint);margin-top:-.6rem;margin-bottom:1.6rem}}
  .pf-actions{{display:flex;gap:.8rem;flex-wrap:wrap}}
  .pf-changes{{display:none;margin-top:1.4rem}}
  .pf-changes.on{{display:block}}
  .pf-foot{{text-align:center;color:var(--text-muted);font-size:.88rem;padding:2rem 0 0}}
  #pfDone{{display:none;text-align:center;padding:clamp(2rem,5vw,3.4rem)}}
  #pfDone.on{{display:block}}
  #pfDone .ic{{width:74px;height:74px;border-radius:50%;background:var(--grad-gold);display:grid;
    place-items:center;margin:0 auto 1.2rem;color:#1a1408}}
  #pfDone .ic svg{{width:36px;height:36px}}
  @media print{{ .pf-check,.pf-actions,.pf-changes{{display:none}} }}
</style></head><body>

<div class="pf">
  <div class="pf-head">
    <span class="pf-brand"><img src="../signage/assets/ccu-mark-dark.png" alt="">Custom Creations Unlimited</span>
    <span class="pf-job">Proof <strong>#{job}</strong> &middot; {date}</span>
  </div>

  <div class="pf-card">
    <div class="pf-art"><img src="art/{artfile}" alt="Design proof for job {job}"></div>
    <div class="pf-body">
      <div id="pfMain">
        <h1>{greeting}please review your proof</h1>
        <p class="pf-lede">Check every detail below. Once you approve, this goes straight into production exactly as shown.</p>

        <ul class="pf-details">{details}</ul>

        <form id="pfForm" novalidate>
          <input type="hidden" name="_subject" value="Proof #{job} — decision from {customer}">
          <input type="hidden" name="Job" value="{job}">
          <input type="hidden" name="Customer" value="{customer}">
          <input type="hidden" name="Item" value="{item}">
          <input type="hidden" name="Decision" id="pfDecision" value="">
          <input type="hidden" name="_replyto" value="{email}">
          <input type="hidden" name="_autoresponse" value="Thanks {customer} — we've recorded your response to proof #{job}.

If you approved it, we'll begin production and let you know when it ships. If you asked for changes, we'll send an updated proof shortly.

Questions? Just reply to this email.

— Custom Creations Unlimited
{phone} · {cemail}">
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">

          <div class="pf-check">
            <label><input type="checkbox" class="pf-ck"> <span>Spelling and wording are correct</span></label>
            <label><input type="checkbox" class="pf-ck"> <span>Colors are correct</span></label>
            <label><input type="checkbox" class="pf-ck"> <span>Size and placement are correct</span></label>
          </div>
          <p class="pf-note">Tick all three to enable approval. We produce exactly what you approve, so please read carefully.</p>

          <div class="pf-actions">
            <button class="btn btn--gold btn--lg" type="button" id="pfApprove" disabled>Approve for production</button>
            <button class="btn btn--ghost btn--lg" type="button" id="pfReject">Request changes</button>
          </div>

          <div class="pf-changes" id="pfChanges">
            <div class="field"><label for="pfNotes">What needs to change?</label>
              <textarea class="textarea" id="pfNotes" name="Requested changes" rows="4"
                placeholder="e.g. change 'Est. 2020' to 'Est. 2021', move the logo up slightly"></textarea></div>
            <div class="pf-actions" style="margin-top:1rem">
              <button class="btn btn--gold btn--lg" type="button" id="pfSendChanges">Send change request</button>
            </div>
          </div>
        </form>
      </div>

      <div id="pfDone">
        <div class="ic"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <h1 id="pfDoneHead">Thank you!</h1>
        <p class="pf-lede" id="pfDoneMsg"></p>
      </div>
    </div>
  </div>

  <p class="pf-foot">Questions? Call {phone} or email <a href="mailto:{cemail}">{cemail}</a><br>
    <a href="{site}">ccucustom.com</a></p>
</div>

<script>
(function(){{
  var f=document.getElementById('pfForm'), cks=[].slice.call(document.querySelectorAll('.pf-ck'));
  var ok=document.getElementById('pfApprove'), no=document.getElementById('pfReject');
  var box=document.getElementById('pfChanges'), send=document.getElementById('pfSendChanges');
  var dec=document.getElementById('pfDecision');

  cks.forEach(function(c){{ c.addEventListener('change', function(){{
    ok.disabled = !cks.every(function(x){{return x.checked}});
  }}); }});

  no.addEventListener('click', function(){{ box.classList.add('on'); document.getElementById('pfNotes').focus(); }});

  function submit(decision, head, msg, btn){{
    if (f.elements['_gotcha'].value) return;
    dec.value = decision;
    btn.disabled = true; btn.textContent = 'Sending…';
    var fd = new FormData(f);
    fd.append('Submitted', new Date().toString());
    fetch('{endpoint}', {{method:'POST', body:fd, headers:{{'Accept':'application/json'}}}})
      .then(function(r){{ if(!r.ok) throw 0; done(head,msg); }})
      .catch(function(){{
        window.location.href='mailto:{cemail}?subject='+encodeURIComponent('Proof #{job} — '+decision)
          +'&body='+encodeURIComponent('Job: {job}\\nCustomer: {customer}\\nDecision: '+decision
          +'\\nNotes: '+(document.getElementById('pfNotes').value||'—'));
        done(head,msg);
      }});
  }}
  function done(head,msg){{
    document.getElementById('pfMain').style.display='none';
    document.getElementById('pfDoneHead').textContent=head;
    document.getElementById('pfDoneMsg').textContent=msg;
    document.getElementById('pfDone').classList.add('on');
    window.scrollTo({{top:0,behavior:'smooth'}});
  }}

  ok.addEventListener('click', function(){{
    submit('APPROVED','Approved — thank you!',
      'We\\'ve got your approval and your order is going into production. We\\'ll email you when it ships.', ok);
  }});
  send.addEventListener('click', function(){{
    submit('CHANGES REQUESTED','Change request received',
      'Thanks — we\\'ll make those updates and send you a revised proof shortly.', send);
  }});
}})();
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, help="your job/order number, e.g. 1042")
    ap.add_argument("--art", required=True, help="path to the proof image")
    ap.add_argument("--customer", default="")
    ap.add_argument("--email", default="", help="customer email (for their confirmation copy)")
    ap.add_argument("--item", default="")
    ap.add_argument("--detail", action="append", default=[],
                    help="a detail line; repeat for several")
    a = ap.parse_args()

    os.makedirs(os.path.join(OUT, "art"), exist_ok=True)
    token = secrets.token_hex(3)
    slug = f"{re.sub(r'[^A-Za-z0-9-]', '', a.job)}-{token}"

    ext = os.path.splitext(a.art)[1].lower() or ".png"
    artfile = f"{slug}{ext}"
    shutil.copyfile(os.path.expanduser(a.art), os.path.join(OUT, "art", artfile))

    e = html.escape
    details = "".join(f"<li>{e(d)}</li>" for d in (a.detail or ["(no details supplied)"]))
    greeting = f"{e(a.customer.split()[0])}, " if a.customer else ""

    page = PAGE.format(
        job=e(a.job), date=datetime.date.today().strftime("%B %-d, %Y"),
        artfile=e(artfile), customer=e(a.customer or "customer"),
        email=e(a.email), item=e(a.item), details=details,
        greeting=greeting, endpoint=FORM_ENDPOINT,
        phone=PHONE, cemail=EMAIL, site=SITE)

    path = os.path.join(OUT, slug + ".html")
    open(path, "w", encoding="utf-8").write(page)
    print("created  proof/%s.html" % slug)
    print("send     %s/proof/%s.html" % (SITE, slug))


if __name__ == "__main__":
    main()
