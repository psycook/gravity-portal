# Financial Transaction: table definition

**Status: created and published in RetailFinanceDemo on 7 October 2026. The approved 8,015-record synthetic history batch has been loaded and reconciled against the existing account balances. The solution has since been exported and unpacked into `solutions\RetailFinanceDemo`.**

Approved and created on 7 October 2026 in the Gravity demonstration environment, `https://smc-diamond-service.crm.dynamics.com`. The business-behaviour sections below remain implementation requirements, not deployed validation or automation.

## Purpose

Store synthetic account activity for customer transaction histories, statements and demonstrations of Arc assistance. Each row represents one transaction on one financial account, such as a card purchase, salary payment, transfer, interest credit or loan repayment.

This is an account-activity model, not a production payment processor, double-entry general ledger, investment trade ledger or verified banking record. A row marked Posted means posted within the demonstration only.

## Table properties

| Property | Implemented definition |
|---|---|
| Display name | Financial Transaction |
| Plural display name | Financial Transactions |
| Schema name | `rfd_FinancialTransaction` |
| Logical name | `rfd_financialtransaction` |
| Entity set name | `rfd_financialtransactions` |
| Primary key | `rfd_financialtransactionid` - Dataverse-generated GUID |
| Primary name | `rfd_name` - Transaction number, autonumber text, maximum 50 characters |
| Autonumber format | `TXN-{SEQNUM:10}`; display reference only, not chronological ordering or an access credential |
| Ownership | User or team owned, for colleague access control |
| Table type | Standard Dataverse table; not an activity table |
| Attachments | Not required for the initial version |
| Auditing | Enabled on the new table and its custom business columns. Environment-wide auditing remains off; no organisation setting was changed |
| Solution | `RetailFinanceDemo` (unmanaged) |
| Publisher | Retail Finance Demo; unique name `RetailFinanceDemo`, customization prefix `rfd`, choice-value prefix `22866` |
| Table metadata ID | `cab8bb6c-5dc2-f111-a05c-6045bd015270` |

Column names below are the implemented logical names. Always use the actual case-sensitive Web API navigation properties when binding lookups.

### Implemented lookup navigation

| Lookup column | Web API navigation property | Relationship schema name | Delete behaviour |
|---|---|---|---|
| `rfd_financialaccountid` | `rfd_FinancialAccountId` | `rfd_FinancialAccount_FinancialTransactions` | Restrict |
| `rfd_cardinstrumentid` | `rfd_CardInstrumentId` | `rfd_CardInstrument_FinancialTransactions` | Restrict |
| `rfd_originaltransactionid` | `rfd_OriginalTransactionId` | `rfd_FinancialTransaction_Corrections` | Restrict |

For example, bind the account using `rfd_FinancialAccountId@odata.bind` and `/rfd_financialaccounts(<guid>)`, not the lowercase lookup logical name.

## Relationships and account coverage

```text
contact
   1
   |
   many
rfd_financialaccount
   1
   |
   | rfd_financialtransaction.rfd_financialaccountid
   many
rfd_financialtransaction
```

The required Financial Account lookup identifies the account whose balance the transaction affects. The customer is obtained through that account's existing `rfd_customerid` lookup to `contact`. Do not duplicate the customer on the transaction: that would allow conflicting customer/account links.

### Cards are instruments, not a second balance

The existing financial-account table contains both account holdings and card instruments. A debit-card purchase belongs to its linked current account; a credit-card purchase belongs to its linked credit card account. The optional Card Instrument lookup records which card was used.

The same row can therefore appear in both the account history and the card's activity view without creating two debits. An unlinked card must be flagged for correction, not assigned an invented underlying account.

Current, savings, ISA, mortgage, loan and credit card accounts can hold transactions directly. Card instruments get activity through the Card Instrument lookup. Investment account activity in this first version covers cash movements only, not holdings, units or trade settlement. An account classified as Other needs an agreed balance convention before generating its history.

## Columns

**Required** below distinguishes application-required metadata from conditional rules. Dataverse application-required fields alone do not guarantee API enforcement. Conditional requirements need explicit validation. The controlled synthetic-data loader validates the approved historical batch; no general-purpose server-side validation plug-in or flow has been deployed.

