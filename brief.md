**AI Daily IT Intelligence Brief — 2026-10-23**

🔴 **[Security / Critical] Critical Flaw in Python’s Popular Pillow Image Library Allows Code Execution via a Crafted Image**
The Pillow library (CVE-2026-112900) can execute OS commands when processing crafted EPS images because it passes the filename to Ghostscript without validation.
_Why it matters:_ Exploiting the flaw can lead to remote code execution on servers using Pillow.
_Suggested action:_ Apply any available patches or mitigate by validating image inputs.
[Source](https://thehackernews.com/2026/10/critical-flaw-in-pythons-popular-pillow.html)

🔴 **[Security / Critical] Researchers Demonstrate Node2Shell RCE Exploit on Node.js Build Using Crafted Brotli Data**
Researchers showed that crafted Brotli data can trigger code execution in the official Node.js 24.22.0 Linux arm64 image via the built‑in Brotli decoder (CVE-2026-111497).
_Why it matters:_ The vulnerability affects default Node.js builds without custom modifications.
_Suggested action:_ Update Node.js to a version that addresses CVE-2026-111497.
[Source](https://thehackernews.com/2026/10/researchers-demonstrate-node2shell-rce.html)

🟠 **[Security / High] Russian-Linked Hackers Used New Mesh Network Backdoor in Destructive Ukraine Attack**
The Sandworm group and another actor carried out a destructive wiping attack on a Ukrainian logistics company using the UAC-0099 (Earth Sirrush) backdoor after a spear‑phishing email on July 16, 2025.
_Why it matters:_ It demonstrates evolving destructive capabilities targeting critical infrastructure.
_Suggested action:_ Monitor for indicators of the UAC-0099 backdoor and strengthen email defenses.
[Source](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html)

🟠 **[Security / High] Critical x402 SDK Flaw Could Let Malicious APIs Drain AI Agents’ Token Balances**
The x402 SDK default client allowed malicious APIs to drain an AI agent’s token balance by signing full‑balance payments, affecting agents that auto‑sign payments.
_Why it matters:_ It could result in unauthorized depletion of token funds for AI agents.
_Suggested action:_ Ensure spending limits are configured and update to SDK releases after August 18.
[Source](https://thehackernews.com/2026/10/critical-x402-sdk-flaw-could-let.html)

🟠 **[Security / High] PHP2Shell Exploit Attempts Hit Millions as Attackers Try to Deploy Mirai Malware**
Threat actors attempted to exploit the newly disclosed PHP2Shell vulnerabilities (CVE-2026-109618, CVE-2026-109619) to install a Mirai‑like botnet called Potassium, but the attempts were largely unsuccessful.
_Why it matters:_ It highlights ongoing exploitation attempts of high‑severity PHP flaws.
_Suggested action:_ Verify that systems are patched against PHP2Shell vulnerabilities.
[Source](https://thehackernews.com/2026/10/php2shell-exploit-attempts-hit-millions.html)

🟠 **[Vendor / High] Railway warns devs to rotate secrets after potential breach**
Cloud platform Railway issued an urgent warning after detecting suspicious activity on systems that store customer environment variables, urging users to rotate secrets.
_Why it matters:_ Potential exposure of secret keys could compromise deployed applications.
_Suggested action:_ Rotate all environment variable secrets immediately.
[Source](https://www.bleepingcomputer.com/news/security/railway-warns-devs-to-rotate-secrets-after-potential-breach/)

🟠 **[Vendor / High] Capcom confirms data breach affecting 11.7 million accounts**
Capcom confirmed a breach of its CAPCOM ID service, exposing more than 11.7 million customer email addresses and associated information.
_Why it matters:_ The large‑scale exposure puts millions at risk of phishing and fraud.
_Suggested action:_ Monitor for phishing attempts and consider password changes for affected accounts.
[Source](https://www.bleepingcomputer.com/news/security/capcom-confirms-data-breach-affecting-117-million-accounts/)

🟠 **[Vendor / High] LiteLLM release pipeline hacked to distribute info-stealer malware**
Hackers compromised the LiteLLM project's PyPI package and published malicious Docker images that steal credentials, secrets, and environment variables.
_Why it matters:_ Supply‑chain compromise can spread malware to downstream users.
_Suggested action:_ Verify package integrity and replace any compromised images.
[Source](https://www.bleepingcomputer.com/news/security/litellm-release-pipeline-hacked-to-distribute-info-stealer-malware/)

🟡 **[Security / Medium] URGENT - PHP Warns of Another Unpatched RCE Two Days After Emergency PHP2Shell Patches**
PHP warned of a new code execution issue (CVE-2026-115560) affecting web applications with an unusual configuration, but no emergency fix is planned, only a recommendation to turn off a feature.
_Why it matters:_ The issue could allow attackers to run code on vulnerable servers.
_Suggested action:_ Review and disable the mentioned feature in affected PHP configurations.
[Source](https://thehackernews.com/2026/10/urgent-php-warns-of-another-unpatched.html)

🟡 **[Security / Medium] The AI Agent Nobody Owns: Watch Expert Webinar On Your Newest Insider Threat**
An article warns that unsupervised AI agents can store API keys and passwords, acting as insider threats without proper oversight.
_Why it matters:_ Unmanaged AI agents can become hidden vectors for data exfiltration.
_Suggested action:_ Implement governance and access controls for AI agents.
[Source](https://thehackernews.com/2026/10/the-ai-agent-nobody-owns-watch-expert.html)

_Advisory only — no automatic changes were made to any system._