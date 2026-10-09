# =====================================================================
# GRAVITY — SharePoint Online themes (light + dark)
# Requires: SharePoint Online Management Shell, SharePoint admin rights.
#   Install-Module -Name Microsoft.Online.SharePoint.PowerShell
#   Connect-SPOService -Url https://<your-tenant>-admin.sharepoint.com
# Then:  .\apply-sharepoint-themes.ps1
# Apply on a site: Settings (gear) > Change the look > Theme > "Gravity Dark" or "Gravity Light".
# Gravity is a fictional concept brand for demonstration purposes.
# =====================================================================

$gravityLight = @{
    "themePrimary" = "#5B3FE0";
    "themeLighterAlt" = "#F8F7FE";
    "themeLighter" = "#E5E0FA";
    "themeLight" = "#CEC5F6";
    "themeTertiary" = "#9D8CEC";
    "themeSecondary" = "#6F56E4";
    "themeDarkAlt" = "#5239CA";
    "themeDark" = "#4530AA";
    "themeDarker" = "#33237D";
    "neutralLighterAlt" = "#F8F8F8";
    "neutralLighter" = "#F4F4F5";
    "neutralLight" = "#EAEBEB";
    "neutralQuaternaryAlt" = "#E0E0E0";
    "neutralQuaternary" = "#D3D3D4";
    "neutralTertiaryAlt" = "#C3C3C5";
    "neutralTertiary" = "#A5A5A7";
    "neutralSecondary" = "#646568";
    "neutralPrimaryAlt" = "#37383C";
    "neutralPrimary" = "#05060B";
    "neutralDark" = "#040408";
    "black" = "#000000";
    "white" = "#FFFFFF";
}

$gravityDark = @{
    "themePrimary" = "#7B61FF";
    "themeLighterAlt" = "#0C0B1A";
    "themeLighter" = "#181532";
    "themeLight" = "#282154";
    "themeTertiary" = "#493B99";
    "themeSecondary" = "#6D56E2";
    "themeDarkAlt" = "#8871FF";
    "themeDark" = "#9B87FF";
    "themeDarker" = "#B5A7FF";
    "neutralLighterAlt" = "#0C0D12";
    "neutralLighter" = "#111216";
    "neutralLight" = "#1B1B1F";
    "neutralQuaternaryAlt" = "#222226";
    "neutralQuaternary" = "#2B2C2F";
    "neutralTertiaryAlt" = "#3F3F41";
    "neutralTertiary" = "#717070";
    "neutralSecondary" = "#ADABA8";
    "neutralPrimaryAlt" = "#D1CFCA";
    "neutralPrimary" = "#F5F2EC";
    "neutralDark" = "#F9F7F4";
    "black" = "#FFFFFF";
    "white" = "#05060B";
}

Add-SPOTheme -Identity "Gravity Light" -Palette $gravityLight -IsInverted $false -Overwrite
Add-SPOTheme -Identity "Gravity Dark"  -Palette $gravityDark  -IsInverted $true  -Overwrite

# Optional: hide the default themes so sites only see the brand themes
# Set-SPOHideDefaultThemes $true

Write-Host "Gravity themes added. Recommended site setup for 'The Observatory':" -ForegroundColor Cyan
Write-Host " - Header: Extended layout, background image patterns/gravity-grid-banner-2560x640.png"
Write-Host " - Site logo: logos/png/gravity-symbol-colour-1024.png (or icons/gravity-app-icon-512.png)"
Write-Host " - Navigation: Transmissions | Flight Rules | Star Charts | Crew | Launch Sequence | Mission Log"