### Identity and account links

| Display name | Logical name | Type | Required | Purpose |
|---|---|---|---|---|
| Financial Transaction | `rfd_financialtransactionid` | GUID | System | Primary key |
| Transaction number | `rfd_name` | Autonumber text (50) | Generated | Stable customer-service/display reference |
| Financial Account | `rfd_financialaccountid` | Lookup to `rfd_financialaccount` | Yes | Account being debited or credited |
| Card Instrument | `rfd_cardinstrumentid` | Lookup to `rfd_financialaccount` | No | Debit or credit card used; must link to the Financial Account above |
| Original Transaction | `rfd_originaltransactionid` | Lookup to `rfd_financialtransaction` | Conditional | Original posted transaction for a linked refund or reversal |
| Transfer group reference | `rfd_transfergroupreference` | Text (100) | Conditional | Shared identifier connecting the two sides of an internal transfer |

All three lookup relationships restrict deletion of a referenced row rather than cascade-delete transaction history. Customer ownership continues to come from the financial account, not the transaction's Dataverse `ownerid`.

### Transaction details

| Display name | Logical name | Type | Required | Purpose |
|---|---|---|---|---|
| Description | `rfd_description` | Text (200) | Yes | Customer-readable description, such as `North Star Coffee` or `Monthly salary` |
| Transaction type | `rfd_transactiontype` | Choice | Yes | How the movement occurred; values below |
| Category | `rfd_category` | Choice | Yes | Spending/income classification; default Uncategorized |
| Direction | `rfd_direction` | Choice | Yes | Debit or Credit; values below |
| Transaction status | `rfd_transactionstatus` | Choice | Yes | Pending, Posted, Declined or Cancelled; no implicit Posted default |
| Amount | `rfd_amount` | Money | Yes | Positive magnitude, minimum GBP 0.01; direction carries the sign |
| Currency | `transactioncurrencyid` | Lookup to `transactioncurrency` | Yes | Standard Dataverse currency, explicitly GBP for this first demo |
| Occurred on | `rfd_occurredon` | Date and time, User Local | Yes | When the purchase, authorisation or payment happened |
| Posted on | `rfd_postedon` | Date and time, User Local | Conditional | Required only for Posted rows; empty otherwise |
| Value date | `rfd_valuedate` | Date Only | No | Effective banking date, distinct from processing time |
| Posting sequence | `rfd_postingsequence` | Whole number, minimum 1 | Conditional | Per-account ordering for Posted rows, including equal posting timestamps |
| Balance after | `rfd_balanceafter` | Money, signed | No | Reconciled account balance immediately after this posted movement |
| Payment reference | `rfd_paymentreference` | Text (100) | No | Synthetic reference shown on the statement |
| Counterparty name | `rfd_counterpartyname` | Text (150) | No | Synthetic merchant, employer, payee or payer name |
| Channel | `rfd_channel` | Choice | No | How the customer initiated the activity; values below |

Both Money columns use currency precision; GBP was confirmed active with two decimal places. Amount permits values from 0.01 to 1,000,000,000,000; Balance after permits values from -1,000,000,000,000 to 1,000,000,000,000. Posting sequence permits integers from 1 to 2,147,483,647. Dataverse supplies the standard base-currency companion columns and exchange-rate field. The standard currency lookup is application-required; no second custom currency lookup was created.

The transaction currency must match its financial account. Multi-currency purchases, original foreign amounts and exchange-rate calculations are deferred; do not label foreign amounts as GBP.

### Import and demonstration controls

| Display name | Logical name | Type | Required | Purpose |
|---|---|---|---|---|
| Source system | `rfd_sourcesystem` | Text (100) | Yes | For example, `GravityDemo`; identifies the generator/integration |
| Source reference | `rfd_sourcereference` | Text (100) | Yes | Stable source identifier for the same logical transaction across reruns |
| Demo batch reference | `rfd_demobatchreference` | Text (100) | Yes for generated data | Identifies an approved generation batch for reconciliation and targeted cleanup |
| Is simulated | `rfd_issimulated` | Yes/No | Yes; default Yes | Must remain Yes for all data created by this demonstration |

