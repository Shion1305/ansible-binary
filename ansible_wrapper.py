#!/usr/bin/env python3
"""
Ansible wrapper script for standalone binary compilation.
This script serves as the entry point for the Nuitka-compiled Ansible binary.
"""

import sys
import os


def main():
    """Main entry point that delegates to ansible CLI."""
    try:
        # Get the base name of how we were called
        program_name = os.path.basename(sys.argv[0])

        # Map program names to (module, function) for Ansible CLIs.
        # This mirrors the console_scripts installed by ansible / ansible-core.
        entry_map = {
            'ansible': ('ansible.cli.adhoc', 'main'),
            'ansible-playbook': ('ansible.cli.playbook', 'main'),
            'ansible-galaxy': ('ansible.cli.galaxy', 'main'),
            'ansible-vault': ('ansible.cli.vault', 'main'),
            'ansible-console': ('ansible.cli.console', 'main'),
            'ansible-config': ('ansible.cli.config', 'main'),
            'ansible-doc': ('ansible.cli.doc', 'main'),
            'ansible-inventory': ('ansible.cli.inventory', 'main'),
            'ansible-pull': ('ansible.cli.pull', 'main'),
        }

        # Determine which entrypoint to use; default to "ansible" behavior.
        module_name, func_name = entry_map.get(
            program_name,
            ('ansible.cli.adhoc', 'main'),
        )

        # Import the module and resolve the entry function
        module = __import__(module_name, fromlist=[func_name])
        entry_func = getattr(module, func_name)

        # Emulate the console_script shims: normalize sys.argv[0]
        if sys.argv[0].endswith("-script.pyw"):
            sys.argv[0] = sys.argv[0][:-11]
        elif sys.argv[0].endswith(".exe"):
            sys.argv[0] = sys.argv[0][:-4]

        # Execute the real entrypoint, letting it handle sys.argv itself
        sys.exit(entry_func())

    except KeyboardInterrupt:
        print("\n\nUser interrupted execution", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
