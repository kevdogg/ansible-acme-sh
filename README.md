# 🧩 ansible-acme-sh

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ansible](https://img.shields.io/badge/Ansible-Role-blue?logo=ansible)](https://github.com/kevdogg/ansible-acme-sh)

---

### 🚀 Overview

**ansible-acme-sh** is an [Ansible](https://www.ansible.com) role for managing SSL/TLS certificates using [acme.sh](https://github.com/acmesh-official/acme.sh).  
It automates the complete lifecycle of certificate management — **plan, issue, renew, deploy, remove, and teardown** — using DNS-based challenges with optional systemd integration.

> **Repository:** [github.com/kevdogg/ansible-acme-sh](https://github.com/kevdogg/ansible-acme-sh)

---

## ✨ Key Features

- 🔐 Fully automated issuance and renewal of Let's Encrypt certificates via **acme.sh**
- 🧠 Intelligent preflight “plan” mode — preview changes before applying
- ⚙️ Optional **systemd service + timer** for automatic renewals
- 🧹 Complete uninstall and cleanup routines (`remove_all`, `teardown`)
- 💬 Built-in **notification hooks** (Mailgun, Slack, etc.)
- 🧪 Developer filters for CLI flag manipulation (`has_flag`, `remove_flag`, etc.)
- 🧾 Final summary reports and optional plan vs. actual comparison
- 🧰 Safe, idempotent, and per-domain configurable

---

## 🖥️ Supported Platforms

| OS Family | Versions |
|------------|-----------|
| Ubuntu     | 20.04 – 24.04 |
| Debian     | 10+ |
| Fedora / RHEL | 9+ |
| Alpine / BSD | latest |
| macOS      | supported (manual timer setup) |

---

## ⚙️ Installation

### From GitHub
```bash
ansible-galaxy install git+https://github.com/kevdogg/ansible-acme-sh.git
From Local Development (recommended)
In your ansible.cfg:

ini
Copy code
roles_path = ~/git/roles:/etc/ansible/roles
Clone locally:

bash
Copy code
git clone https://github.com/kevdogg/ansible-acme-sh.git ~/git/roles/kevdogg.acme_sh
🧭 Example Playbook
yaml
Copy code
---
- name: Configure and manage certificates
  hosts: all
  become: true

  roles:
    - role: kevdogg.acme_sh
      tags: ["acme"]
Example host_vars/example.com.yml:

yaml
Copy code
acme_sh_domains:
  - domains: ["example.com", "www.example.com"]
    staging: true
    acme_sh_pkcs12_password: "pass"
    install_cert_reloadcmd: "systemctl reload nginx.service"

  - domains: ["api.example.com"]
    remove: true
🧩 Key Variables (Summary)
Variable	Default	Description
acme_sh_become_user	{{ ansible_become_user }}	System user that runs acme.sh
acme_sh_default_git_url	https://github.com/acmesh-official/acme.sh.git	acme.sh repository
acme_sh_default_copy_certs_to_path	/etc/ssl/letsencrypt	Target cert storage directory
acme_sh_enable_notify	true	Enable acme.sh notifications
acme_sh_default_dns_provider	dns_cf	DNS API provider (Cloudflare default)
acme_sh_default_dns_provider_api_keys	{ CF_Token, CF_Zone_ID, CF_Email }	API credentials
acme_sh_default_server	letsencrypt	Default CA authority
acme_sh_uninstall	false	Remove everything (systemd, certs, repo)
acme_sh_default_extra_flags	--ecc	Default cert type (ECC)

🗂️ See defaults/main.yml for all configuration options.

🔄 Role Execution Flow (ASCII Diagram)
pgsql
Copy code
┌───────────────────────────────────────────────────────────────┐
│                        Preflight Phase                        │
│---------------------------------------------------------------│
│  acme-plan.yml → Build domain plan                            │
│  acme-plan-summary-compact.yml → Display planned actions       │
└──────────────┬────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                   Installation Phase                          │
│---------------------------------------------------------------│
│  acme-install-acme-sh.yml → Install acme.sh, setup systemd     │
│  acme-resolve-acme-paths.yml → Resolve binaries and paths      │
└──────────────┬────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                  Workflow Phase (Default)                     │
│---------------------------------------------------------------│
│  acme-domain-workflow.yml → Issue / renew / deploy certs      │
│  [debug-tag tasks show live progress per domain]              │
└──────────────┬────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                     Removal Phase                             │
│---------------------------------------------------------------│
│  acme-domain-remove.yml → Remove selected domains             │
│  acme-remove-all.yml → Full teardown (when uninstall enabled) │
└──────────────┬────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                     Postflight Phase                          │
│---------------------------------------------------------------│
│  acme-summary-compact.yml → Show final results summary         │
│  Includes plan vs actual deltas when enabled                  │
└──────────────┬────────────────────────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────────────┐
│                    Developer / Debug Mode                     │
│---------------------------------------------------------------│
│  test-filters.yml → Validate CLI flag filter plugins           │
│  (Run manually with `--tags test-filters`)                    │
└───────────────────────────────────────────────────────────────┘
🧭 Role Execution Flow (Mermaid Diagram)
mermaid
Copy code
flowchart TD
  A[🧩 Preflight Phase<br/>acme-plan.yml / summary] --> B[⚙️ Installation Phase<br/>acme-install-acme-sh.yml]
  B --> C[🔁 Workflow Phase<br/>acme-domain-workflow.yml]
  C --> D[🗑️ Removal Phase<br/>acme-domain-remove.yml]
  D --> E[🧹 Full Teardown<br/>acme-remove-all.yml]
  E --> F[📋 Postflight Summary<br/>acme-summary-compact.yml]
  F --> G[🧪 Developer / Filter Test<br/>test-filters.yml]

  style A fill:#E3F2FD,stroke:#1E88E5,stroke-width:2px
  style B fill:#E8F5E9,stroke:#43A047,stroke-width:2px
  style C fill:#FFF8E1,stroke:#FDD835,stroke-width:2px
  style D fill:#FFEBEE,stroke:#E53935,stroke-width:2px
  style E fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
  style F fill:#F1F8E9,stroke:#7CB342,stroke-width:2px
  style G fill:#ECEFF1,stroke:#546E7A,stroke-width:2px
🏷️ Tag Reference
Tag	Executes	Description
plan	acme-plan.yml, acme-plan-summary-compact.yml	Preflight plan + display
install_acme.sh	acme-install-acme-sh.yml	Install and setup acme.sh
workflow	acme-domain-workflow.yml	Issue, renew, and deploy certs
remove_all	acme-remove-all.yml	Full teardown of certs and systemd
summary	acme-summary-compact.yml	Final report and delta analysis
debug	test-filters.yml, debug-acme-scoreboard.yml	Developer tests and extra logging
notify	Internal in acme-install-acme-sh.yml	Configure notifications
teardown	Alias for remove_all	Complete uninstall and cleanup

🧪 Developer Tools
Run internal filter verification directly:

bash
Copy code
ansible-playbook roles/kevdogg.acme_sh/tasks/test-filters.yml -vvv
Or from a playbook:

bash
Copy code
ansible-playbook playbook.yml --tags test-filters -vvv
Common debug options:

bash
Copy code
# Full execution
ansible-playbook playbook.yml

# Skip debug tasks
ansible-playbook playbook.yml --skip-tags debug

# Only plan and summary
ansible-playbook playbook.yml --tags plan,summary
🧰 Example Developer Setup
bash
Copy code
git clone https://github.com/kevdogg/ansible-acme-sh.git ~/git/roles/kevdogg.acme_sh
cd ~/ansible/letsencrypt
ansible-playbook playbook.yml --limit ns3.gohilton.com
🧾 License
Licensed under the MIT License — see LICENSE.

👨‍💻 Maintainer & Version Info
Field	Value
Maintainer	KevDog
Version	2025.11.09
Compatible with	acme.sh ≥ 3.0.8
Repository	github.com/kevdogg/ansible-acme-sh
Last Updated	🕓 2025-11-09
