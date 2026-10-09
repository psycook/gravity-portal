# Gravity account card artwork

This mapping governs illustrative card artwork on the authenticated Power Pages
account screen. It does not grant a tier, issue a card, define eligibility, or
change fees, rates or benefits. The PNG filenames are authoritative for the
creative pairings below.

| Tier | Debit artwork | Credit artwork |
|---|---|---|
| Launchpad | Moon | No supplied credit design; do not invent one |
| Starter | Mars | Mercury |
| Everyday | Earth | Venus |
| Premier | Neptune | Uranus |
| Wealth | Jupiter | Saturn |
| Private | Sun | Sun / Eclipse |

## Selection policy

An optional **Card design** choice (`rfd_carddesign`) on Financial Account selects
one of these eleven artworks explicitly. This records the design/tier/instrument
together and avoids conflicting tier and card selections. Colleagues choose it
on the Dataverse record; customers cannot edit it from the website.

For existing records with no choice:

- Current accounts and debit-card instruments display Everyday / Earth.
- Credit-card accounts and credit-card instruments display Everyday / Venus.
- Savings, ISAs, mortgages, loans, investments and other products display Earth
  only as an account illustration, with an explicit notice that no card is
  implied for that product.

Do not infer Starter, Premier, Wealth or Private from a customer's balance,
account name, age or borrowing. Those commercial tiers need a deliberate record
selection. Do not derive Launchpad age eligibility from card imagery: supplied
sources disagree on the age range.

Every image is labelled **Illustrative mock card**. Only the last four digits
from an existing account record may be shown separately. Artwork never indicates
a real issued card, live card controls or a completed banking action.

## Implementation

`config/card-designs.json` is the shared mapping for the Dataverse choice,
web-sized derivatives and the generated Liquid card template. The generator
creates 360-pixel-wide JPEGs, preserving the supplied PNG originals and their
portrait proportions. Every design is available; a missing explicit choice uses
the deterministic fallback above.
