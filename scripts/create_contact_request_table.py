from enum import IntEnum
from pathlib import Path
import sys
import time


PLUGIN_ROOT = Path.home() / ".copilot" / "installed-plugins" / "awesome-copilot" / "dataverse"
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from auth import get_client  # noqa: E402


SOLUTION = "RetailFinanceDemo"
TABLE_SCHEMA = "rfd_ContactRequest"
TABLE_LOGICAL = "rfd_contactrequest"


class RequestType(IntEnum):
    GENERAL_ACCOUNT_QUESTION = 228660000
    CURRENT_ACCOUNT_SWITCHING = 228660001
    CARD_OR_TRANSACTION_CONCERN = 228660002
    SAVINGS_OR_ISA_QUESTION = 228660003
    HOME_BUYING_OR_MORTGAGE_SUPPORT = 228660004
    BORROWING_SUPPORT = 228660005
    COMPLAINT = 228660006
    MONEY_WORRIES_OR_SOFT_LANDING = 228660007
    ACCESSIBILITY_OR_VULNERABILITY_SUPPORT = 228660008
    OTHER = 228660009


class PreferredChannel(IntEnum):
    SECURE_MESSAGE = 228660000
    PHONE_CALL = 228660001
    VIDEO_CALL = 228660002


class PreferredContactTime(IntEnum):
    ANY_TIME = 228660000
    MORNING = 228660001
    AFTERNOON = 228660002
    EVENING = 228660003


class Urgency(IntEnum):
    STANDARD = 228660000
    SOON = 228660001
    URGENT = 228660002


class RequestStatus(IntEnum):
    NEW = 228660000
    ACKNOWLEDGED = 228660001
    IN_PROGRESS = 228660002
    WAITING_FOR_CUSTOMER = 228660003
    RESOLVED = 228660004
    CANCELLED = 228660005


class Source(IntEnum):
    POWER_PAGES = 228660000
    ARC_HANDOVER = 228660001
    MISSION_CONTROL = 228660002
    OTHER = 228660003


def main() -> None:
    client = get_client("dv-metadata")
    existing = client.tables.get(TABLE_SCHEMA)

    if existing is None:
        info = client.tables.create(
            TABLE_SCHEMA,
            {
                "rfd_Subject": "string",
                "rfd_Details": "memo",
                "rfd_RequestType": RequestType,
                "rfd_PreferredChannel": PreferredChannel,
                "rfd_PreferredContactValue": "string",
                "rfd_PreferredContactTime": PreferredContactTime,
                "rfd_Urgency": Urgency,
                "rfd_RequestStatus": RequestStatus,
                "rfd_ConsentToContact": "bool",
                "rfd_Source": Source,
                "rfd_IsSimulated": "bool",
                "rfd_AcknowledgedOn": "datetime",
                "rfd_ResolvedOn": "datetime",
                "rfd_ResolutionSummary": "memo",
            },
            solution=SOLUTION,
            primary_column="rfd_Name",
            display_name="Contact Request",
        )
        print(
            "Created table:",
            info.schema_name,
            info.logical_name,
            info.entity_set_name,
            info.metadata_id,
        )
        time.sleep(15)
    else:
        print(
            "Reusing table:",
            existing.schema_name,
            existing.logical_name,
            existing.entity_set_name,
            existing.metadata_id,
        )

    columns = client.tables.list_columns(
        TABLE_LOGICAL,
        select=["LogicalName", "SchemaName", "AttributeType"],
    )
    has_customer = any(
        column.get("LogicalName") == "rfd_customerid" for column in columns
    )

    if not has_customer:
        relationship = client.tables.create_lookup_field(
            referencing_table=TABLE_LOGICAL,
            lookup_field_name="rfd_CustomerId",
            referenced_table="contact",
            display_name="Customer",
            description="The signed-in Gravity demonstration customer.",
            required=True,
            cascade_delete="Restrict",
            solution=SOLUTION,
        )
        print(
            "Created relationship:",
            relationship.relationship_schema_name,
            relationship.lookup_schema_name,
        )
        time.sleep(10)
    else:
        print("Reusing lookup: rfd_customerid")

    final = client.tables.get(TABLE_SCHEMA)
    print(
        "Verified:",
        final.schema_name,
        final.logical_name,
        final.entity_set_name,
        final.metadata_id,
    )


if __name__ == "__main__":
    main()
