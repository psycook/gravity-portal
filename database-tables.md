# Database tables

This document describes the Dataverse tables used for customers, their financial accounts and financial transactions in the Gravity demonstration environment.

The [Financial Transaction table definition](financial-transaction-table-definition.md) documents `rfd_financialtransaction`, created and published in `RetailFinanceDemo` on 7 October 2026. It links transaction activity to `rfd_financialaccount` and optionally to a card instrument or original transaction. Both alternate keys are Active. Batch `GRAVITY-TXN-2026-09-30-V1` contains 8,015 simulated transactions covering all 331 products for 100 customers, with existing balances and customer records unchanged. The controlled loader validated and reconciled this batch; no general-purpose server-side validation automation has been deployed. The solution has since been exported and unpacked into `solutions\RetailFinanceDemo`.

> This is a demonstration data model. All customer and financial information must be synthetic and must not be treated as real banking data.

## Relationship overview

```text
contact (customer)
    1
    |
    | rfd_financialaccount.rfd_customerid
    |
    many
rfd_financialaccount (financial account)
```

Each demonstration customer is a row in `contact`. Each account belonging to that customer is a row in `rfd_financialaccount`.

Although `rfd_customerid` is a Dataverse Customer column that technically supports either `contact` or `account`, Gravity uses a `contact` reference for retail customers. The standard Dataverse `account` table represents organisations and must not be confused with a customer's banking account.

## Contact

| Property | Value |
|---|---|
| Display name | Contact |
| Logical name | `contact` |
| Collection name | `contacts` |
| Primary key | `contactid` |
| Primary name | `fullname` |
| Gravity purpose | Represents a retail banking customer |

Contact is a standard Dataverse table extended with Gravity-specific customer, identity and know-your-customer (KYC) fields. Power Pages identity fields are also present because contacts can represent authenticated website users.

### Core customer fields

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `contactid` | GUID | System | Unique customer identifier |
| `firstname` | Text (50) | No | Customer's first name |
| `middlename` | Text (50) | No | Customer's middle name |
| `lastname` | Text (50) | Yes | Customer's surname |
| `fullname` | Text (160) | Calculated | Customer's combined display name |
| `birthdate` | Date | No | Customer's date of birth |
| `emailaddress1` | Email (100) | No | Primary email address |
| `mobilephone` | Phone (50) | No | Mobile telephone number |
| `telephone1` | Phone (50) | No | Primary telephone number |
| `preferredcontactmethodcode` | Choice | No | Preferred contact channel |
| `address1_line1` | Text (250) | No | Primary address line 1 |
| `address1_line2` | Text (250) | No | Primary address line 2 |
| `address1_line3` | Text (250) | No | Primary address line 3 |
| `address1_city` | Text (80) | No | Primary address town or city |
| `address1_county` | Text (50) | No | Primary address county |
| `address1_postalcode` | Text (20) | No | Primary address postcode |
| `address1_country` | Text (80) | No | Primary address country |
| `statecode` | State | System | Active or inactive row state |
| `statuscode` | Status | System | Active or inactive row status |

### Gravity customer and KYC fields

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_customernumber` | Text (50) | No | Gravity customer reference |
| `rfd_demoaccountnumber` | Text (20) | No | Demonstration account or sign-in reference |
| `rfd_kycreference` | Text (200) | No | Reference for the simulated KYC process |
| `rfd_kycstatus` | Choice | No | Current KYC verification status |
| `rfd_kycriskrating` | Choice | No | KYC risk classification |
| `rfd_kycverifiedon` | Date | No | Date on which KYC was verified |
| `rfd_kycreviewdue` | Date | No | Date on which KYC should next be reviewed |
| `rfd_screeningstatus` | Choice | No | Customer screening result |

#### KYC status values

| Value | Label |
|---:|---|
| `100000000` | Not started |
| `100000001` | Pending |
| `100000002` | Verified |
| `100000003` | Review required |
| `100000004` | Not verified |
| `100000005` | Expired |

#### KYC risk rating values

| Value | Label |
|---:|---|
| `100000000` | Not assessed |
| `100000001` | Low |
| `100000002` | Standard |
| `100000003` | High |

#### Screening status values

| Value | Label |
|---:|---|
| `100000000` | Not screened |
| `100000001` | Pending |
| `100000002` | Clear |
| `100000003` | Potential match - review required |
| `100000004` | Confirmed match |
| `100000005` | Screening error |

### Power Pages identity fields

The table contains standard Power Pages identity columns prefixed with `adx_identity_`, including username, login enabled, lockout and authentication state. These fields support website identity and must not be used to store PINs, card details, one-time passcodes or other banking credentials.

## Financial Account

| Property | Value |
|---|---|
| Display name | Financial Account |
| Logical name | `rfd_financialaccount` |
| Collection name | `rfd_financialaccounts` |
| Primary key | `rfd_financialaccountid` |
| Primary name | `rfd_name` |
| Gravity purpose | Represents a customer-owned banking product, lending facility or card instrument |

Financial Account stores the customer's current accounts, savings accounts, ISAs, mortgages, loans, card accounts and card instruments. It is not the Dataverse organisation `account` table and is not a transaction ledger.

### Identity and ownership

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_financialaccountid` | GUID | System | Unique financial account identifier |
| `rfd_name` | Text (200) | Yes | Human-readable account name |
| `rfd_holdingnumber` | Text (50) | Yes | Stable identifier for the product holding |
| `rfd_customerid` | Customer lookup | Yes | Owning retail customer; Gravity references `contact` |
| `rfd_producttype` | Choice | Yes | Kind of banking product or instrument |
| `rfd_productid` | Lookup to `product` | No | Associated Dataverse product definition |
| `rfd_linkedfinancialaccountid` | Lookup to `rfd_financialaccount` | No | Related account, such as the account behind a card |
| `rfd_externalreference` | Text (100) | No | Identifier in an external or source system |
| `rfd_sourcesystem` | Text (100) | No | Name of the originating system |

