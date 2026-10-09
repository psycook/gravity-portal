from pathlib import Path
import json
import re
import shutil
import uuid


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "power-pages"
SOURCE = ROOT / "site-source" / "gravity-bank---gravity-bank-demo"

HOME_ROOT_ID = "08057f2f-85c2-f111-a05c-70a8a5b10a71"
HOME_LOCAL_ID = "74bbfb32-85c2-f111-a05a-70a8a5b106ad"
PAGE_TEMPLATE_ID = "94e75b28-85c2-f111-a05c-70a8a5b10130"
WEB_TEMPLATE_ID = "a0a3e137-85c2-f111-a05c-70a8a5b10a05"
PUBLISHED_STATE_ID = "6570ef26-85c2-f111-a05a-6045bd061c5d"
WEBSITE_LANGUAGE_ID = "9da3e137-85c2-f111-a05c-70a8a5b10a05"
AUTHENTICATED_ROLE_ID = "fb6c7532-85c2-f111-a05c-6045bd015270"

PAGES = [
    ("home", "Home", "/", "home.html"),
    ("everyday", "Everyday", "everyday", "everyday.html"),
    ("save", "Save", "save", "save.html"),
    ("home-buying", "Home buying", "home-buying", "home-buying.html"),
    ("borrow", "Borrow", "borrow", "borrow.html"),
    ("solar-system", "Solar System", "solar-system", "solar-system.html"),
    ("proof", "Proof", "proof", "proof.html"),
    ("switch", "Switch", "switch", "switch.html"),
    ("arc", "Arc", "arc", "arc.html"),
    ("support", "Mission Control", "support", "support.html"),
    ("contact-us", "Contact us", "contact-us", "contact-us.html"),
    ("my-gravity", "My Gravity", "my-gravity", "my-gravity.html"),
    ("account", "Account", "account", "account.html"),
    ("transaction", "Transaction", "transaction", "transaction.html"),
    ("banking-request", "Banking request", "banking-request", "banking-request.html"),
]

ASSETS = [
    ("gravity.css", "text/css"),
    ("gravity-lockup-horizontal-on-dark.png", "image/png"),
    ("gravity-symbol-colour-glow.png", "image/png"),
    ("gravity-favicon-32.png", "image/png"),
    ("arc-agent-icon-192.png", "image/png"),
    ("gravity-grid-1920x1080.png", "image/png"),
    ("gravity-hero-singularity.jpg", "image/jpeg"),
    ("gravity-arc-ai-companion.jpg", "image/jpeg"),
    ("gravity-orbit-moons.jpg", "image/jpeg"),
    ("gravity-event-horizon-card.jpg", "image/jpeg"),
    ("gravity-liftoff-launch-arc.jpg", "image/jpeg"),
    ("gravity-look-up-moorland.jpg", "image/jpeg"),
    ("gravity-strong-pull-gravity-well.jpg", "image/jpeg"),
    ("gravity-solar-system-community.jpg", "image/jpeg"),
    ("gravity-mission-control-team.jpg", "image/jpeg"),
    ("gravity-observatory-dome.jpg", "image/jpeg"),
    ("gravity-star-trails.jpg", "image/jpeg"),
]


def new_id() -> str:
    return str(uuid.uuid4())


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def yaml_value(path: Path, field: str) -> str | None:
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{field}: "):
                return line.split(": ", 1)[1].strip()
    return None


def record_id(path: Path) -> str:
    return yaml_value(path, "adx_webpageid") or new_id()


