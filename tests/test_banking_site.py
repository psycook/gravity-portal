"""Opt-in live tests using only the two approved synthetic QA customers."""

import json
import os
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, quote, urlparse
import uuid

from playwright.sync_api import sync_playwright

PLUGIN = Path.home() / ".copilot" / "installed-plugins" / "awesome-copilot" / "dataverse"
sys.path.insert(0, str(PLUGIN / "scripts"))
from auth import get_client

BASE = "https://gravity-bank-demo.powerappsportals.com"


@unittest.skipUnless(os.environ.get("GRAVITY_QA_STATE"), "Requires approved QA fixture state")
class BankingJourneys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = Path(os.environ["GRAVITY_QA_STATE"])
        cls.state = json.loads(cls.path.read_text())
        cls.client = get_client("dv-data")
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(channel="msedge", headless=True)
        cls.contexts = {}
        for key in ("alpha", "beta"):
            storage = cls.path.parent / (key + "-browser-state.json")
            context = cls.browser.new_context(
                storage_state=str(storage) if storage.exists() else None,
                viewport={"width": 1440, "height": 1000}
            )
            page = context.new_page()
            if not storage.exists():
                page.goto(BASE + "/SignIn", wait_until="networkidle")
                page.locator("#Username").fill(cls.state[key]["username"])
                page.locator("#PasswordValue").fill(cls.state[key]["password"])
                page.get_by_role("button", name="Sign in", exact=True).click()
                page.wait_for_load_state("networkidle")
                context.storage_state(path=str(storage))
            cls.contexts[key] = context
            page.close()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def page(self, key="alpha"):
        return self.contexts[key].new_page()

    def navigate(self, page, path):
        response = page.goto(BASE + path, wait_until="networkidle")
        self.assertEqual(response.status, 200)
        text = page.locator("main").inner_text()
        self.assertNotIn("Liquid error", text)
        self.assertNotIn("Exception", text)
        self.assertNotIn("does not expect", text)
        return text

    def portal_request(self, page, payload=None, method="POST", url="/_api/rfd_bankingrequests"):
        return page.evaluate("""async input => {
          const tokenResponse = await fetch('/_layout/tokenhtml', {cache:'no-store'});
          const tokenDocument = new DOMParser().parseFromString(await tokenResponse.text(), 'text/html');
          const token = tokenDocument.querySelector('input[name=__RequestVerificationToken]');
          if (!token) throw new Error('Native antiforgery token missing');
          const response = await fetch(input.url, {
            method:input.method, headers:{'Content-Type':'application/json',
            '__RequestVerificationToken':token.value},
            body:input.method==='GET'?undefined:JSON.stringify(input.payload)
          });
          return {status:response.status,id:response.headers.get('entityid'),body:await response.text()};
        }""", {"url": url, "method": method, "payload": payload})

    def payload(self, key="alpha", table="account", context=None, contact=None):
        customer = self.state[key]
        payload = {
            "rfd_name": "QA permission boundary",
            "rfd_subject": "QA permission boundary",
            "rfd_details": "Synthetic request used to test owned-record linking.",
            "rfd_requesttype": 228660000 if table == "account" else 228660002,
            "rfd_issimulated": True,
            "rfd_CustomerId@odata.bind": f"/contacts({contact or customer['contact']})",
        }
        field, entity = (
            ("rfd_FinancialAccountId", "rfd_financialaccounts") if table == "account"
            else ("rfd_FinancialTransactionId", "rfd_financialtransactions")
        )
        record = context or customer["accounts" if table == "account" else "transactions"][0]
        payload[field + "@odata.bind"] = f"/{entity}({record})"
        return payload

    def test_all_accounts_and_transaction_paging(self):
        page = self.page()
        try:
            text = self.navigate(page, "/my-gravity/")
            self.assertIn("Welcome back", text)
            self.assertNotIn("QA Beta", text)
            rows = set(page.locator("#accounts .account-row").evaluate_all("(els)=>els.map(e=>e.href)"))
            while page.get_by_role("link", name="More accounts", exact=True).count():
                page.get_by_role("link", name="More accounts", exact=True).click()
                page.wait_for_load_state("networkidle")
                rows.update(page.locator("#accounts .account-row").evaluate_all("(els)=>els.map(e=>e.href)"))
            self.assertEqual(len(rows), 13)
            self.assertEqual({url.split("id=")[-1] for url in rows}, set(self.state["alpha"]["accounts"]))
            account = self.state["alpha"]["accounts"][0]
            self.navigate(page, "/account/?id=" + account)
            self.assertEqual(page.locator(".transaction-row").count(), 25)
            self.assertIn("1,234.56", page.locator(".balance-card__amount").inner_text())
            transactions = set(page.locator(".transaction-row").evaluate_all("(els)=>els.map(e=>e.href)"))
            page.get_by_role("link", name="Older transactions", exact=True).click()
            page.wait_for_load_state("networkidle")
            transactions.update(page.locator(".transaction-row").evaluate_all("(els)=>els.map(e=>e.href)"))
            self.assertEqual(len(transactions), 27)
            self.assertEqual({url.split("id=")[-1] for url in transactions}, set(self.state["alpha"]["transactions"]))
        finally:
            page.close()

    def test_dashboard_shows_latest_eight_across_accounts(self):
        page = self.page()
        try:
            accounts = self.state["alpha"]["accounts"]
            rows = self.client.records.list(
                "rfd_financialtransaction",
                select=["rfd_financialtransactionid", "rfd_occurredon"],
                filter=" or ".join(f"_rfd_financialaccountid_value eq {account}" for account in accounts),
                orderby=["rfd_occurredon desc", "rfd_financialtransactionid asc"], top=8
            )
            expected = [row["rfd_financialtransactionid"] for row in rows]
            self.assertEqual(len(expected), 8)
            self.assertEqual(len(self.state["alpha"]["dashboard_transactions"]), 2)
            self.assertTrue(set(self.state["alpha"]["dashboard_transactions"]).issubset(expected))
            for path in ("/my-gravity/", "/my-gravity/?p=2"):
                self.navigate(page, path)
                actual = page.locator("#recent-activity .transaction-row").evaluate_all(
                    "(els)=>els.map(e=>new URL(e.href).searchParams.get('id'))"
                )
                self.assertEqual(actual, expected)
                self.assertNotIn("QA Beta", page.locator("#recent-activity").inner_text())
                self.assertLessEqual(page.locator("#requests .case-row").count(), 15)
            beta_page = self.page("beta")
            try:
                self.navigate(beta_page, "/my-gravity/")
                actual = beta_page.locator("#recent-activity .transaction-row").evaluate_all(
                    "(els)=>els.map(e=>new URL(e.href).searchParams.get('id'))"
                )
                self.assertEqual(set(actual), set(self.state["beta"]["transactions"]))
            finally:
                beta_page.close()
        finally:
            page.close()

    def test_all_five_linked_form_types(self):
        page = self.page()
        try:
            for kind, reason, value in (
                ("account", "request", 228660000),
                ("account", "complaint", 228660001),
                ("transaction", "query", 228660002),
                ("transaction", "dispute", 228660003),
                ("transaction", "fraud", 228660004),
            ):
                record = self.state["alpha"]["accounts" if kind == "account" else "transactions"][0]
                self.navigate(page, f"/banking-request/?kind={kind}&id={record}&reason={reason}")
                page.locator("#bankingRequestType").select_option(str(value))
                subject = "QA " + reason + " " + uuid.uuid4().hex[:8]
                page.locator("#bankingSubject").fill(subject)
                page.locator("#bankingDetails").fill("Synthetic demonstration. Please review this linked item.")
                page.locator("input[name=consent]").check()
                with page.expect_response(
                    lambda response: "/_api/rfd_bankingrequests" in response.url
                    and response.request.method == "POST"
                ) as response_info:
                    page.get_by_role("button", name="Send to Mission Control", exact=True).click()
                response = response_info.value
                self.assertIn(response.status, (201, 204),
                              response.text() if response.status not in (201, 204) else "")
                row_id = response.headers.get("entityid")
                self.assertTrue(row_id)
                row = self.client.records.retrieve("rfd_bankingrequest", row_id)
                self.assertEqual(row["rfd_subject"], subject)
                self.assertEqual(row["_rfd_customerid_value"], self.state["alpha"]["contact"])
                self.assertEqual(row["rfd_requesttype"], value)
                lookup = "_rfd_financialaccountid_value" if kind == "account" else "_rfd_financialtransactionid_value"
                self.assertEqual(row[lookup], record)
                other = "_rfd_financialtransactionid_value" if kind == "account" else "_rfd_financialaccountid_value"
                self.assertIsNone(row.get(other))
                self.assertTrue(row["rfd_issimulated"])
                page.locator(".form-status--success").wait_for()
                self.assertIn("No card has been frozen", page.locator("[data-form-status]").inner_text())
                self.assertTrue(page.get_by_role("button", name="Request saved", exact=True).is_disabled())
                self.navigate(page, "/my-gravity/")
                self.assertIn(subject, page.locator("#requests").inner_text())
        finally:
            page.close()

    def test_isolation_for_read_and_tampered_lookup_writes(self):
        page = self.page()
        beta_page = self.page("beta")
        try:
            for kind, records in (("account", "accounts"), ("transaction", "transactions")):
                other = self.state["beta"][records][0]
                text = self.navigate(page, "/" + kind + "/?id=" + other)
                self.assertIn("We can't find that item", text)
                self.assertNotIn("QA Beta", text)
                self.assertFalse(page.locator("[data-banking-form]").count())
                self.navigate(page, "/my-gravity/")
                result = self.portal_request(page, self.payload(table=kind, context=other))
                if result["status"] in (201, 204) and result["id"]:
                    self.client.records.delete("rfd_bankingrequest", result["id"])
                self.assertIn(result["status"], (401, 403, 404), result["body"])
            result = self.portal_request(page, self.payload(contact=self.state["beta"]["contact"]))
            if result["status"] in (201, 204) and result["id"]:
                self.client.records.delete("rfd_bankingrequest", result["id"])
            self.assertIn(result["status"], (401, 403, 404), result["body"])
            self.navigate(beta_page, "/my-gravity/")
            self.assertNotIn("QA Alpha", beta_page.locator("main").inner_text())
            self.assertEqual(beta_page.locator("#accounts .account-row").count(), 1)
            result = self.portal_request(beta_page, method="GET", url="/_api/rfd_bankingrequests?$select=rfd_subject")
            self.assertEqual(result["status"], 200, result["body"])
            self.assertEqual(json.loads(result["body"])["value"], [])
            latest = self.client.records.list(
                "rfd_bankingrequest",
                filter=f"_rfd_customerid_value eq {self.state['alpha']['contact']}",
                select=["rfd_bankingrequestid"], orderby=["createdon desc"], top=1
            ).first()
            result = self.portal_request(
                page, {"rfd_subject": "QA forbidden update"}, method="PATCH",
                url=f"/_api/rfd_bankingrequests({latest['rfd_bankingrequestid']})"
            )
            self.assertEqual(result["status"], 403, result["body"])
        finally:
            page.close()
            beta_page.close()

    def test_anonymous_invalid_links_cards_and_responsive_layout(self):
        anonymous = self.browser.new_context()
        page = anonymous.new_page()
        try:
            record = self.state["alpha"]["accounts"][0]
            text = self.navigate(page, "/account/?id=" + record)
            self.assertIn("Your orbit is private", text)
            self.assertNotIn("QA Alpha", text)
            self.assertIn("account", page.locator("main a[href*='returnUrl']").get_attribute("href"))
            result = self.portal_request(page, self.payload())
            self.assertIn(result["status"], (401, 403, 404), result["body"])
            transaction = self.state["alpha"]["transactions"][0]
            self.navigate(page, "/banking-request/?kind=transaction&id=" + transaction + "&reason=fraud")
            sign_in = page.locator("main a[href*='returnUrl']").get_attribute("href")
            return_path = parse_qs(urlparse(sign_in).query)["returnUrl"][0]
            params = parse_qs(urlparse(return_path).query)
            self.assertEqual(params["id"], [transaction])
            self.assertEqual(params["kind"], ["transaction"])
            self.assertEqual(params["reason"], ["fraud"])
        finally:
            anonymous.close()
        page = self.page()
        try:
            text = self.navigate(page, "/account/?id=" + quote("not-a-guid"))
            self.assertIn("We can't find that item", text)
            designs = json.loads((Path(__file__).parents[1] / "power-pages" / "config" / "card-designs.json").read_text())
            for i, design in enumerate(designs):
                self.navigate(page, "/account/?id=" + self.state["alpha"]["accounts"][i])
                expected = Path(design["source"]).with_suffix(".jpg").name
                self.assertIn(expected, page.locator(".banking-card-art img").get_attribute("src"))
                self.assertTrue(page.locator(".banking-card-art img").evaluate("(img)=>img.complete && img.naturalWidth>0"))
            self.navigate(page, "/account/?id=" + self.state["alpha"]["accounts"][-1])
            self.assertIn("venus", page.locator(".banking-card-art img").get_attribute("src"))
            self.assertNotIn("QA-ALPHA-013", page.locator("main").inner_text())
            self.navigate(page, "/banking-request/?kind=account&id=" + self.state["alpha"]["accounts"][-1])
            self.assertNotIn("QA-ALPHA-013", page.locator("main").inner_text())
            self.assertIn("Card ending 1012", page.locator(".banking-context").inner_text())
            beta_page = self.page("beta")
            self.navigate(beta_page, "/account/?id=" + self.state["beta"]["accounts"][0])
            self.assertIn("earth", beta_page.locator(".banking-card-art img").get_attribute("src"))
            beta_page.close()
            for width, height in ((1440, 900), (1280, 720), (390, 844)):
                page.set_viewport_size({"width": width, "height": height})
                for name, path in (
                    ("dashboard", "/my-gravity/"),
                    ("account", "/account/?id=" + self.state["alpha"]["accounts"][0]),
                    ("transaction", "/transaction/?id=" + self.state["alpha"]["transactions"][0]),
                    ("request", "/banking-request/?kind=account&id=" + self.state["alpha"]["accounts"][0]),
                ):
                    self.navigate(page, path)
                    self.assertTrue(page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
                    self.assertFalse(page.locator(".arc-dock").count())
                    self.assertLessEqual(
                        page.locator("main h1").evaluate("(el)=>parseFloat(getComputedStyle(el).fontSize)"), 48
                    )
                    if name == "dashboard":
                        sidebar = page.locator(".dashboard-sidebar")
                        cards = sidebar.locator(".card").evaluate_all(
                            "(els)=>els.map(e=>e.getBoundingClientRect().height)"
                        )
                        self.assertLess(cards[0], 430)
                        self.assertLess(cards[1], 320)
                        self.assertLess(cards[2], 320)
                        self.assertTrue(page.locator(".quick-action").evaluate_all("""els => els.every(el => {
                            const r = el.getBoundingClientRect();
                            return r.height >= 44 && el.scrollWidth <= el.clientWidth;
                        })"""))
                        if width >= 1280:
                            self.assertLessEqual(page.locator("#accounts .account-row").first.evaluate(
                                "(el)=>el.getBoundingClientRect().bottom"
                            ), height)
                        page.screenshot(path=str(self.path.parent / f"dashboard-density-{width}.png"))
                    page.screenshot(path=str(self.path.parent / f"banking-{name}-{width}.png"), full_page=True)
        finally:
            page.close()

    def test_request_failure_is_not_reported_as_completion(self):
        page = self.page()
        try:
            self.navigate(page, "/banking-request/?kind=account&id=" + self.state["alpha"]["accounts"][0])
            page.locator("#bankingSubject").fill("QA rejected submission")
            page.locator("#bankingDetails").fill("Synthetic failed request.")
            page.locator("input[name=consent]").check()
            page.route("**/_api/rfd_bankingrequests", lambda route: route.fulfill(
                status=403, content_type="application/json", body='{"error":{"message":"Rejected test request"}}'
            ))
            page.get_by_role("button", name="Send to Mission Control", exact=True).click()
            page.locator(".form-status--error").wait_for()
            self.assertIn("not accepted", page.locator("[data-form-status]").inner_text())
            self.assertFalse(page.locator(".form-status--success").count())
            self.assertTrue(page.get_by_role("button", name="Send to Mission Control", exact=True).is_enabled())
        finally:
            page.close()

    def test_existing_communication_form_still_saves(self):
        page = self.page()
        try:
            self.navigate(page, "/contact-us/")
            page.locator("#requestType").select_option("228660000")
            page.locator("#channel-message").check()
            page.locator("#subject").fill("QA communication regression " + uuid.uuid4().hex[:8])
            page.locator("#details").fill("Synthetic secure-message contact request.")
            page.locator("input[name=consent]").check()
            with page.expect_response(
                lambda response: "/_api/rfd_contactrequests" in response.url
                and response.request.method == "POST"
            ) as response_info:
                page.get_by_role("button", name="Send to Mission Control", exact=True).click()
            response = response_info.value
            self.assertIn(response.status, (201, 204),
                          response.text() if response.status not in (201, 204) else "")
            row = self.client.records.retrieve("rfd_contactrequest", response.headers["entityid"])
            self.assertEqual(row["_rfd_customerid_value"], self.state["alpha"]["contact"])
            self.assertEqual(row["rfd_preferredchannel"], 228660000)
            page.locator(".form-status--success").wait_for()
        finally:
            page.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
