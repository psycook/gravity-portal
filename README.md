# Gravity Bank

**Your money, your orbit.**

A multi-page Microsoft Power Pages customer website for Gravity, a fictional
UK retail bank. The experience combines a cinematic public website with a
Contact-authenticated customer area backed by Dataverse.

> Demonstration only. All customers, balances and activity must be synthetic.
> This is not a live banking service. Support submissions create demonstration
> records, not real card freezes, payments, refunds or lending decisions.

## Current experience

The deployed site is [Gravity Bank](https://gravity-bank-demo.powerappsportals.com).
Signed-in customers enter [My Gravity](https://gravity-bank-demo.powerappsportals.com/my-gravity/).

- Public pages cover Everyday, Save, Home buying, Borrow, Solar System, Proof,
  switching, Arc and Mission Control.
- My Gravity shows Contact-scoped accounts, the latest eight transactions
  across those accounts, and recent cases and requests.
- Account pages include supplied mock-card artwork and full, paged transaction
  histories. Transaction pages link to queries, disputes and suspected-fraud
  requests.
- Account requests, complaints and transaction support forms create linked
  Dataverse records. The communication form supports several contact options.

Authentication uses native Power Pages identities linked to Contacts.
Financial access is Contact- or Parent-scoped; there is no anonymous or global
financial-data permission. Arc is presented as AI, but the current website does
not establish a new live Copilot Studio connection or banking automation.

## Repository layout

| Path | Purpose |
|---|---|
| `power-pages\` | Editable pages, shared Liquid templates, CSS, JavaScript, configuration and implementation documentation |
| `scripts\` | Power Pages source generator, Dataverse provisioning, permissions and approved synthetic QA setup |
| `tests\` | Opt-in live banking-journey tests |
| `site-source\gravity-bank---gravity-bank-demo\` | Canonical Standard-model upload source, including stable record and attachment IDs |
| `solutions\RetailFinanceDemo\` | Exported and unpacked Dataverse solution metadata |
| `branding\` | Supplied artwork, design references and supporting collateral |
| `.github\` | Project-wide and Markdown-specific contributor instructions |
| `database-tables.md` | Customer and financial data-model documentation |
| `financial-transaction-table-definition.md` | Transaction schema and demonstration constraints |
| `financial-account-names.json` | Approved financial-account naming rules |

Edit the implementation in `power-pages\`, then run the generator. Commit both
the editable package and the resulting `site-source\` changes. Do not discard
the existing upload source or regenerate its record IDs: those IDs prevent
duplicate Power Pages records and stale web-file attachments.

Downloaded comparison copies in `banking-deployment-readback\`,
`deployed-site-export\` and `production-site-check\` are local diagnostics, not
additional source trees.

## Local prerequisites

The verified development environment is Windows with PowerShell, Python 3.13,
Node.js 24 and Power Platform CLI (PAC) 2.12.2. Git is needed for version control.
There is no npm application, package-manager build or standalone local portal
server in this project.

The Python dependency versions in [requirements.txt](requirements.txt) match
the working development environment. Pillow is used by the source generator;
the other dependencies support managed Dataverse access and live QA.

Dataverse scripts and live tests also require the installed Dataverse skills
plugin's managed `auth.py` helper. They currently locate it beneath:

```text
%USERPROFILE%\.copilot\installed-plugins\awesome-copilot\dataverse\scripts
```

Installing the Python requirements does not install that plugin or authenticate
the user. Local source generation and syntax checks do not need the plugin or
Dataverse credentials. Live browser tests use installed Microsoft Edge.

## Build and local checks

Run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --requirement .\requirements.txt

python .\scripts\build_power_pages_source.py
node --check .\power-pages\web-files\gravity.js
python -m compileall -q .\scripts .\tests
```

The generator assembles shared templates, embeds JavaScript in the layout and
creates web-sized card images without changing the branding originals.
JavaScript and SVG web-file attachments are blocked in the current environment,
so the deployed layout embeds the script and uses supplied PNG logos.

Inspect generated changes before committing. There is no configured linter;
the checks above validate source generation and Python/JavaScript syntax, not
live Dataverse access or rendered portal behaviour.

## Live tests and deployment

See [the Power Pages implementation guide](power-pages/README.md) for verified
deployment commands, table permissions, schema details and the opt-in test
command. See [the card mapping](power-pages/card-tier-mapping.md) for artwork
selection and fallbacks.

Live tests are **not an offline unit suite**. They need managed Dataverse
authentication, the approved synthetic QA Contacts and external fixture state.
Some tests create real demonstration support records in the target environment.
Keep QA credentials and authenticated browser state outside the repository;
never run these tests against real customer records.

The current deployment uses:

| Setting | Value |
|---|---|
| Dataverse environment | `https://smc-diamond-service.crm.dynamics.com/` |
| Dataverse solution | `RetailFinanceDemo` |
| Power Pages data model | Standard |
| Site | Production and Public |

Confirm the intended environment and verify the active PAC connection before
running any provisioning, data-write or deployment command. Do not use the
Enhanced-model upload flag `--modelVersion 2` for this site.

No automatic GitHub deployment is configured. Publishing, restarting the site,
changing permissions and seeding data require explicit approval.

## Design and contribution guidance

Read [the project instructions](.github/copilot-instructions.md) before making
changes. The visual reference is the
[approved Gravity homepage HTML concept](branding/website-single-page-proof-of-concept/gravity-homepage-concept.html),
not the alternative lime-accented preview or SharePoint palettes.

Gravity is the customer-facing bank; Singularity is the separate internal
SharePoint identity. Preserve the dark-first palette, supplied artwork,
consistent typography, UK English, visible focus and reduced-motion support.
Check changed pages at desktop and mobile sizes, including cross-page links and
the exact behaviour of financial and support journeys.

The supplied Office brand book and policy documents are encrypted or
rights-managed. Obtain accessible, authorised exports before deriving detailed
policy rules. Do not infer compliance from filenames.

## GitHub and sensitive files

Use a private repository unless the owner explicitly approves public release.
The ignore rules exclude local environment files, authentication material, QA
credentials/browser sessions, diagnostic exports, logs and Python caches.
They intentionally retain deployable source, unpacked solution XML and artwork.

Before staging files, inspect `git status --short` and review the staged diff.
Ignore rules are a safety net, not a guarantee: never commit passwords, tokens,
private keys, real customer records or personal test data. Already-tracked files
are not removed by adding an ignore rule.

The Git attributes preserve binary artwork and normalise text line endings.
Large branding images may be suitable for Git LFS if the owner chooses to
configure it; Git LFS is not currently required by this project.

No open-source licence has been selected. Do not assume permission to
redistribute supplied branding, protected documents or other collateral.