def page_yaml(
    page_id: str,
    title: str,
    partial_url: str,
    *,
    root: bool,
    root_page_id: str | None = None,
    parent_page_id: str | None = None,
    display_order: int,
) -> str:
    lines = [
        f"adx_displayorder: {display_order}",
        "adx_enablerating: false",
        "adx_enabletracking: false",
        "adx_excludefromsearch: false",
        "adx_feedbackpolicy: 756150005",
        "adx_hiddenfromsitemap: false",
        f"adx_isroot: {'true' if root else 'false'}",
        f"adx_name: {title}",
        f"adx_pagetemplateid: {PAGE_TEMPLATE_ID}",
    ]
    if parent_page_id:
        lines.append(f"adx_parentpageid: {parent_page_id}")
    lines.extend(
        [
            f"adx_partialurl: {partial_url}",
            f"adx_publishingstateid: {PUBLISHED_STATE_ID}",
        ]
    )
    if root_page_id:
        lines.append(f"adx_rootwebpageid: {root_page_id}")
    lines.extend(
        [
            "adx_sharedpageconfiguration: false",
            f"adx_title: {title}",
            f"adx_webpageid: {page_id}",
        ]
    )
    if not root:
        lines.append(f"adx_webpagelanguageid: {WEBSITE_LANGUAGE_ID}")
    return "\n".join(lines) + "\n"


def build_template() -> str:
    layout = (PACKAGE / "web-templates" / "Gravity Layout.liquid").read_text(
        encoding="utf-8"
    )
    header = (PACKAGE / "web-templates" / "Gravity Header.liquid").read_text(
        encoding="utf-8"
    )
    footer = (PACKAGE / "web-templates" / "Gravity Footer.liquid").read_text(
        encoding="utf-8"
    )
    template = layout.replace(
        "{% include 'Gravity Header' %}", header
    ).replace("{% include 'Gravity Footer' %}", footer)
    template = template.replace("{{ page.adx_copy }}", "{% include 'Page Copy' %}")
    template = template.replace("{% block head %}{% endblock %}", "")
    template = template.replace("{% block scripts %}{% endblock %}", "")
    script = (PACKAGE / "web-files" / "gravity.js").read_text(encoding="utf-8")
    template = template.replace(
        '<script src="/gravity.js"></script>',
        f"<script>\n{script}\n</script>",
    )
    template = template.replace(
        "/gravity-lockup-horizontal-on-dark.svg",
        "/gravity-lockup-horizontal-on-dark.png",
    )
    template = template.replace(
        "/gravity-symbol-colour-glow.svg",
        "/gravity-symbol-colour-glow.png",
    )
    return template


def build_pages() -> None:
    pages_root = SOURCE / "web-pages"
    home_root_yaml = pages_root / "home" / "Home.webpage.yml"
    home_local_yaml = (
        pages_root / "home" / "content-pages" / "Home.en-US.webpage.yml"
    )
    write(
        home_root_yaml,
        page_yaml(
            HOME_ROOT_ID,
            "Home",
            "/",
            root=True,
            display_order=1,
        ),
    )
    write(
        home_local_yaml,
        page_yaml(
            HOME_LOCAL_ID,
            "Home",
            "/",
            root=False,
            root_page_id=HOME_ROOT_ID,
            display_order=1,
        ),
    )
    home_copy = (PACKAGE / "pages" / "home.html").read_text(encoding="utf-8")
    write(pages_root / "home" / "Home.webpage.copy.html", home_copy)
    write(
        pages_root / "home" / "content-pages" / "Home.en-US.webpage.copy.html",
        home_copy,
    )

    for order, (folder, title, partial_url, source_name) in enumerate(PAGES[1:], 2):
        page_dir = pages_root / folder
        content_dir = page_dir / "content-pages"
        file_title = title.replace(" ", "-")
        root_yaml = page_dir / f"{file_title}.webpage.yml"
        local_yaml = content_dir / f"{file_title}.en-US.webpage.yml"
        root_id = record_id(root_yaml)
        local_id = record_id(local_yaml)
        content = (PACKAGE / "pages" / source_name).read_text(encoding="utf-8")
        write(
            root_yaml,
            page_yaml(
                root_id,
                title,
                partial_url,
                root=True,
                parent_page_id=HOME_ROOT_ID,
                display_order=order,
            ),
        )
        write(page_dir / f"{file_title}.webpage.copy.html", content)
        write(page_dir / f"{file_title}.webpage.summary.html", "")
        write(page_dir / f"{file_title}.webpage.custom_css.css", "")
        write(page_dir / f"{file_title}.webpage.custom_javascript.js", "")
        write(
            local_yaml,
            page_yaml(
                local_id,
                title,
                partial_url,
                root=False,
                root_page_id=root_id,
                parent_page_id=HOME_ROOT_ID,
                display_order=order,
            ),
        )
        write(content_dir / f"{file_title}.en-US.webpage.copy.html", content)
        write(content_dir / f"{file_title}.en-US.webpage.summary.html", "")
        write(content_dir / f"{file_title}.en-US.webpage.custom_css.css", "")
        write(content_dir / f"{file_title}.en-US.webpage.custom_javascript.js", "")


