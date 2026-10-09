"""Provision the Gravity linked-support schema in the confirmed demo environment."""

from enum import IntEnum
import argparse
import json
import os
from pathlib import Path
import sys
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path.home() / ".copilot" / "installed-plugins" / "awesome-copilot" / "dataverse"
sys.path.insert(0, str(PLUGIN / "scripts"))
from auth import get_client
from PowerPlatform.Dataverse.core.errors import HttpError

SOLUTION = "RetailFinanceDemo"
WEBSITE = "1d1bdc36-85c2-f111-a05c-70a8a5b10130"
ENVIRONMENT = "https://smc-diamond-service.crm.dynamics.com/"


class RequestType(IntEnum):
    ACCOUNT_REQUEST = 228660000
    ACCOUNT_COMPLAINT = 228660001
    TRANSACTION_QUERY = 228660002
    TRANSACTION_DISPUTE = 228660003
    SUSPECTED_FRAUD = 228660004


class RequestStatus(IntEnum):
    NEW = 228660000
    IN_PROGRESS = 228660001
    RESOLVED = 228660002
    CANCELLED = 228660003


def retry_metadata(operation):
    for attempt in range(5):
        try:
            return operation()
        except HttpError as error:
            if "running" not in str(error).lower() or attempt == 4:
                raise
            delay = 30 * (attempt + 1)
            print(f"Metadata lock: retrying in {delay}s", flush=True)
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    if os.environ.get("DATAVERSE_URL", "").rstrip("/") != ENVIRONMENT.rstrip("/"):
        raise SystemExit("Set DATAVERSE_URL to the confirmed Gravity demo environment.")
    client = get_client("dv-metadata")
    if args.inspect:
        for table in ("adx_entitypermission", "adx_webrole"):
            records = client.records.list(table, filter=f"_adx_websiteid_value eq {WEBSITE}")
            print(table, json.dumps([record.data for record in records], default=str))
        for table in ("rfd_financialaccount", "rfd_financialtransaction"):
            columns = client.tables.list_columns(
                table, select=["LogicalName", "SchemaName", "AttributeType"]
            )
            print(table, json.dumps(columns, default=str))
            print("relationships", json.dumps(
                client.tables.list_table_relationships(table), default=str
            ))
        return

    table = client.tables.get("rfd_BankingRequest")
    if not table:
        table = client.tables.create(
            "rfd_BankingRequest",
            {
                "rfd_Subject": "string",
                "rfd_Details": "memo",
                "rfd_RequestType": RequestType,
                "rfd_RequestStatus": RequestStatus,
                "rfd_IsSimulated": "bool",
            },
            solution=SOLUTION,
            primary_column="rfd_Name",
            display_name="Banking Request",
        )
        print("Created", table.logical_name, table.entity_set_name, flush=True)
        time.sleep(30)
        client = get_client("dv-metadata")
    columns = client.tables.list_columns("rfd_bankingrequest", select=["LogicalName"])
    existing = {c["LogicalName"] for c in columns}
    for schema, target, label, required in (
        ("rfd_CustomerId", "contact", "Customer", True),
        ("rfd_FinancialAccountId", "rfd_financialaccount", "Financial account", False),
        ("rfd_FinancialTransactionId", "rfd_financialtransaction", "Transaction", False),
    ):
        if schema.lower() not in existing:
            result = retry_metadata(lambda: client.tables.create_lookup_field(
                referencing_table="rfd_bankingrequest",
                lookup_field_name=schema,
                referenced_table=target,
                display_name=label,
                required=required,
                cascade_delete="Restrict",
                solution=SOLUTION,
            ))
            print(result.relationship_schema_name, result.lookup_schema_name, flush=True)
            time.sleep(30)
    designs = json.loads((ROOT / "power-pages" / "config" / "card-designs.json").read_text())
    choices = IntEnum("CardDesign", {
        f"{d['tier']} {d['planet']} {d['instrument']}".upper().replace(" / ", "_").replace(" ", "_"):
        d["value"] for d in designs
    })
    account_columns = client.tables.list_columns("rfd_financialaccount", select=["LogicalName"])
    if not any(c["LogicalName"] == "rfd_carddesign" for c in account_columns):
        retry_metadata(lambda: client.tables.add_columns(
            "rfd_financialaccount", {"rfd_CardDesign": choices}
        ))
        print("Added rfd_carddesign", flush=True)
        time.sleep(30)
        client = get_client("dv-metadata")
    design_metadata = client.tables.list_columns(
        "rfd_financialaccount", filter="LogicalName eq 'rfd_carddesign'", select=["MetadataId"]
    )[0]
    subprocess.run([
        "pac", "solution", "add-solution-component",
        "--solutionUniqueName", SOLUTION, "--component", design_metadata["MetadataId"],
        "--componentType", "2", "--environment", "https://smc-diamond-service.crm.dynamics.com/",
    ], check=True)
    print("Verified", json.dumps(
        client.tables.list_columns("rfd_bankingrequest", select=["LogicalName", "SchemaName", "AttributeType"]),
        default=str
    ), flush=True)


if __name__ == "__main__":
    main()
