# Customer proof approval

Static pages, no backend. One page per job, unguessable URL, decision arrives
by email through Formspree.

## Create a proof
    python3 scripts/new-proof.py --job 1042 \
      --art ~/Desktop/miller-board.png \
      --customer "Dana Miller" --email dana@example.com \
      --item "Custom Engraved Cutting Board" \
      --detail "Personalization: The Miller Family · Est. 2020" \
      --detail "Size: 12x18 walnut · Qty: 1"

It prints the URL to send. Commit and push, then the link is live.

## What the customer sees
The artwork, the order details, and three tick boxes — spelling, colors,
size/placement. **Approve is disabled until all three are ticked**, so an
approval is always an explicit confirmation of each point. They can instead
request changes and type what's wrong.

## What you get
An email with the job number, customer, decision (APPROVED or CHANGES
REQUESTED), any notes, and a timestamp. The customer gets a confirmation copy
automatically. If Formspree is ever unreachable the page falls back to opening
a pre-filled email, so a decision is never silently lost.

## Notes
- Pages are `noindex` and the URL carries a random token, but anyone with the
  link can view it. **Don't use this for artwork that must stay confidential** —
  that needs real authentication and a backend.
- `1042-839a5b.html` is a sample. Delete it and its file in `art/` when done.
- Endpoint/phone/email are constants at the top of `scripts/new-proof.py`.
