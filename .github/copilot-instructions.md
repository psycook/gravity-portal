# GravityBank - Copilot instructions

Project-wide guidance for GitHub Copilot CLI. Entries marked TODO are placeholders for the project owner, not agent tasks or runnable commands.

## Project context

- Build a demonstration website on Microsoft Power Pages for **Gravity**, a fictional UK retail bank.
- Demonstrate how automation and AI agents can change retail banking, including customer self-service, assisted journeys and the work performed by bank colleagues. Show the customer need, agent assistance, automated process and human oversight, not just a chatbot or marketing page.
- The brand is bold, cinematic and inspired by the cosmic wonder of *Interstellar*: gravity, light, orbits, time and human connection. Use Gravity's supplied assets and original creative language, not film artwork, characters, dialogue, music or other film IP.
- This is a demonstration, not a live banking service. Use synthetic customer and financial data, clearly identify simulations, and do not imply that real accounts, payments or lending decisions have been created.

## Brand identity and authoritative references

- **Gravity is the bank's main brand and the identity of this Power Pages website. Singularity is the branding for the internal SharePoint site.** Keep these identities and site purposes separate.
- **The required website look and feel is the [Gravity homepage HTML concept](../branding/website-single-page-proof-of-concept/gravity-homepage-concept.html).** Open and inspect this page before implementing or changing the website UI. It is the visual reference, not a production application or a requirement to build a single-page site.
- The approved concept uses singularity imagery and the greeting "Welcome to the singularity." These are creative elements in that reference, not instructions to rename the bank or make the Power Pages site an intranet.
- Use the [brand reference](../branding/Images/buildkit/gravity-brand-reference.md) for supporting logo rules, language, products and agent behaviour where consistent with the owner's instructions and the approved HTML.
- Some supplied material calls the intranet "The Observatory". The owner's clarification that the internal SharePoint identity is Singularity takes precedence over that naming.
- The [separate homepage preview image](../branding/Images/imagery/gravity-home-page-preview.png) contains a different logo and lime-accented design. It is **not** the required look and feel for the Power Pages site. Do not blend that visual direction or the SharePoint theme palettes into the approved website design.

## Multi-page website requirement

- The final solution must implement **multiple Power Pages pages for the required sections**, not reproduce the concept as one long page with anchor-only navigation.
- Carry the concept's navigation and content into the agreed sitemap: Everyday, Save, Home (home buying), Borrow, Solar System and Proof, with appropriate pages for switching, Arc and Mission Control support. Keep the landing/homepage distinct from the "Home" mortgage and home-buying category.
- Use real page URLs for navigation between sections. In-page anchors can still support navigation within an individual page.
- Share the header, footer, navigation, typography, buttons, cards, styles and assets across pages. Preserve the concept's coherent visual identity rather than designing each page independently.
- Adapt the concept into maintainable Power Pages templates, page content and web files. Do not duplicate its entire HTML, embedded images and scripts on every page.
- The concept's sign-in toast and Arc conversation/Moon-creation interactions are browser-only demonstrations, not working authentication, banking operations or Copilot Studio connections. Implement the requested behaviour or clearly label an intentional simulation.

## Website design direction

- Preserve the approved concept's dark-first, spacious, premium treatment: an oversized cosmic hero, Gravity Grid and orbital motifs, restrained glow, translucent dark panels, fine borders, rounded cards and pill-shaped calls to action.
- Use light and gradients sparingly to draw attention to the important action. Avoid a generic banking template, lime accents from the alternative preview, cartoon space imagery or excessive animation.
- Core palette:

  | Colour | Hex | Main role |
  | --- | --- | --- |
  | Singularity Black | `#05060B` | Page background |
  | Deep Field | `#0D1124` | Dark surfaces |
  | Event Navy | `#151A35` | Raised surfaces |
  | Starlight | `#F5F2EC` | Primary text |
  | Moondust | `#9AA1B9` | Secondary text |
  | Horizon Violet | `#7B61FF` | Primary accent |
  | Photon Cyan | `#46E0F5` | Links, data and secondary accent |
  | Accretion Gold | `#FFB648` | Warm highlights |
  | Nebula Lilac | `#B4A6FF` | Accent text on dark |

