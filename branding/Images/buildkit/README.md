# GRAVITY — Build Kit v1.0
Everything needed to build websites, SharePoint sites, apps, workflows and agents in the Gravity brand.
Gravity is a fictional concept brand for demonstration purposes.

## What's in this folder
| File | Use it for |
|---|---|
| `gravity-brand-reference.md` | The full brand reference: idea, language, logo rules, colour, type, tone, products, Arc, guardrails. Also a good knowledge source for the colleague agent "Navigator". |
| `gravity-tokens.css` | Web and Power Pages: CSS variables (dark default + `data-theme="light"`), gradients, type scale, spacing, motion, starter button/card classes. |
| `gravity-tokens.json` | The same tokens in W3C design-token format for apps and design tools. |
| `apply-sharepoint-themes.ps1` | Adds the **Gravity Dark** and **Gravity Light** themes to your tenant (SharePoint Online Management Shell). |
| `sharepoint-theme-gravity-dark.json` / `-light.json` | The raw SharePoint/Fluent theme palettes. |
| `powerbi-theme-gravity.json` | Power BI report theme (View > Themes > Browse for themes). |
| `powerapps-named-formulas.txt` | Paste into App > Formulas; use `GravityColor.*`, `GravityTheme.*`, `GravityFont.*`. |
| `copilot-studio-webchat-styleoptions.json` | Styling for embedding the Arc agent on a website. |
| `arc-agent-instructions.md` | Copilot Studio set-up for Arc: settings, starters, topics, paste-ready instructions, AI register entry. |
| `adaptive-card-arc-fraud-check.json` | "Was this you?" fraud-check Adaptive Card for agent or Teams demos. |

## Quick start
1. **SharePoint — "The Observatory" intranet**: connect with `Connect-SPOService`, run `apply-sharepoint-themes.ps1`, then Change the look > Theme > Gravity Dark. Header background: `gravity-brand-assets/patterns/gravity-grid-banner-2560x640.png`. Site logo: `gravity-brand-assets/logos/png/gravity-symbol-colour-1024.png`. Suggested navigation: Transmissions · Flight Rules · Star Charts · Crew · Launch Sequence · Mission Log.
2. **Power Apps** ("Mission Control", "Launch Sequence"): paste the named formulas, set screen Fill to `GravityTheme.Background`, upload the lockup PNG to Media.
3. **Copilot Studio**: create "Arc", paste section B of `arc-agent-instructions.md`, set the icon to `gravity-brand-assets/icons/arc-agent-icon-192.png`.
4. **Power Automate — "Flight Plans"**: FP-01 Switch-in welcome · FP-02 Fraud alert and card freeze · FP-03 Complaint triage (8-week clock) · FP-04 Soft Landing referral · FP-05 Mortgage rate-switch reminder.
5. **Power BI — "Proof" dashboards**: import `powerbi-theme-gravity.json`.
6. **Teams**: app icons `gravity-teams-color-192.png` and `gravity-teams-outline-32.png`.
7. **Websites / Power Pages**: link `gravity-tokens.css`; see the homepage concept in `gravity-website/`.

## Brand assets (in `gravity-brand-assets/`)
- `logos/svg` + `logos/png`: horizontal and stacked lockups (on dark, on light, white, black), the Singularity symbol (colour, glow, white, black), wordmark (white, black).
- `icons`: app icon (1024/512/180), favicon (SVG/32/64), Teams colour 192 + outline 32, Arc avatar (SVG/512) and agent icon (192).
- `patterns`: the Gravity Grid — 2560×640 banner, 1920×1080 (slides, Teams backgrounds), 1080 square.
- `cards`: Orbit, Event Horizon and Launchpad card faces (SVG + PNG).

## Golden rules
- Dark-first: Singularity Black backgrounds, Starlight text, light used sparingly "like a photon ring".
- Playful product name + plain descriptor, always (e.g. "Liftoff — easy-access saver").
- Never say "black hole" about money. Never use film titles, characters, quotes or stills.
- Body text on dark: Starlight / Moondust / Photon Cyan / Nebula Lilac. On light: Singularity Black / Slate / Violet 700.
- Before any real-world use: trade mark, Companies House, domain and FCA Register name checks.