Dataverse supplies `createdon`, `modifiedon`, `createdby`, `modifiedby`, ownership, row version, `statecode` and `statuscode`. Do not use creation time as the date of a historical transaction.

## Choice definitions

All five choices are local. The actual values use the solution publisher's `22866` choice-value prefix, replacing the draft's `100000000` placeholders. Use the values below in integrations and synthetic-data generation.

| Column | Implemented values |
|---|---|
| `rfd_direction` | `228660000` Debit; `228660001` Credit |
| `rfd_transactionstatus` | `228660000` Pending; `228660001` Posted; `228660002` Declined; `228660003` Cancelled |
| `rfd_transactiontype` | `228660000` Card purchase; `228660001` Bank transfer; `228660002` Direct debit; `228660003` Standing order; `228660004` Cash withdrawal; `228660005` Cash deposit; `228660006` Interest; `228660007` Fee; `228660008` Refund; `228660009` Reversal; `228660010` Loan drawdown; `228660011` Repayment |
| `rfd_category` | `228660000` Uncategorized; `228660001` Groceries; `228660002` Eating out; `228660003` Transport; `228660004` Shopping; `228660005` Home and bills; `228660006` Entertainment; `228660007` Travel; `228660008` Health and wellbeing; `228660009` Income; `228660010` Savings and investments; `228660011` Transfers; `228660012` Interest; `228660013` Fees; `228660014` Borrowing repayments |
| `rfd_channel` | `228660000` Card in person; `228660001` Card online; `228660002` Cash machine; `228660003` Online banking; `228660004` Mobile banking; `228660005` Branch; `228660006` Automated; `228660007` Other |

Transaction type and category answer different questions: a salary can be a Bank transfer with category Income. A refund should normally retain the original purchase category so spending insights can net it correctly. Categorisation must not imply regulated advice.

## Balance and lifecycle rules

### Debit and credit

Store a positive Amount and a separate Direction. Do not store a negative Amount as well as Debit.

| Account convention | Debit | Credit |
|---|---|---|
| Deposit/cash account: positive balance means money held | Reduces balance | Increases balance |
| Existing Gravity lending/credit card account: negative balance means money owed | Makes the balance more negative; increases amount owed | Makes the balance less negative; reduces amount owed |

For example, a GBP 25.00 debit changes a deposit balance from GBP 500.00 to GBP 475.00. The same purchase changes a credit card balance from GBP -100.00 to GBP -125.00 (GBP 125.00 owed).

Live inspection before seeding confirmed that all existing mortgage, loan and credit card balances are negative. The approved history preserves this convention, replacing the draft's positive-debt example. For this batch, `next balance = previous balance + credits - debits` applies consistently to all balance-bearing accounts. Lending repayments may include interest and fees: this activity table must not automatically equate the full repayment with a reduction in `rfd_outstandingprincipal`.

### Posting and pending activity

Only Posted rows contribute to the booked balance. Pending rows may represent a hold but must not be included in that balance. Declined and Cancelled rows affect neither booked nor available balance.

The normal transitions are Pending to Posted, Declined or Cancelled. Pending to Posted updates the same row and preserves its source reference; it does not add a duplicate purchase. Directly imported historical rows may start as Posted.

Once posted, amount, direction, currency and account links are immutable. Corrections use a new transaction. Pending rows have no Posted on, Posting sequence or Balance after. Posted rows need a unique sequence within their account, ordered consistently with Posted on, which must not precede Occurred on.

Available balance is separate from booked balance and also depends on holds, overdrafts or credit limits. This table does not by itself implement an available-balance engine or release pending authorisations.

### Refunds and reversals

A Reversal points to the original Posted row, belongs to the same account and currency, has the opposite direction and reverses the full amount. Allow only one posted full reversal for an original row. The original remains Posted, so both entries stay in balance calculations and net to zero.

