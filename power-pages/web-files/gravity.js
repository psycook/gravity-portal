(function () {
  "use strict";

  var navToggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
  }

  var currentPath = window.location.pathname.toLowerCase();
  document.querySelectorAll(".primary-nav a").forEach(function (link) {
    var linkPath = new URL(link.href, window.location.origin).pathname.toLowerCase();
    if (linkPath !== "/" && currentPath.indexOf(linkPath) === 0) {
      link.setAttribute("aria-current", "page");
    }
  });

  document.querySelectorAll("[data-contact-form]").forEach(function (form) {
    form.addEventListener("submit", submitContactRequest);
  });
  document.querySelectorAll("[data-banking-form]").forEach(function (form) {
    form.addEventListener("submit", submitBankingRequest);
  });

  function submitBankingRequest(event) {
    event.preventDefault();
    var form = event.currentTarget;
    if (form.getAttribute("aria-busy") === "true" || form.getAttribute("data-sent") === "true") return;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    var submit = form.querySelector("[type=submit]");
    var status = form.querySelector("[data-form-status]");
    var data = new FormData(form);
    var kind = form.getAttribute("data-context-kind");
    var contextId = form.getAttribute("data-context-id");
    var contactId = form.getAttribute("data-contact-id");
    var type = Number(data.get("requestType"));
    var validTypes = kind === "account" ? [228660000, 228660001] : [228660002, 228660003, 228660004];
    var guid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!guid.test(contextId) || !guid.test(contactId) || ["account", "transaction"].indexOf(kind) < 0 || validTypes.indexOf(type) < 0) {
      showFormStatus(status, "error", "This request link is incomplete. Return to your account or transaction and open a new request.");
      return;
    }
    var subject = clean(data.get("subject"));
    var details = clean(data.get("details"));
    if (!subject || !details) {
      showFormStatus(status, "error", "Enter a subject and details before sending.");
      return;
    }
    var payload = {
      rfd_name: subject,
      rfd_subject: subject,
      rfd_details: details,
      rfd_requesttype: type,
      rfd_issimulated: true
    };
    payload["rfd_CustomerId@odata.bind"] = "/contacts(" + contactId + ")";
    if (kind === "account") {
      payload["rfd_FinancialAccountId@odata.bind"] = "/rfd_financialaccounts(" + contextId + ")";
    } else {
      payload["rfd_FinancialTransactionId@odata.bind"] = "/rfd_financialtransactions(" + contextId + ")";
    }
    form.setAttribute("aria-busy", "true");
    submit.disabled = true;
    submit.textContent = "Saving request...";
    safeAjax({
      type: "POST",
      url: "/_api/rfd_bankingrequests",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function (_response, _text, xhr) {
        form.setAttribute("data-sent", "true");
        var entityId = xhr.getResponseHeader("entityid");
        showFormStatus(status, "success", "Your demonstration request is saved for human review." +
          (entityId ? " Reference: " + shortReference(entityId) + "." : " The response did not include a reference; check My Gravity before sending again.") +
          " No card has been frozen, payment reversed or refund issued.");
      },
      error: function (xhr) {
        if (xhr.stage === "token") {
          showFormStatus(status, "error", "Your request was not sent because a secure form token could not be obtained. Refresh the page and check your sign-in before trying again.");
          return;
        }
        var uncertain = !xhr.status || xhr.status >= 500;
        showFormStatus(status, "error", uncertain ?
          "We could not confirm whether your request was saved. Check My Gravity before trying again to avoid a duplicate." :
          "Your request was not accepted. Check your sign-in and account link, then try again. Error " + xhr.status + ".");
      },
      complete: function () {
        form.setAttribute("aria-busy", "false");
        submit.disabled = form.getAttribute("data-sent") === "true";
        submit.textContent = submit.disabled ? "Request saved" : "Send to Mission Control";
      }
    });
  }

  function showFormStatus(element, state, message) {
    element.className = "form-status form-status--" + state + " is-visible";
    element.textContent = message;
    element.focus();
  }

  function submitContactRequest(event) {
    event.preventDefault();
    var form = event.currentTarget;
    var submit = form.querySelector("[type=submit]");
    var status = form.querySelector("[data-form-status]");

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var data = new FormData(form);
    var contactId = form.getAttribute("data-contact-id");

    status.className = "form-status";
    status.textContent = "";
    submit.disabled = true;
    submit.textContent = "Sending request...";

    var payload = {
      rfd_name: clean(data.get("subject")),
      rfd_subject: clean(data.get("subject")),
      rfd_details: clean(data.get("details")),
      rfd_requesttype: Number(data.get("requestType")),
      rfd_preferredchannel: Number(data.get("preferredChannel")),
      rfd_preferredcontactvalue: clean(data.get("contactValue")),
      rfd_preferredcontacttime: Number(data.get("preferredTime")),
      rfd_urgency: Number(data.get("urgency")),
      rfd_consenttocontact: data.get("consent") === "on",
      rfd_source: 228660000,
      rfd_issimulated: true
    };

    if (contactId) {
      payload["rfd_CustomerId@odata.bind"] = "/contacts(" + contactId.replace(/[{}]/g, "") + ")";
    }

    safeAjax({
      type: "POST",
      url: "/_api/rfd_contactrequests",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function (_data, _status, xhr) {
        var entityId = xhr.getResponseHeader("entityid");
        status.className = "form-status form-status--success is-visible";
        status.textContent = "Your demonstration request has been saved for Mission Control to review. No automatic response or real banking action has been started. Reference: " + shortReference(entityId);
        form.reset();
        status.focus();
      },
      error: function (xhr) {
        var message = "We lost signal for a moment. Your request was not sent. Please try again.";
        try {
          var response = JSON.parse(xhr.responseText);
          if (response && response.error && response.error.message) {
            message += " " + response.error.message;
          }
        } catch (_error) {
          // Keep the clear customer-safe error above.
        }
        status.className = "form-status form-status--error is-visible";
        status.textContent = message;
        status.focus();
      },
      complete: function () {
        submit.disabled = false;
        submit.textContent = "Send to Mission Control";
      }
    });
  }

  function safeAjax(options) {
    var stage = "token";
    fetch("/_layout/tokenhtml", {credentials: "same-origin", cache: "no-store"}).then(function (response) {
      if (!response.ok) throw new Error("Secure form token unavailable.");
      return response.text();
    }).then(function (html) {
      var document = new DOMParser().parseFromString(html, "text/html");
      var input = document.querySelector("input[name=__RequestVerificationToken]");
      if (!input || !input.value) throw new Error("Secure form token was not returned by Power Pages.");
      stage = "request";
      var headers = Object.assign({}, options.headers, {
        "Content-Type": options.contentType,
        "Accept": "application/json",
        "__RequestVerificationToken": input.value
      });
      return fetch(options.url, {
        method: options.type, headers: headers, body: options.data,
        credentials: "same-origin", redirect: "error"
      });
    }).then(function (response) {
      if (!response.ok) {
        return response.text().then(function (body) {
          if (options.error) options.error({status: response.status, responseText: body, stage: stage});
        });
      }
      if (options.success) options.success(null, "success", {
        getResponseHeader: function (name) { return response.headers.get(name); }
      });
    }).catch(function (error) {
      if (options.error) options.error({
        status: 0, stage: stage,
        responseText: JSON.stringify({error: {message: error.message}})
      });
    }).finally(function () {
      if (options.complete) options.complete();
    });
  }

  function clean(value) {
    return String(value || "").trim();
  }

  function shortReference(entityId) {
    if (!entityId) return "pending";
    return entityId.replace(/[{}-]/g, "").slice(0, 10).toUpperCase();
  }
})();
