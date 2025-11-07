import re

# ======================================================================
#  CLI FLAG UTILITIES — For use in Ansible Jinja2 templates
#
#  These helpers make it easy to safely add, remove, or check command-line
#  flags (e.g., --force, --ecc) when building acme.sh commands dynamically.
#
#  Usage examples are provided below each filter definition.
# ======================================================================


# ----------------------------------------------------------------------
# 1. has_flag()
# ----------------------------------------------------------------------
def has_flag(extra_flags, flag_names):
    """
    Check if one or more flags appear as standalone tokens
    in the provided extra_flags string.

    Example Jinja2 usage:
      {{ item.acme_sh_extra_flags | has_flag('--ecc') }}
      {{ '--debug --force' | has_flag(['--debug', '--verbose']) }}

    Returns: True if ANY flag is present, else False
    """
    if not extra_flags or not flag_names:
        return False

    if isinstance(flag_names, str):
        flag_names = [flag_names]

    for flag in flag_names:
        escaped_flag = re.escape(flag)
        pattern = rf'(^|\s){escaped_flag}(\s|$)'
        if re.search(pattern, extra_flags):
            return True
    return False


# ----------------------------------------------------------------------
# 2. add_flag_if_missing()
# ----------------------------------------------------------------------
def add_flag_if_missing(command, flag):
    """
    Append a flag to a command string only if it's not already present.

    Example Jinja2 usage:
      {{ 'acme.sh --issue -d example.com' | add_flag_if_missing('--force') }}
      → acme.sh --issue -d example.com --force
    """
    if not command or not flag:
        return command or ''
    escaped_flag = re.escape(flag)
    pattern = rf'(^|\s){escaped_flag}(\s|$)'
    if not re.search(pattern, command):
        return f"{command.strip()} {flag}"
    return command.strip()


# ----------------------------------------------------------------------
# 3. ensure_flags_present()
# ----------------------------------------------------------------------
def ensure_flags_present(command, flags):
    """
    Ensures that all specified flags are present in a command string.
    Adds any missing ones without duplication.

    Example Jinja2 usage:
      {{ 'acme.sh --issue -d example.com --ecc' |
          ensure_flags_present(['--force', '--debug']) }}
      → acme.sh --issue -d example.com --ecc --force --debug
    """
    if not command:
        command = ''
    if not flags:
        return command.strip()

    for flag in flags:
        escaped_flag = re.escape(flag)
        pattern = rf'(^|\s){escaped_flag}(\s|$)'
        if not re.search(pattern, command):
            command = f"{command.strip()} {flag}"
    return command.strip()


# ----------------------------------------------------------------------
# 4. remove_flag()
# ----------------------------------------------------------------------
def remove_flag(command, flags):
    """
    Removes one or more flags from a command string.

    Example Jinja2 usage:
      {{ 'acme.sh --issue -d example.com --staging --debug'
         | remove_flag(['--staging', '--debug']) }}
      → acme.sh --issue -d example.com

      {{ 'acme.sh --renew --force' | remove_flag('--force') }}
      → acme.sh --renew
    """
    if not command or not flags:
        return command or ''
    if isinstance(flags, str):
        flags = [flags]

    for flag in flags:
        escaped_flag = re.escape(flag)
        pattern = rf'(^|\s){escaped_flag}(\s|$)'
        command = re.sub(pattern, ' ', command)
    # Normalize spacing
    return re.sub(r'\s+', ' ', command).strip()


# ----------------------------------------------------------------------
#  Filter Registration
# ----------------------------------------------------------------------
class FilterModule(object):
    ''' Custom Jinja2 filters for CLI flag manipulation (ACME utilities) '''
    def filters(self):
        return {
            'has_flag': has_flag,
            'add_flag_if_missing': add_flag_if_missing,
            'ensure_flags_present': ensure_flags_present,
            'remove_flag': remove_flag,
        }