def build_assets() -> None:
    target = SOURCE / "web-files"
    source = PACKAGE / "web-files"
    for order, (name, mime_type) in enumerate(ASSETS, 20):
        metadata_path = target / f"{name}.webfile.yml"
        web_file_id = yaml_value(metadata_path, "adx_webfileid") or new_id()
        annotation_id = yaml_value(metadata_path, "annotationid") or new_id()
        shutil.copy2(source / name, target / name)
        write(
            metadata_path,
            "\n".join(
                [
                    "adx_contentdisposition: 756150000",
                    f"adx_displayorder: {order}",
                    "adx_enabletracking: false",
                    "adx_excludefromsearch: true",
                    "adx_hiddenfromsitemap: false",
                    f"adx_name: {name}",
                    f"adx_parentpageid: {HOME_ROOT_ID}",
                    f"adx_partialurl: {name}",
                    f"adx_publishingstateid: {PUBLISHED_STATE_ID}",
                    f"adx_webfileid: {web_file_id}",
                    f"annotationid: {annotation_id}",
                    f"filename: {name}",
                    "isdocument: true",
                    f"mimetype: {mime_type}",
                    f"objectid: {web_file_id}",
                    "objecttypecode: adx_webfile",
                ]
            )
            + "\n",
        )


def build_banking_templates() -> None:
    from PIL import Image

    designs = json.loads((PACKAGE / "config" / "card-designs.json").read_text())
    lines = [
        "{% assign card_design = banking_account.rfd_carddesign.value %}",
        "{% unless card_design %}",
        "{% if banking_account.rfd_producttype.value == 100000005 or banking_account.rfd_producttype.value == 100000007 %}",
        "{% assign card_design = 228660004 %}",
        "{% else %}{% assign card_design = 228660003 %}{% endif %}",
        "{% endunless %}",
        "{% case card_design %}",
    ]
    for design in designs:
        name = Path(design["source"]).with_suffix(".jpg").name
        with Image.open(ROOT / "branding" / "Images" / "cards" / design["source"]) as image:
            image.thumbnail((360, 640), Image.Resampling.LANCZOS)
            image.convert("RGB").save(PACKAGE / "web-files" / name, quality=88, optimize=True)
        ASSETS.append((name, "image/jpeg"))
        lines.extend([
            f"{{% when {design['value']} %}}",
            f"{{% assign card_tier = '{design['tier']}' %}}",
            f"{{% assign card_planet = '{design['planet']}' %}}",
            f"{{% assign card_instrument = '{design['instrument']}' %}}",
            f'<img src="/{name}" alt="{design["planet"]} {design["tier"]} {design["instrument"].lower()} mock card" width="360" loading="lazy">',
        ])
    lines.extend(["{% endcase %}"])
    templates = {
        path.stem: path.read_text(encoding="utf-8")
        for path in (PACKAGE / "web-templates").glob("Gravity Banking *.liquid")
    }
    templates["Gravity Transaction Rows"] = (
        PACKAGE / "web-templates" / "Gravity Transaction Rows.liquid"
    ).read_text(encoding="utf-8")
    templates["Gravity Card Artwork"] = "\n".join(lines)
    for name, content in templates.items():
        directory = SOURCE / "web-templates" / name.lower().replace(" ", "-")
        metadata = directory / f"{name.replace(' ', '-')}.webtemplate.yml"
        template_id = yaml_value(metadata, "adx_webtemplateid") or new_id()
        write(metadata, f"adx_name: {name}\nadx_webtemplateid: {template_id}\n")
        write(directory / f"{name.replace(' ', '-')}.webtemplate.source.html", content)