### Account details and balances

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_accountnumber` | Text (34) | No | Account number |
| `rfd_sortcode` | Text (8) | No | UK sort code |
| `rfd_iban` | Text (34) | No | International Bank Account Number |
| `rfd_bic` | Text (11) | No | Bank Identifier Code |
| `rfd_currentbalance` | Money | No | Current account balance |
| `rfd_availablebalance` | Money | No | Balance currently available to the customer |
| `rfd_balanceasof` | Date and time | No | Time at which the balances were measured |
| `rfd_overdraftlimit` | Money | No | Agreed overdraft limit |
| `rfd_creditlimit` | Money | No | Credit limit for a lending or card product |
| `transactioncurrencyid` | Lookup to `transactioncurrency` | No | Currency used by money columns |

Dataverse also maintains corresponding base-currency columns, such as `rfd_currentbalance_base`, for money values.

### Lifecycle and servicing

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_lifecyclestatus` | Choice | No | Product lifecycle state |
| `rfd_openedon` | Date | No | Account opening date |
| `rfd_closedon` | Date | No | Account closure date |
| `rfd_maturitydate` | Date | No | Maturity date for fixed-term products |
| `rfd_productreviewdue` | Date | No | Next scheduled product review |
| `rfd_duediligencestatus` | Choice | No | Due-diligence state for the holding |
| `rfd_servicingrestriction` | Choice | No | Restriction applied to account servicing |
| `rfd_restrictionreason` | Multiline text | No | Explanation for a restriction |
| `rfd_servicingnotes` | Multiline text | No | Internal servicing notes for the demonstration |
| `statecode` | State | System | Active or inactive row state |
| `statuscode` | Status | System | Active or inactive row status |

### Interest and lending

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_annualinterestrate` | Decimal | No | Demonstration annual interest rate |
| `rfd_interestratetype` | Choice | No | Fixed, variable, tracker or introductory rate |
| `rfd_originalprincipal` | Money | No | Original amount borrowed |
| `rfd_outstandingprincipal` | Money | No | Principal still outstanding |
| `rfd_arrearsamount` | Money | No | Amount currently in arrears |
| `rfd_remainingtermmonths` | Integer | No | Remaining term in months |
| `rfd_repaymentfrequency` | Choice | No | Scheduled repayment frequency |
| `rfd_nextpaymentamount` | Money | No | Next scheduled payment amount |
| `rfd_nextpaymentdate` | Date | No | Next scheduled payment date |

### ISA fields

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_isatype` | Choice | No | Type of ISA |
| `rfd_isataxyear` | Text (7) | No | Tax year, for example `2026/27` |
| `rfd_isasubscriptionsytd` | Money | No | Subscriptions recorded in the current tax year |
| `rfd_isaremainingallowance` | Money | No | Demonstration remaining ISA allowance |
| `rfd_isflexibleisa` | Yes/No | No | Whether the product is represented as a flexible ISA |
| `rfd_isatransferreference` | Text (100) | No | ISA transfer reference |
| `rfd_isatransferstatus` | Choice | No | State of an ISA transfer |

ISA allowances and balances in this demonstration are synthetic. They must not be presented as verified tax guidance or real customer information.

### Card fields

| Column | Type | Required | Purpose |
|---|---|---:|---|
| `rfd_cardreference` | Text (100) | No | Internal card reference |
| `rfd_cardlastfour` | Text (4) | No | Last four digits used for safe display |
| `rfd_cardnetwork` | Choice | No | Card network |
| `rfd_cardstatus` | Choice | No | Card lifecycle or security state |
| `rfd_cardexpirymonth` | Integer | No | Expiry month |
| `rfd_cardexpiryyear` | Integer | No | Expiry year |
| `rfd_isvirtualcard` | Yes/No | No | Whether the instrument is virtual |

Do not add full card numbers, CVVs, PINs or one-time passcodes to this table.

### Product type values