- The Horizon gradient runs violet to cyan for primary actions. The Photon Ring runs gold through Hot White (`#FFF1D9`) and cyan to violet for signature hero/logo moments.
- Typography: **Lexend** for headings, **Lexend Exa** for widely tracked uppercase eyebrow labels, and **Inter** for body/UI. Use the supplied Segoe UI/system fallbacks. Headings are sentence case; monetary values use tabular figures.
- Reuse the [CSS design tokens](../branding/Images/buildkit/gravity-tokens.css) and [JSON design tokens](../branding/Images/buildkit/gravity-tokens.json) where compatible. The HTML concept's layout and component styling take precedence over starter defaults; for example, it uses 12/20/28 px surface radii. Do not assume importing the token stylesheet alone reproduces the approved design.
- Use the supplied logo artwork, not a typed recreation of the custom wordmark. Select the correct dark/light or monochrome variant, preserve proportions and clear space, and use the favicon mark at very small sizes.
- Imagery should combine cosmic scale with human warmth: light against darkness, orbital forms, British landscapes at night and real people. Use the provided library rather than film stills or unrelated stock imagery.
- Motion should "orbit, don't bounce": smooth, restrained easing with reduced-motion support. Preserve responsive layouts, keyboard navigation, visible focus, meaningful image alternatives and high-contrast usability.
- Target WCAG AA contrast: at least 4.5:1 for normal text and 3:1 for large text. Check actual backgrounds and gradient button states; decorative glow is not a substitute for contrast.

## Branding directory map

The workspace currently contains instruction files and supplied branding/reference material, not an exported Power Pages implementation or an established build/test project.

| Source | Contents and intended use |
| --- | --- |
| [Brand book](<../branding/Gravity Brand Book.pptx>) | Office presentation supplied as brand collateral; see the protected-document limitation below. |
| [Build kit](../branding/Images/buildkit/) | Brand reference, CSS/JSON tokens, Arc setup, web-chat styling, fraud-check Adaptive Card, SharePoint themes/script, Power Apps named formulas and Power BI theme. Start with its [README](../branding/Images/buildkit/README.md), but resolve paths against the actual workspace. |
| [SVG logos](../branding/Images/logos/svg/) and [PNG logos](../branding/Images/logos/png/) | Horizontal/stacked lockups, symbol and wordmark variants for dark/light and monochrome use; 13 files in each format. Prefer SVG for scalable web artwork. |
| [Icons](../branding/Images/icons/) | App icons, favicons, Teams icons, Arc avatar and agent icon. |
| [Patterns](../branding/Images/patterns/) | Gravity Grid backgrounds in 1920x1080, 2560x640 banner and 1080-square formats. |
| [Imagery](../branding/Images/imagery/) | Cosmic hero, gravity well, savings launch arc, moorland, community, Arc, card and Mission Control imagery, plus intranet/flight-manual concepts and the alternative homepage preview. |
| [Card artwork](../branding/Images/cards/) | Eleven planet-themed card designs plus a collection overview: Moon/Launchpad; Mars and Mercury/Starter; Earth and Venus/Everyday; Neptune and Uranus/Premier; Jupiter and Saturn/Wealth; Sun and Eclipse/Private. |
| [Themes](../branding/themes/) | Dark/light SharePoint/Fluent JSON palettes, matching the corresponding build-kit SharePoint palettes. These are not Power Pages CSS themes. |
| [Policy and procedure documents](../branding/polices/) | Eight Office documents. The existing directory is spelled `polices`; use that actual path rather than assuming `policies`. |

- Some build-kit examples refer to distribution folders named `gravity-brand-assets` or `gravity-website`, and to asset variants not present here. Use the actual files listed above; do not invent missing paths.
- Preserve supplied originals. Create appropriately sized web derivatives when necessary; the large card PNGs and the concept's embedded data URIs should not be copied indiscriminately into deployed pages.
- Card artwork is illustrative, not a source of product rules. For example, the collection overview labels Launchpad for ages 11-17 while the written reference and HTML describe ages 6-17. Confirm eligibility and any tier-to-product mapping before implementing those rules.

### Policy and procedure references

The following subjects are identifiable from the supplied filenames:

