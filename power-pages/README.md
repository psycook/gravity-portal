# Gravity Power Pages website

This folder contains the implementation package for Gravity's multi-page customer website. It is designed for a Power Pages site using the standard Contact identity model and the existing `RetailFinanceDemo` Dataverse solution.

## Included experience

- Public pages: Home, Everyday, Save, Home buying, Borrow, Solar System, Proof, switching, Arc and Mission Control.
- Authenticated `My Gravity` dashboard using Liquid and FetchXML to show Contact-scoped financial accounts, transactions, cases and contact requests.
- Authenticated communication request form using the Power Pages Web API to create `rfd_contactrequest` rows.
- Account drill-down with mock card artwork, balances and cookie-paged transactions.
- Transaction overviews with linked query, dispute and suspected-fraud forms.
- Account request and complaint forms creating Contact-owned `rfd_bankingrequest` rows.
- Shared Liquid header, footer and layout plus responsive CSS and JavaScript.
- Power Pages site-setting and table-permission specifications.
- A Dataverse schema contract for the Contact Request table.

All customer and financial content is explicitly presented as synthetic demonstration data. The site does not claim that a real payment, switch or lending decision has completed.

## Power Pages mapping

`scripts\build_power_pages_source.py` maps this package into the downloaded
Standard-model source at `site-source\gravity-bank---gravity-bank-demo`. It
preserves page, template, web-file and attachment GUIDs on rebuild. The shared
layout is deployed through the Default studio template; reusable banking
fragments are separate web templates. Shared JavaScript is embedded in the
layout because this environment blocks JavaScript web-file attachments.

The generator also creates web-sized card derivatives from the supplied
originals and synchronises the Web API field allowlists. Apply permissions with
`scripts\configure_banking_permissions.py`; the JSON specification uses verified
live relationship names, not inferred schema names.

| Page | Partial URL | Access |
|---|---|---|
| Home | `/` | Public |
| Everyday | `/everyday/` | Public |
| Save | `/save/` | Public |
| Home buying | `/home-buying/` | Public |
| Borrow | `/borrow/` | Public |
| Solar System | `/solar-system/` | Public |
| Proof | `/proof/` | Public |
| Switch | `/switch/` | Public |
| Arc | `/arc/` | Public |
| Mission Control | `/support/` | Public |
| Contact us | `/contact-us/` | Public page; form requires sign-in |
| My Gravity | `/my-gravity/` | Authenticated |
| Account | `/account/?id=<account GUID>` | Authenticated data; anonymous sign-in gate |
| Transaction | `/transaction/?id=<transaction GUID>` | Authenticated data; anonymous sign-in gate |
| Linked support | `/banking-request/?kind=account\|transaction&id=<GUID>` | Authenticated form |

## Account journeys

My Gravity lists every permitted financial account, including inactive and
closed accounts, in pages of 12. The deposit balance summary is explicitly for
the current page, not an incomplete all-account total. Recent activity shows
only the latest eight transactions across all the customer's accounts,
independently of account paging. The query uses an eight-row first page and
stable date/ID ordering, with an additional Liquid rendering limit: the portal
did not enforce the former FetchXML `top` limit with its permission rewriting.
Each account opens a
detail page with balances, safe account/card identifiers and up to 25
transactions per page. The transaction overview explains status, direction,
type, category, dates and available payment references.
Card products show only existing last-four digits, not their full holding
reference, on both the account and support-form screens.

Paging uses Dataverse cookies, stable tie-break ordering and first-page links.
XML cookies are URL-encoded twice for transport: raw XML in query parameters
otherwise triggers Power Pages request validation. The shared paging template
decodes one transport layer, then XML-escapes the cookie when constructing
FetchXML. Contact/Parent permissions still apply to every page of results.

See [card-tier-mapping.md](card-tier-mapping.md) for the eleven supplied designs,
explicit Dataverse selection and Everyday debit/credit fallbacks. The mapping
does not infer wealth, age eligibility or issued cards. The floating Arc dock is
omitted from financial and form pages so it cannot cover balances or controls;
Arc remains available through the footer and dashboard.

The dashboard, account, transaction and linked-support screens use a compact
customer-area type scale and spacing. Sidebar cards follow their content height
rather than stretching with the account lists; quick actions use aligned rows.
Public marketing heroes and the native sign-in styling remain unchanged.

## Banking Request table

Created in `RetailFinanceDemo`: `rfd_bankingrequest` (schema
`rfd_BankingRequest`, entity set `rfd_bankingrequests`).