| Value | Label |
|---:|---|
| `100000000` | Current account |
| `100000001` | Savings account |
| `100000002` | ISA |
| `100000003` | Mortgage |
| `100000004` | Loan |
| `100000005` | Credit card account |
| `100000006` | Debit card |
| `100000007` | Credit card |
| `100000008` | Investment account |
| `100000009` | Other |

### Lifecycle status values

| Value | Label |
|---:|---|
| `100000000` | Pending opening |
| `100000001` | Active |
| `100000002` | Restricted |
| `100000003` | Frozen |
| `100000004` | Dormant |
| `100000005` | Matured |
| `100000006` | Closed |

### Key relationships

| Column | Related table | Cardinality | Gravity use |
|---|---|---|---|
| `rfd_customerid` | `contact` or `account` | Many financial accounts to one customer | Use `contact` for retail customers |
| `rfd_productid` | `product` | Many financial accounts to one product | Optional product definition |
| `rfd_linkedfinancialaccountid` | `rfd_financialaccount` | Many financial accounts to one linked account | Connect a card or related holding to its underlying account |
| `transactioncurrencyid` | `transactioncurrency` | Many financial accounts to one currency | Currency for monetary values |

## Implementation conventions

- Use `contact.contactid` as the customer identifier.
- Link every financial account to its customer through `rfd_financialaccount.rfd_customerid`.
- Set `rfd_customerid` to a `contact` row for Gravity retail banking journeys.
- Use `rfd_holdingnumber` as the stable product-holding reference; do not rely on the display name as an identifier.
- Use `rfd_producttype` to determine which specialised fields and user interface sections apply.
- Treat balances, rates, allowances, card data and servicing states as synthetic demonstration values.
- Keep the distinction between a proposed action and a completed action visible in demonstrations. Updating a row alone must not imply that a real banking operation occurred.

Standard Dataverse ownership, auditing, currency, import and modification columns are present on both tables but are not repeated in full here.

## Gravity financial account naming catalogue

The following names were approved on 7 October 2026 for the 331 customer-owned financial accounts in `https://smc-diamond-service.crm.dynamics.com`. The deterministic replacement rules are held in [financial-account-names.json](financial-account-names.json).

The rename was applied on 7 October 2026 to all 331 accounts. Every account matched its approved name afterwards, with no original names remaining and no changes to the financial values, references, relationships or statuses checked against the pre-update snapshot.

Use the brand name followed by a plain product descriptor. Preserve an existing ` ending 1234` suffix exactly, including leading zeroes; never replace it with a full account or card number.

| Previous name, excluding suffix | Approved name, excluding suffix | Accounts in the approved rename |
|---|---|---:|
| Gravity Basic Current Account | Gravity Orbit basic current account | 26 |
| Gravity Everyday Current Account | Gravity Orbit everyday current account | 18 |
| Gravity Reward Current Account | Gravity Orbit rewards current account | 18 |
| Gravity Premium Current Account | Gravity Event Horizon premium current account | 38 |
| Gravity Easy Access Saver | Gravity Liftoff easy-access saver | 43 |
| Gravity 12 Month Fixed Saver | Gravity Deep Space 12-month fixed saver | 3 |
| Gravity Flexible Cash ISA | Gravity Zero-G flexible cash ISA | 37 |
| Gravity Stocks and Shares ISA | Gravity Constellation stocks and shares ISA | 7 |
| Gravity Lifetime Cash ISA | Gravity Escape Velocity lifetime cash ISA | 1 |
| Gravity Repayment Mortgage | Gravity Landing repayment mortgage | 8 |
| Gravity Personal Loan | Gravity Momentum personal loan | 14 |
| Gravity Credit Card Account | Gravity Venus credit card account | 20 |
| Gravity Visa Debit Card, linked to a basic, everyday or reward current account | Gravity Earth Visa debit card | 50 |
| Gravity Visa Debit Card, linked to a premium current account | Gravity Neptune Visa debit card | 28 |
| Gravity Mastercard Credit Card | Gravity Venus Mastercard credit card | 20 |
| **Total** | | **331** |

Orbit, Event Horizon, Liftoff, Deep Space, Zero-G, Escape Velocity and Landing build on the existing product universe. Constellation gives investment ISAs a shared identity; Momentum names personal lending. Earth, Neptune and Venus take their visual inspiration from the [Gravity card collection](branding/Images/cards/gravity-card-collection-overview.png).

The planet assignments are an approved branding convention, not new eligibility or pricing rules. Neptune is selected from the card's existing link to a premium account, not from the customer's age, balance or inferred wealth. Slingshot remains reserved for credit-builder products; these ordinary credit cards are not relabelled as credit-builder products.

This rename changes only `rfd_financialaccount.rfd_name`. It does not rename the `product` catalogue or change customer names, account numbers, holding references, balances, account types, card networks, linked accounts or product terms. Dataverse modification timestamps and any configured audit history may reflect the updates. The counts above describe this approved batch, not a permanent limit on future accounts.
