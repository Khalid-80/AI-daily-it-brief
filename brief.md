**AI Daily IT Intelligence Brief — 2026-10-26**

🔴 **[Security / Critical] Two Critical Wasmtime Flaws Could Let Malicious WebAssembly Modules Escape Sandboxes**
Two critical flaws in the Wasmtime WebAssembly runtime could allow a malicious module to break out of its sandbox, and fixed versions have been released.
_Why it matters:_ Sandbox escape could let attackers execute code on vulnerable hosts.
_Suggested action:_ Update Wasmtime to the patched version immediately.
[Source](https://thehackernews.com/2026/10/two-critical-wasmtime-flaws-could-let.html)

🔴 **[Security / Critical] PHP2Shell security flaws now sucessfully exploited in the wild**
Two critical RCE vulnerabilities (CVE-2026-109618 and CVE-2026-109619) known as PHP2Shell are being actively exploited in the wild.
_Why it matters:_ Active exploitation puts vulnerable PHP applications at immediate risk of compromise.
_Suggested action:_ Patch affected PHP installations and monitor for exploitation attempts.
[Source](https://www.bleepingcomputer.com/news/security/php2shell-security-flaws-now-sucessfully-exploited-in-the-wild/)

🟠 **[Security / High] uCreator Android Spyware Can Steal Telegram 2FA Passwords and Clone WeChat Accounts**
The uCreator Android spyware kit hides malicious code in tampered Telegram and WeChat apps to steal 2FA passwords and clone accounts.
_Why it matters:_ It enables credential theft and unauthorized access to popular messaging platforms.
_Suggested action:_ Block and remove any tampered app installations and monitor for compromised accounts.
[Source](https://thehackernews.com/2026/10/ucreator-android-spyware-can-steal.html)

🟠 **[Microsoft 365 / High] Microsoft 365 Token-Replay Attacks Compromise 97 Accounts at 79 Organizations**
A campaign used adversary‑in‑the‑middle token replay to hijack Microsoft 365 sign‑in sessions, compromising 97 accounts across 79 organizations.
_Why it matters:_ Token replay can give attackers persistent access to corporate email and data.
_Suggested action:_ Enforce MFA, monitor token usage, and rotate compromised tokens.
[Source](https://thehackernews.com/2026/10/microsoft-365-token-replay-attacks.html)

🟠 **[Vendor / High] Gheist Uses Stolen GitHub Tokens to Steal Private Repository Secrets via Actions Logs**
The Gheist campaign steals GitHub tokens, plants workflows that log repository secrets, then extracts and deletes the logs.
_Why it matters:_ Exfiltrated secrets can lead to further compromise of private code and infrastructure.
_Suggested action:_ Revoke compromised tokens, rotate secrets, and audit GitHub Actions for unauthorized workflows.
[Source](https://thehackernews.com/2026/10/gheist-uses-stolen-github-tokens-to.html)

🟠 **[Security / High] Unpatched Tailscale SSH Flaws Could Let a Hacked Device Reach Root on Other Servers**
Two flaws in Tailscale SSH allow a compromised device with port‑forwarding enabled to gain root access on reachable servers within the network.
_Why it matters:_ Lateral movement could lead to full network compromise.
_Suggested action:_ Apply the available patches and disable unnecessary port forwarding.
[Source](https://thehackernews.com/2026/10/unpatched-tailscale-ssh-flaws-could-let.html)

🟠 **[Security / High] PHP2Shell Exploitation Attempts Continue Amid Suspected N. Korea Global Scanning Activity**
Palo Alto Networks reports ongoing exploitation attempts of PHP2Shell flaws targeting a European government agency, amid broader scanning activity.
_Why it matters:_ Continued attacks indicate persistent threat actors targeting vulnerable PHP sites.
_Suggested action:_ Ensure all PHP systems are patched and increase monitoring for exploitation signatures.
[Source](https://thehackernews.com/2026/10/php2shell-exploitation-hits-government.html)

🟡 **[Security / Medium] Malicious File in Downloads Folder Tries to Trick AI Coding Agent Into Installing Malware**
A malicious instruction file in a developer's Downloads folder attempted to persuade an AI coding agent to install a known‑malicious npm package, which was blocked by security monitoring.
_Why it matters:_ AI‑assisted development tools can be leveraged to deliver malware silently.
_Suggested action:_ Implement file integrity monitoring and restrict AI agent actions on untrusted inputs.
[Source](https://thehackernews.com/2026/10/malicious-file-in-downloads-folder.html)

🔵 **[Security / Information] Between alerts: What Attackers Do in the Spaces Ordinary Detection Misses**
The article discusses how SOCs struggle with alert overload and the need for network detection to connect alerts into a coherent intrusion timeline.
_Why it matters:_ The thin description requires human review to assess actionable insights.
_Suggested action:_ Have analysts review the detection workflow for gaps.
[Source](https://thehackernews.com/2026/10/between-alerts-what-attackers-do-in.html)

🔵 **[Vendor / Information] Kali Linux 2026.3 released with 6 new tools, desktop updates**
Kali Linux 2026.3 adds six new hacking tools, desktop environment improvements, and refreshed build scripts.
_Why it matters:_ New tools may affect security testing and toolchains.
_Suggested action:_ Review the new tools for relevance to your environment.
[Source](https://www.bleepingcomputer.com/news/linux/kali-linux-20263-released-with-6-new-tools-desktop-updates/)

_Advisory only — no automatic changes were made to any system._