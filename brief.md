**AI Daily IT Intelligence Brief — 2026-09-24**

🔴 **[Vendor / Critical] Check Point warns of hackers exploiting Security Gateway VPN RCE flaw**
Check Point confirms active exploitation of CVE-2026-85102, a pre‑authentication remote code execution vulnerability in its Security Gateway VPN certificate handling.
_Why it matters:_ The flaw allows unauthenticated attackers to execute code on VPN appliances.
_Suggested action:_ Apply the vendor’s patches and enforce multi‑factor authentication for VPN access.
[Source](https://www.bleepingcomputer.com/news/security/check-point-warns-of-hackers-exploiting-security-gateway-vpn-rce-flaw/)

🔴 **[Vendor / Critical] Hackers start exploiting critical WordPress flaw for code execution**
Threat actors are exploiting CVE-2026-87902 in WordPress to write files that execute shell commands when accessed.
_Why it matters:_ The vulnerability enables remote code execution on compromised sites.
_Suggested action:_ Patch WordPress installations immediately and monitor for suspicious file changes.
[Source](https://www.bleepingcomputer.com/news/security/hackers-start-exploiting-critical-wordpress-flaw-for-code-execution/)

🔴 **[Vendor / Critical] MikroTrick Chain Let Attackers Take Over MikroTik Routers Without a Password or SSH Key**
Two chained MikroTik RouterOS SSH vulnerabilities (CVE-2026-67279 and CVE-2026-86060) allow attackers to gain full admin control of exposed routers without authentication.
_Why it matters:_ Compromised routers can be used for network infiltration and traffic interception.
_Suggested action:_ Update RouterOS to the latest version and restrict SSH access.
[Source](https://thehackernews.com/2026/09/mikrotrick-chain-let-attackers-take.html)

🟠 **[Windows / High] Placeholder domain used in dev docs now serves ClickFix attacks**
A placeholder domain "third-party.com" used in documentation now hosts a fake Cloudflare verification page that attempts to trick Windows users into running PowerShell commands.
_Why it matters:_ It demonstrates how innocuous placeholder domains can be weaponized to compromise Windows systems.
_Suggested action:_ Block the domain and educate users about suspicious verification pages.
[Source](https://www.bleepingcomputer.com/news/security/placeholder-domain-used-in-dev-docs-now-serves-clickfix-attacks/)

🟠 **[Security / High] New RemControl Android banking malware targets users in Europe and Canada**
RemControl is a new Android malware-as-a-service platform that distributes banking trojans via malvertising that impersonates the TVTap IPTV app.
_Why it matters:_ It targets banking credentials of users in Europe and Canada.
_Suggested action:_ Update mobile security solutions and advise users to install apps only from trusted sources.
[Source](https://www.bleepingcomputer.com/news/security/new-remcontrol-android-banking-malware-targets-users-in-europe-and-canada/)

🟠 **[Vendor / High] Attackers Use Malicious Terraform Providers to Deliver Go Malware via HashiCorp Registry**
Researchers found Go‑based malware distributed through malicious Terraform providers and Go modules hosted on the HashiCorp Registry.
_Why it matters:_ It introduces a new supply‑chain attack vector for infrastructure‑as‑code tools.
_Suggested action:_ Verify provider authenticity and restrict registry usage to trusted sources.
[Source](https://thehackernews.com/2026/09/attackers-use-malicious-terraform.html)

🟠 **[Vendor / High] A Leaked GitLab Issue Email Address Lets Anyone Push Code and Run CI Jobs as You**
A leaked private email address used for filing GitLab issues can be abused to push code and trigger CI jobs under the victim’s identity.
_Why it matters:_ Attackers can gain code execution and repository control without authentication.
_Suggested action:_ Rotate the issue email address and restrict its usage.
[Source](https://thehackernews.com/2026/09/a-leaked-gitlab-issue-email-address.html)

🟠 **[Security / High] Malicious AI agents steal 600K credit cards, infect 100+ sites with skimmers**
A threat actor uses open‑source AI agent frameworks to compromise hundreds of e‑commerce sites, stealing over 600,000 credit cards and deploying skimmers.
_Why it matters:_ The scale of credential theft poses significant financial risk to consumers and merchants.
_Suggested action:_ Deploy web‑application firewalls and monitor for unauthorized AI agent activity.
[Source](https://www.bleepingcomputer.com/news/security/malicious-ai-agents-steal-600k-credit-cards-infect-100-plus-sites-with-skimmers/)

🟡 **[Security / Medium] InfraTrust report warns network management systems under attack**
The InfraTrust report highlights increasing attacks on network management systems, with several critical vulnerabilities being exploited shortly after disclosure.
_Why it matters:_ Compromised management systems can give attackers broad control over enterprise infrastructure.
_Suggested action:_ Prioritize patching of management software and monitor for exploitation attempts.
[Source](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-network-management-systems-under-attack/)

🔵 **[Microsoft 365 / Information] Reimagining the SOC for the agentic era in Microsoft Defender**
Microsoft announced ISOC in Microsoft Defender, a new foundation for agentic security integrating SIEM and threat protection.
_Why it matters:_ It signals a shift toward AI‑driven security operations.
_Suggested action:_ Review the new capabilities and plan integration into existing SOC workflows.
[Source](https://www.microsoft.com/en-us/security/blog/2026/09/23/reimagining-the-soc-for-the-agentic-era-in-microsoft-defender/)

_Advisory only — no automatic changes were made to any system._