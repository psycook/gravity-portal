# Gravity Bank

**Your money, your orbit.**

Gravity is a fictional UK retail bank. This project implements a **multi-page Microsoft Power Pages website** demonstrating customer self-service and assisted banking journeys.

The aim is to show the whole experience: a customer's need, useful agent assistance, an automated process and human oversight when it matters.

> Demonstration only. Use synthetic customer and financial data. This is not a live banking service, and illustrative products, rates and actions must not be presented as real banking operations.

## Current status

The site is deployed at <https://gravity-bank-demo.powerappsportals.com>. The workspace contains public and authenticated pages, Dataverse-linked support forms, deployable Power Pages source, unpacked solution metadata and live regression tests.

See the [root README](../README.md) for repository layout, prerequisites, local checks and GitHub handling. The homepage concept remains a design prototype; its Arc interactions are not evidence of a live AI connection or money transfer.

## Website scope

The website uses **separate Power Pages pages for the required sections**, with real page URLs and consistent shared navigation. The single-page concept establishes the appearance, not the site architecture.

The reference content covers:

- **Everyday:** current accounts, Moons savings pots and everyday money management.
- **Save:** savings products, goals and round-ups.
- **Home:** home buying and mortgages, distinct from the website's landing page.
- **Borrow:** borrowing and credit-building products.
- **Solar System:** shared money, families and community.
- **Proof:** transparency, fees, service information and AI usage.
- Supporting journeys for switching, **Arc** and **Mission Control** customer support.

The implemented sitemap and account/support journeys are documented in the [Power Pages guide](../power-pages/README.md). Agree any additional journeys and integrations before implementing them.

## Brand and visual direction

**Gravity** is the bank's main brand and the identity of this website. **Singularity** is the identity of the internal SharePoint site, which is a separate experience.

The required website look and feel is the [Gravity homepage HTML concept](../branding/website-single-page-proof-of-concept/gravity-homepage-concept.html). Its singularity imagery and greeting are creative elements, not a change to the bank's name.

- Bold, cinematic imagery inspired by the cosmic wonder of *Interstellar*: gravity, light, orbits and human connection. Use original Gravity assets, not film artwork, dialogue or music.
- Dark-first backgrounds, Starlight text, violet/cyan accents and restrained gold highlights.
- Lexend headings, Lexend Exa labels and Inter body text.
- Spacious layouts, orbital motifs, rounded panels, pill-shaped buttons and subtle motion.
- UK English, plain financial language and a calm, candid, warm voice.
- Responsive, keyboard-accessible pages with visible focus, readable contrast and reduced-motion support.

The alternative lime-accented homepage preview and SharePoint theme files are **not** the website's visual reference. Use the [brand reference](../branding/Images/buildkit/gravity-brand-reference.md) and design tokens to support the approved HTML, not override it.

## AI and automation demonstrations

**Arc** is Gravity's customer-facing AI money companion. **Mission Control** is the human support team. Arc should identify itself as AI, explain its limits, confirm actions and offer a warm human handover for sensitive situations.

Candidate journeys include:

- Account opening and know-your-customer (KYC) checks.
- Current account switching.
- Fraud alerts and card freezing.
- Complaint triage.
- Soft Landing support for financial difficulty.
- Mortgage rate-switch reminders.

The supplied kit also describes **Navigator** for colleague knowledge, **Flight Director** for orchestration and **Flight Plans** for Power Automate workflows. Copilot Studio and Power Automate integrations are supporting options to be scoped, not existing connections.

Keep simulated and connected behaviour clearly distinguishable. Never report an action as completed unless it actually succeeded, and never use real customer credentials or financial data in demonstrations.

## Project resources

| Resource | Purpose |
| --- | --- |
| [Copilot instructions](copilot-instructions.md) | Detailed project requirements, design rules and development boundaries. |
| [Documentation instructions](instructions/documentation.instructions.md) | Editable guidance scoped to Markdown files. |
| [Homepage concept](../branding/website-single-page-proof-of-concept/gravity-homepage-concept.html) | Authoritative website look and feel; a single-page reference for the multi-page implementation. |
| [Brand book](<../branding/Gravity Brand Book.pptx>) | Supplied brand presentation; subject to the access limitation below. |
| [Build kit](../branding/Images/buildkit/README.md) | Brand reference, CSS/JSON tokens, Arc setup, chat styling and supporting Microsoft platform resources. |
| [Logos](../branding/Images/logos/), [icons](../branding/Images/icons/) and [patterns](../branding/Images/patterns/) | Supplied identity artwork and Gravity Grid backgrounds. |
| [Imagery](../branding/Images/imagery/) and [card artwork](../branding/Images/cards/) | Cosmic and human imagery, product visuals and planet-themed card designs. |
| [Themes](../branding/themes/) | SharePoint/Fluent palettes, not Power Pages stylesheets. |
| [Policies and procedures](../branding/polices/) | Eight documents covering switching, fraud, complaints, KYC, vulnerable customers and responsible AI. |

The policy directory is intentionally linked using its existing spelling, `polices`. Some build-kit examples use older distribution paths; resolve references against the actual workspace.

The supplied PowerPoint brand book and eight Word policy/procedure documents are encrypted or rights-managed. Their contents were not readable during the initial inspection. Accessible, authorised exports are needed before deriving policy requirements from them.

## Getting started

1. Read the [project instructions](copilot-instructions.md).
2. Open the approved HTML concept in a browser. From the project root, PowerShell can launch it with:

   ```powershell
   Start-Process '.\branding\website-single-page-proof-of-concept\gravity-homepage-concept.html'
   ```

3. Review the [build kit](../branding/Images/buildkit/README.md) and reusable assets.
4. Follow the [root README](../README.md) for local setup and checks. Confirm the target environment before running live tests, provisioning or deployment commands.

Verified generation, syntax-check, live-test and deployment commands are documented in the root README and Power Pages guide. There is no standalone local portal server or configured linter. Preserve the supplied branding originals, and obtain explicit approval before publishing a site or changing tenant/environment configuration.

### Working with GitHub Copilot CLI

Launch Copilot CLI from the project root:

```powershell
copilot
```

Run `/instructions` inside the session to check that the project instructions are discovered and enabled. File-specific instructions apply to matching `applyTo` patterns.

TODO entries in the instruction files are owner placeholders for decisions and verified commands, not tasks or commands for the agent to execute.