- FM-101: current account switching procedure.
- FM-102: fraud alert and card freeze procedure.
- FM-103: complaint triage procedure.
- FM-104: account opening and KYC procedure.
- FR-001: fraud and scams policy.
- FR-002: vulnerable customers and Soft Landing policy.
- FR-003: complaints handling policy.
- FR-004: responsible AI policy.

The supplied brand-book PPTX and all eight DOCX files currently use encrypted/rights-managed Office containers. Their document contents could not be read during the initial inspection. Obtain an accessible, authorised export before deriving detailed policy rules or claiming a workflow complies with them; filenames alone are not evidence of policy requirements.

## Language and banking content

- Use UK English, plain language, short sentences and a calm, candid, curious, warm voice. Format money in GBP with pence and dates for a UK audience.
- Core brand language includes "Your money, your orbit", "The smallest point. The strongest pull", and "Look up". Use it selectively; clarity about money, fees, risks and next steps comes first.
- Pair imaginative product names with plain descriptors: Orbit current account, Event Horizon premium current account, Liftoff easy-access saver, Deep Space fixed-term saver, Zero-G cash ISA, Escape Velocity first-home saving, Landing mortgages, Slingshot credit-builder card, Launchpad young people's accounts and Solar System shared money/community.
- Keep feature names consistent: Moons are pots, Boosters are round-ups, Lens provides insights, Pull brings accounts together and supports switching, Gravity Lock provides card/scam controls, Proof is the transparency hub, and Soft Landing is financial-difficulty support.
- Never describe a customer's money as a "black hole", trapped or impossible to withdraw. Restrict "nothing escapes" language to fraud/security. Avoid film references in customer-facing copy.
- Treat rates, fees, service promises, protection statements and example balances in the concept as demonstration content, not verified claims for a real bank. Keep the fictional/demo status visible and verify regulatory statements before any external real-world use.

## AI agents and automation demonstrations

- **Arc** is the customer-facing AI money companion; **Mission Control** is the human support team. Follow the [Arc setup and behaviour reference](../branding/Images/buildkit/arc-agent-instructions.md) when implementing its experience.
- Arc must identify itself as AI. Candour stays at 100%; wit defaults to 40%, with Brief/Balanced/Deep detail options. Wit drops to zero for fraud, complaints, bereavement, hardship or vulnerability, with a warm human handover.
- Confirm the amount, source and destination before a money-moving action, including in demonstrations. Never request PINs, passwords, one-time passcodes or full card numbers. Do not provide regulated financial advice or pretend missing account data is available.
- Make the difference between an explanation, a proposed action, a confirmed action and a completed action visible. Do not report completion when an operation failed or was never connected.
- Candidate demonstration journeys already supported by the reference material include switching, account opening/KYC, fraud alerts/card freezing, complaint triage, Soft Landing referrals and mortgage rate-switch reminders. Select the required journeys with the owner rather than automatically implementing every example.
- The wider kit also describes **Navigator** for colleague knowledge, **Flight Director** for orchestration and **Flight Plans** for Power Automate workflows. These are supporting integration concepts, not permission to build or modify a SharePoint site or other applications as part of every website task.
- For an agreed Copilot Studio integration, reuse the [web-chat style options](../branding/Images/buildkit/copilot-studio-webchat-styleoptions.json) and Arc assets, replacing placeholder URLs with actual hosted assets. The [fraud-check Adaptive Card](../branding/Images/buildkit/adaptive-card-arc-fraud-check.json) is a demo starting point; its submit actions require real handlers or clearly labelled simulation.

## Development workflow and change boundaries

- Keep the implementation centred on Power Pages. Confirm the site structure, environment and integration requirements before introducing a separate application framework or backend.
- No setup, preview, build, test, lint or deployment commands have been verified for this workspace yet. Do not infer them from the reference HTML or the scripts for other Microsoft products.
- TODO: Record the Power Pages site/environment, source/download layout and verified setup/preview commands.
- TODO: Record build, test and lint commands once tooling exists, or explicitly mark them not applicable.
- TODO: Record the approved deployment procedure and target environment.
- When implementing UI, compare the rendered pages with the approved HTML at desktop and mobile sizes. Validate cross-page links, consistent shared navigation, accessibility and the exact behaviour of the requested demonstrations.
- Do not overwrite branding originals, execute the SharePoint theme-application script, publish a site, change tenant/environment configuration or connect to real customer data without explicit approval.
