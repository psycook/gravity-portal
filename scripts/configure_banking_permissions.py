"""Apply Contact/Parent-scoped permissions without granting financial writes."""

import json
import os
from pathlib import Path
import subprocess
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path.home() / ".copilot" / "installed-plugins" / "awesome-copilot" / "dataverse"
sys.path.insert(0, str(PLUGIN / "scripts"))
from auth import get_client

WEBSITE = "1d1bdc36-85c2-f111-a05c-70a8a5b10130"
ROLE = "fb6c7532-85c2-f111-a05c-6045bd015270"
SCOPES = {"Contact": 756150001, "Parent": 756150003, "Self": 756150004}


def main():
    if os.environ.get("DATAVERSE_URL", "").rstrip("/") != "https://smc-diamond-service.crm.dynamics.com":
        raise SystemExit("Set DATAVERSE_URL to the confirmed Gravity demo environment.")
    client = get_client("dv-data")
    definitions = json.loads((ROOT / "power-pages" / "config" / "table-permissions.json").read_text())
    existing = {
        row["adx_entityname"]: row["adx_entitypermissionid"]
        for row in client.records.list(
            "adx_entitypermission", filter=f"_adx_websiteid_value eq {WEBSITE}"
        )
    }
    for definition in definitions["permissions"]:
        name = definition["name"]
        payload = {
            "adx_entityname": name,
            "adx_entitylogicalname": definition["table"],
            "adx_scope": SCOPES[definition["scope"]],
            "adx_websiteid@odata.bind": f"/adx_websites({WEBSITE})",
        }
        for privilege in ("Read", "Create", "Write", "Delete", "Append", "AppendTo"):
            payload["adx_" + privilege.lower()] = privilege in definition["privileges"]
        if definition["scope"] == "Contact":
            payload["adx_contactrelationship"] = definition["relationship"]
        elif definition["scope"] == "Parent":
            payload["adx_parentrelationship"] = definition["relationship"]
            payload["adx_parententitypermission@odata.bind"] = (
                f"/adx_entitypermissions({existing[definition['parentPermission']]})"
            )
        if name in existing:
            client.records.update("adx_entitypermission", existing[name], payload)
        else:
            existing[name] = client.records.create("adx_entitypermission", payload)
        associated = client.records.retrieve(
            "adx_entitypermission", existing[name],
            expand=["adx_entitypermission_webrole($select=adx_webroleid)"]
        )
        if not any(role["adx_webroleid"] == ROLE for role in associated["adx_entitypermission_webrole"]):
            subprocess.run([
                os.environ["COMSPEC"], "/c", shutil.which("dataverse"), "data", "associate",
                "--table", "adx_entitypermissions", "--id", existing[name],
                "--relationship", "adx_entitypermission_webrole",
                "--related", "adx_webroles", "--related-id", ROLE,
                "--environment", "https://smc-diamond-service.crm.dynamics.com/",
            ], check=True)
        print(name, existing[name], definition["privileges"], flush=True)


if __name__ == "__main__":
    main()