def update_settings() -> None:
    settings_path = SOURCE / "sitesetting.yml"
    text = settings_path.read_text(encoding="utf-8")
    text = text.replace(
        "adx_name: Authentication/Registration/OpenRegistrationEnabled\n"
        "  adx_sitesettingid: 7d29132c-85c2-f111-a05c-6045bd015270\n"
        "  adx_value: true",
        "adx_name: Authentication/Registration/OpenRegistrationEnabled\n"
        "  adx_sitesettingid: 7d29132c-85c2-f111-a05c-6045bd015270\n"
        "  adx_value: false",
    )
    additions = [
        ("Webapi/rfd_contactrequest/enabled", "true"),
        (
            "Webapi/rfd_contactrequest/fields",
            "rfd_name,rfd_subject,rfd_details,rfd_requesttype,rfd_preferredchannel,"
            "rfd_preferredcontactvalue,rfd_preferredcontacttime,rfd_urgency,"
            "rfd_consenttocontact,rfd_source,rfd_issimulated,rfd_customerid,rfd_CustomerId",
        ),
        ("Webapi/rfd_bankingrequest/enabled", "true"),
        (
            "Webapi/rfd_bankingrequest/fields",
            "rfd_name,rfd_subject,rfd_details,rfd_requesttype,rfd_customerid,"
            "rfd_financialaccountid,rfd_financialtransactionid,rfd_issimulated,"
            "rfd_CustomerId,rfd_FinancialAccountId,rfd_FinancialTransactionId",
        ),
    ]
    for name, value in additions:
        if f"adx_name: {name}" not in text:
            text += (
                f"- adx_name: {name}\n"
                f"  adx_sitesettingid: {new_id()}\n"
                f"  adx_value: {value}\n"
            )
        else:
            pattern = (
                r"(?m)(^- adx_name: " + re.escape(name)
                + r"\n(?:  (?!adx_value:).*\n)*  adx_value: ).*$"
            )
            text, updated = re.subn(pattern, lambda match: match[1] + value, text)
            if updated != 1:
                raise ValueError(f"Expected one site setting to update: {name}")
    write(settings_path, text)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Downloaded Power Pages source not found: {SOURCE}")

    for blocked_name in (
        "gravity.js",
        "gravity.js.webfile.yml",
        "gravity-lockup-horizontal-on-dark.svg",
        "gravity-lockup-horizontal-on-dark.svg.webfile.yml",
        "gravity-symbol-colour-glow.svg",
        "gravity-symbol-colour-glow.svg.webfile.yml",
    ):
        blocked_path = SOURCE / "web-files" / blocked_name
        if blocked_path.exists():
            blocked_path.unlink()

    write(
        SOURCE
        / "web-templates"
        / "default-studio-template"
        / "Default-studio-template.webtemplate.source.html",
        build_template(),
    )
    write(
        SOURCE / "web-templates" / "header" / "Header.webtemplate.source.html",
        (
            PACKAGE / "web-templates" / "Gravity System Header.liquid"
        ).read_text(encoding="utf-8"),
    )
    write(
        SOURCE / "web-templates" / "footer" / "Footer.webtemplate.source.html",
        (
            PACKAGE / "web-templates" / "Gravity System Footer.liquid"
        ).read_text(encoding="utf-8"),
    )

    page_template = (
        SOURCE / "page-templates" / "Default-studio-template.pagetemplate.yml"
    )
    page_template_text = page_template.read_text(encoding="utf-8").replace(
        "adx_usewebsiteheaderandfooter: true",
        "adx_usewebsiteheaderandfooter: false",
    )
    write(page_template, page_template_text)

    build_pages()
    build_banking_templates()
    build_assets()
    update_settings()
    print(f"Gravity source built at {SOURCE}")


if __name__ == "__main__":
    main()