| Display purpose | Actual logical name | Type |
|---|---|---|
| Primary name | `rfd_name` | Text |
| Subject | `rfd_subject` | Text, 200 characters |
| Details | `rfd_details` | Multiline text |
| Request type | `rfd_requesttype` | Choice |
| Review status | `rfd_requeststatus` | Choice |
| Demonstration flag | `rfd_issimulated` | Boolean |
| Signed-in customer | `rfd_customerid` | Required Contact lookup |
| Account context | `rfd_financialaccountid` | Financial Account lookup |
| Transaction context | `rfd_financialtransactionid` | Financial Transaction lookup |

Request types use `228660000` to `228660004`: account request, account
complaint, transaction query, transaction dispute and suspected fraud.
Status choices use `228660000` to `228660003`: New, In progress, Resolved and
Cancelled. An unset status is presented as New/untriaged; no workflow or
response-time promise is implied.

Account forms store the account lookup only. Transaction forms store the
transaction lookup only; its account is obtained through the existing financial
relationship, avoiding duplicate account/transaction links that could disagree.
The case-sensitive navigation properties are `rfd_CustomerId`,
`rfd_FinancialAccountId` and `rfd_FinancialTransactionId`. Both their navigation
names and logical column names are explicitly allowlisted for the portal API.
Customers cannot submit or update review status through this API.

Financial Account also has the optional choice `rfd_carddesign`. Its values and
artwork are sourced from `config\card-designs.json`. The installed SDK does not
accept a solution argument on `add_columns`, so the provisioning script adds
this column to the confirmed solution through PAC immediately after creation.

## Security requirements

- Use Contact- or Parent-scoped table permissions for every authenticated data surface. FetchXML filtering improves clarity but is not access control.
- Financial accounts and transactions have Read, Append and AppendTo, but no
  Write, Create or Delete. These association privileges support owned-record
  lookup binding; they do not permit financial changes. Cases remain Read-only.
- Contact Self permissions allow Read, Append and AppendTo only for the signed-in
  Contact. No global Contact access is granted.
- Both request tables allow Create, Read and association privileges for the
  signed-in Contact, but no customer Write or Delete. Tests verify that another
  Contact, account or transaction cannot be substituted in a create payload.
- Keep open registration disabled unless the identity journey is explicitly designed and approved. Use invitations or an approved external identity provider.
- Never expose PINs, passwords, one-time passcodes, full card numbers or internal servicing notes.

## Deployment status

The Production/public site is deployed at
<https://gravity-bank-demo.powerappsportals.com>, backed by
`https://smc-diamond-service.crm.dynamics.com/`. Financial records remain synthetic
and the forms create support records only: no freezes, reversals or refunds.

Verified PowerShell commands from the workspace root:

```powershell
python .\scripts\build_power_pages_source.py
node --check .\power-pages\web-files\gravity.js
pac pages upload --path .\site-source\gravity-bank---gravity-bank-demo --environment "https://smc-diamond-service.crm.dynamics.com/"
pac power-pages restart-website --environment "https://smc-diamond-service.crm.dynamics.com/" --id dec80edd-b4f5-4ef8-a955-fbdc71e3624c
```

This is the Standard data model. Do not pass `--modelVersion 2`. Hosting can
temporarily return HTTP 503 after a restart; wait for HTTP 200 before testing.
The metadata solution is exported/unpacked in `solutions\RetailFinanceDemo`.
Deployment readback is retained in `banking-deployment-readback`.

## Validation

`tests\test_banking_site.py` is an opt-in `unittest` suite using Python Playwright
with installed Edge and the managed Dataverse SDK. There is no separate npm
application or linter configuration.

```powershell
$env:DATAVERSE_URL = "https://smc-diamond-service.crm.dynamics.com/"
$env:TENANT_ID = "fc547a7e-3617-4e9c-a506-83fa37eb5247"
$env:GRAVITY_QA_STATE = "<absolute path to approved session-only QA fixture JSON>"
python -m unittest discover -s .\tests -p "test_banking_site.py" -v
```

The approved two-customer fixtures cover 13 accounts (including an inactive
account), 27 paged transactions plus two newer cross-account entries, the
dashboard's exact latest-eight limit and stable ordering across account pages,
all five linked form types, real Dataverse readback,
cross-customer read/write rejection, an anonymous gate, invalid identifiers,
eleven images and fallback artwork, desktop/mobile layouts, failed submissions,
and the existing communication form. QA credentials and authenticated browser
state stay outside deployed source and solution exports. Registration CAPTCHAs
must be completed by a person, never automated.
