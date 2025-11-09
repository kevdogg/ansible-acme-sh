# 🧾 CHANGELOG

All notable changes to **ansible-acme-sh** are documented here.

---

## [2025.11.09] – Major Modernization & Refactor

### ✨ Added
- Comprehensive **README.md** rewrite with diagrams and tag reference.
- Introduced **filter plugin test suite** (`test-filters.yml`).
- Added detailed **summary and teardown phases** with explicit tagging.
- New **developer debug mode** supporting `--tags test-filters`.
- Added **full Mermaid + ASCII execution flow diagrams** to docs.
- Added **systemd timer/service integration** for auto-renewal.

### 🔧 Changed
- Refactored task structure for improved readability and modular design.
- Replaced deprecated or legacy logic with Ansible-safe idioms.
- Enhanced variable defaults and fallback handling.
- Simplified preflight logic and plan summaries.
- Revised tag hierarchy: now includes `plan`, `workflow`, `remove_all`, `debug`, and `summary`.

### 🧹 Removed
- Obsolete teardown subtasks: `remove-acme-certificate-files-and-directory.yml`.
- Removed legacy redundant cleanup files in favor of unified `acme-remove-all.yml`.

### 🧪 Developer Notes
- Filter plugin verification supports both standalone and role-integrated execution.
- Internal filters now validated automatically at verbosity ≥ 3.

---

## [2025.10.20] – Tag Consolidation & Preflight Enhancements

### ✨ Added
- New tag inheritance scheme using `apply:` for `include_tasks`.
- Added `plan` phase with compact preflight summary task.
- Introduced dynamic summary scoreboard using `set_fact`.

### 🔧 Changed
- Improved default handling for `acme_sh_domains` lists.
- Centralized path resolution logic in `acme-resolve-acme-paths.yml`.
- Updated uninstall logic for safety and idempotency.

### 🧹 Removed
- Redundant duplicate set_fact declarations.
- Legacy debug prints replaced with `ansible.builtin.debug` loops.

---

## [2025.09.30] – Modular Role Bootstrap

### ✨ Added
- Initial modular breakdown into:
  - `acme-plan.yml`
  - `acme-install-acme-sh.yml`
  - `acme-domain-workflow.yml`
  - `acme-domain-remove.yml`
  - `acme-remove-all.yml`
  - `acme-summary-compact.yml`

### 🔧 Changed
- All task names normalized for readability and consistency.
- Simplified conditions for domain removal and uninstall phases.
- Added support for macOS and BSD environments.

### 🧹 Removed
- Flat monolithic structure replaced by modular includes.

---

## [2025.09.01] – Initial Role Import

### ✨ Added
- First stable import of ansible-acme-sh.
- Support for issuing, renewing, and removing certificates using acme.sh.
- Support for DNS-based challenges with configurable providers.
- Initial notification system scaffold.
- Default paths and dependency checks.
