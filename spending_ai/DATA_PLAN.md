# Spending AI Data Plan

## First target
Japan May/June.

## Sources
- messy travel notes
- bank/card exports
- Tricount exports
- cash withdrawal/exchange notes

## Truth model
- Bank/card exports show actual money leaving accounts.
- Cash notes explain where withdrawn cash went.
- Tricount explains shared expenses/reimbursements.
- Notes may contain item detail but may be incomplete.
- Avoid double-counting between notes, card exports, and Tricount.

## Core transaction fields
- date
- amount
- currency
- country
- category
- description
- source
- payment_method
- shared_status
- reimbursement_status
- confidence
- raw_text

## First analytics
- total spend
- daily burn
- spend by category
- large expenses
- possible leaks
- missing/uncategorised transactions
- cash vs card split
- country comparison later