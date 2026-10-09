"""Create only the two approved synthetic customer identities and their test rows."""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import secrets
import sys
import uuid

PLUGIN = Path.home() / ".copilot" / "installed-plugins" / "awesome-copilot" / "dataverse"
sys.path.insert(0, str(PLUGIN / "scripts"))
from auth import get_client

WEBSITE = "1d1bdc36-85c2-f111-a05c-70a8a5b10130"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Pass a session-artifact JSON path outside deployed source.")
    if os.environ.get("DATAVERSE_URL", "").rstrip("/") != "https://smc-diamond-service.crm.dynamics.com":
        raise SystemExit("Set DATAVERSE_URL to the confirmed Gravity demo environment.")
    path = Path(sys.argv[1]).resolve()
    state = json.loads(path.read_text()) if path.exists() else {}
    client = get_client("dv-data")
    def navigation(table, attribute, target):
        matches = [
            rel["ReferencingEntityNavigationPropertyName"]
            for rel in client.tables.list_table_relationships(table)
            if rel.get("ReferencingEntity") == table
            and rel.get("ReferencingAttribute") == attribute
            and rel.get("ReferencedEntity") == target
        ]
        if len(matches) != 1:
            raise ValueError(f"Expected one navigation property for {table}.{attribute}")
        return matches[0] + "@odata.bind"

    customer_bind = navigation("rfd_financialaccount", "rfd_customerid", "contact")
    account_bind = navigation("rfd_financialtransaction", "rfd_financialaccountid", "rfd_financialaccount")
    invite_bind = navigation("adx_invitation", "adx_invitecontact", "contact")
    currencies = client.records.list(
        "transactioncurrency", filter="isocurrencycode eq 'GBP'", select=["transactioncurrencyid"]
    )
    currency = currencies.first()["transactioncurrencyid"]
    now = datetime.now(timezone.utc)

    def save():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    for index, key in enumerate(("alpha", "beta")):
        customer = state.setdefault(key, {"accounts": [], "transactions": []})
        if "contact" not in customer:
            customer["contact"] = client.records.create("contact", {
                "firstname": "Gravity QA", "lastname": key.title(),
                "emailaddress1": f"gravity.qa.{key}@example.com",
                "description": "Approved synthetic Power Pages QA identity. Not a real person.",
            })
            save()
        expected = 13 if key == "alpha" else 1
        while len(customer["accounts"]) < expected:
            i = len(customer["accounts"])
            account = client.records.create("rfd_financialaccount", {
                "rfd_name": f"QA {key.title()} Orbit {i + 1:02}",
                "rfd_holdingnumber": f"QA-{key.upper()}-{i + 1:03}",
                customer_bind: f"/contacts({customer['contact']})",
                "rfd_producttype": 100000000,
                "rfd_currentbalance": 1234.56 + i,
                "rfd_availablebalance": 1200.00 + i,
                "rfd_lifecyclestatus": 100000006 if i == 12 else 100000001,
                "rfd_cardlastfour": f"{i + 1000:04}",
                "rfd_carddesign": 228660000 + i % 11,
                "transactioncurrencyid@odata.bind": f"/transactioncurrencies({currency})",
            })
            customer["accounts"].append(account)
            save()
        expected = 27 if key == "alpha" else 2
        while len(customer["transactions"]) < expected:
            i = len(customer["transactions"])
            transaction = client.records.create("rfd_financialtransaction", {
                account_bind: f"/rfd_financialaccounts({customer['accounts'][0]})",
                "rfd_amount": 10.00 + i / 100,
                "rfd_description": f"QA {key.title()} purchase {i + 1:02}",
                "rfd_direction": 228660000,
                "rfd_occurredon": (now - timedelta(days=i)).isoformat(),
                "rfd_issimulated": True,
                "rfd_category": 228660001,
                "rfd_transactionstatus": 228660001,
                "rfd_transactiontype": 228660000,
                "rfd_sourcereference": f"GRV-QA-{key}-{i + 1:03}",
                "rfd_sourcesystem": "Gravity synthetic QA",
                "transactioncurrencyid@odata.bind": f"/transactioncurrencies({currency})",
            })
            customer["transactions"].append(transaction)
            save()
        if key == "alpha":
            dashboard_transactions = customer.setdefault("dashboard_transactions", [])
            while len(dashboard_transactions) < 2:
                i = len(dashboard_transactions)
                account = customer["accounts"][1 if i == 0 else -1]
                transaction = client.records.create("rfd_financialtransaction", {
                    account_bind: f"/rfd_financialaccounts({account})",
                    "rfd_amount": 24.50 + i,
                    "rfd_description": f"QA Alpha cross-account activity {i + 1}",
                    "rfd_direction": 228660000,
                    "rfd_occurredon": now.isoformat(),
                    "rfd_issimulated": True,
                    "rfd_category": 228660001,
                    "rfd_transactionstatus": 228660001,
                    "rfd_transactiontype": 228660000,
                    "rfd_sourcereference": f"GRV-QA-alpha-dashboard-{i + 1}",
                    "rfd_sourcesystem": "Gravity synthetic QA",
                    "transactioncurrencyid@odata.bind": f"/transactioncurrencies({currency})",
                })
                dashboard_transactions.append(transaction)
                save()
        if "invitation" not in customer:
            customer["code"] = str(uuid.uuid4())
            customer["invitation"] = client.records.create("adx_invitation", {
                "adx_name": f"Gravity QA {key.title()} invitation",
                "adx_type": 756150000,
                "adx_invitationcode": customer["code"],
                "adx_maximumredemptions": 1,
                "adx_expirydate": (now + timedelta(days=7)).strftime("%Y-%m-%d"),
                invite_bind: f"/contacts({customer['contact']})",
                "adx_website@odata.bind": f"/adx_websites({WEBSITE})",
            })
            customer["username"] = "gravity.qa." + key + "." + secrets.token_hex(4)
            customer["password"] = secrets.token_urlsafe(24) + "aA1!"
            save()
        if not customer.get("fallbacks_prepared"):
            if key == "alpha":
                client.records.update("rfd_financialaccount", customer["accounts"][-1], {
                    "statecode": 1, "statuscode": 2, "rfd_carddesign": None,
                    "rfd_producttype": 100000005,
                })
            else:
                client.records.update("rfd_financialaccount", customer["accounts"][0], {
                    "rfd_carddesign": None,
                })
            customer["fallbacks_prepared"] = True
            save()
        print(key, "synthetic customer ready:", len(customer["accounts"]), "accounts,",
              len(customer["transactions"]) + len(customer.get("dashboard_transactions", [])),
              "transactions", flush=True)


if __name__ == "__main__":
    main()