A linked Refund can be partial. It also uses the same account/currency and opposite direction. Validate cumulative posted refunds against the original amount, and disallow a full reversal after refunds unless a separately approved correction model handles it. Do not allow self-links or reversal/refund chains in the initial demo.

An unlinked external refund may be represented explicitly without inventing an original transaction. A Reversal always requires the Original Transaction lookup.

### Internal transfers

A transfer between two Gravity accounts produces two rows with the same Transfer group reference: a debit on the source account and a credit on the destination. For this GBP-only demo, their amount and currency must match; both accounts must be accessible to the acting customer.

Validate or atomically write both sides before reporting the simulated transfer as completed. Re-running an import must not create extra sides. Neither side is new income or spending when aggregating transfers between a customer's own deposit accounts.

### Reconciliation before seeding

Generating history must not silently change existing account balances. First agree a date range and a synthetic opening balance for each account. Apply Posted rows in Posting sequence order and reconcile the closing balance to `rfd_currentbalance` at `rfd_balanceasof`, or separately approve a balance update.

Do not invent a salary, fee or adjustment to conceal a mismatch. An opening balance is a statement starting point, not customer income. Leave Balance after empty until it can be reconciled; if populated, calculate it deterministically and recompute it when the underlying history changes.

## Uniqueness and validation

| Implemented alternate key | Columns | Purpose |
|---|---|---|
| `rfd_TransactionSourceKey` | `rfd_financialaccountid`, `rfd_sourcesystem`, `rfd_sourcereference` | Idempotent import/update of a logical account transaction |
| `rfd_AccountPostingSequenceKey` | `rfd_financialaccountid`, `rfd_postingsequence` | Unique posting order within each account |

Both key indexes reached Active after creation. Pending rows leave Posting sequence null; the second key is for Posted rows, not a pending-transaction identifier. Source references must be stable and use URL-safe letters, digits and hyphens for reliable alternate-key addressing.

Write validation must also enforce account/card compatibility, customer links to Contact, GBP currency, allowed state transitions, positive amounts, date/sequence consistency and the conditional rules above. Keep Dataverse row state separate from transaction status: inactivating a row is not a reversal and must not remove a posted movement from reconciliation.

These cross-field rules are required behaviour, not existing automation. Before seeding or exposing write operations, decide which controls require server-side enforcement and which are sufficient in a controlled synthetic-data loader. Do not permit unvalidated website writes.

## Access and data safeguards

Power Pages should initially expose read-only transaction history, using parent-scoped table permissions through Financial Account and its Contact customer relationship. Scope account and card views to the signed-in customer; UI filters alone are not access control. Configure and test permissions before exposing the table.

Do not publish transaction creation/update/delete endpoints to customers in the first version. An agreed server-side simulation handler can later perform validated actions on their behalf.

Use synthetic names and references only. Do not store full card numbers, CVVs, PINs, passwords, one-time passcodes or real payment credentials. Card display details can be obtained from the linked card's existing last-four field.

## Decisions before seeding or website integration

| Decision | Recommendation |
|---|---|
| Coverage of cards | One underlying account transaction with an optional card link; no duplicate card balance |
| Currency | GBP only for the initial demonstration |
| Refund/reversal model | Separate correction rows; preserve posted originals |
| Balance history | Reconcile synthetic history to existing balances without changing them by default |
| Initial website access | Customer-scoped, read-only histories |
| Solution and publisher | Confirmed: `RetailFinanceDemo`, publisher prefix `rfd` |
| Enforcement and auditing | Agree write-validation implementation and approve any audit configuration changes |
| Seed volume and scenarios | Agree transactions per account, history period and any pending/declined/refund examples separately |

Table creation and the historical seed batch below have been approved and performed. Further transaction seeding, balance changes, Power Pages permissions and additional validation/automation remain separate, explicitly approved steps.

## Approved synthetic transaction history

Batch `GRAVITY-TXN-2026-09-30-V1`, source system `GravityDemo`, was approved, created and reconciled on 7 October 2026. It covers 100 Contact customers and their 331 products: 233 balance-bearing accounts and 98 linked card instruments.

| Product | Accounts | Rows per account | Unique transaction rows |
|---|---:|---:|---:|
| Orbit / Event Horizon current accounts | 100 | 50 | 5,000 |
| Liftoff easy-access savings | 43 | 25 | 1,075 |
| Deep Space fixed-term savings | 3 | 10 | 30 |
| Zero-G cash ISAs | 37 | 20 | 740 |
| Constellation stocks and shares ISAs | 7 | 20 | 140 |
| Escape Velocity lifetime cash ISA | 1 | 10 | 10 |
| Landing mortgages | 8 | 10 | 80 |
| Momentum personal loans | 14 | 10 | 140 |
| Venus credit card accounts | 20 | 40 | 800 |
| **Total balance-bearing accounts** | **233** | **10-50** | **8,015** |

Each of the 78 debit cards has 30 linked rows; each of the 20 credit cards has 32. These are subsets of their underlying account histories, not additional transactions. The batch includes one linked partial refund per card, 98 in total.

The final Dataverse readback matched all 8,015 planned records, including their account/card/refund links, amounts, dates, source references and running balances. Every account's history closed at its existing balance, every card had its approved activity count, and all transaction numbers were unique. The account fields and customer location fields read before generation were unchanged afterwards.

### Generation and reconciliation rules

- The approved history window is 6 April to 30 September 2026, ending at the existing account balance snapshot. Activity starts after the relevant account/card opening date. The cancelled debit card has only pre-closure activity.
- Fictional shop, cafe, travel and payment descriptions use the linked Contact's town/city and postcode district across 20 UK towns and cities. No street addresses, full postcodes, sensitive personal traits or real merchant activity are inferred.
- Every row is explicitly simulated and Posted. Counterparties and descriptions identify the demonstration. There are no pending authorisations, declined payments or completed real-world banking actions.
- Current-account income and expenditure are constructed as coherent synthetic monthly budgets. Savings use external funding/withdrawals and illustrative interest. Fixed-term savings use interest credits only, with no invented early withdrawal.
- Cash ISAs and the lifetime cash ISA use illustrative contributions and interest, without invented government bonuses. Investment ISAs contain cash movements only, not trades or investment returns. Generated contributions do not exceed each account's existing ISA subscription total.
- These are selected synthetic activity examples, not a complete tax-year subscription ledger or verified interest schedule. Existing ISA subscription and allowance fields are unchanged; they must not be recalculated from this sample.
- Mortgage/loan histories use illustrative interest and repayments, with additional repayments where a recent opening provides fewer monthly periods. Credit card purchases, interest, partial refunds and repayments remain within the existing credit limit.
- Funding, withdrawals and repayments explicitly use fictional external counterparties. No unpaired internal Gravity transfers are created.
- The loader calculates a synthetic opening balance, then validates each running balance against the fixed closing balance. It does not add balancing adjustments or overwrite account balances. The opening balance can also be recovered from the first row's Balance after minus its signed movement.
- Stable source references, deterministic record IDs and the existing alternate keys support safe resumption. Existing matching transactions are checked and skipped, not rewritten. Purchases are created before their linked refunds.
- No contacts, account names, balances, currencies, product types, dates, card statuses, servicing restrictions or ISA fields are modified.

## Local solution export

The table was confirmed as a component of `RetailFinanceDemo`, and table-only publishing returned HTTP 204. Export attempts through both PAC CLI and the authenticated ExportSolution Web API failed with intermittent TLS/connection resets. No successful solution ZIP or unpacked source has been produced yet.

When connectivity is stable, complete the source export with these commands, running export and unpack separately:

```powershell
pac solution export --name RetailFinanceDemo --path ".\solutions\RetailFinanceDemo.zip" --managed false --environment "https://smc-diamond-service.crm.dynamics.com"
pac solution unpack --zipfile ".\solutions\RetailFinanceDemo.zip" --folder ".\solutions\RetailFinanceDemo" --packagetype Unmanaged
```

Verify the unpacked Financial Transaction definition and both alternate keys before removing the temporary ZIP. This workspace is not currently a Git repository, so no source commit or push has been made.
