# Ansible Binary

A standalone Ansible binary built with Nuitka. This allows you to distribute and run Ansible without requiring Python or dependencies to be installed on the target system.

## Prerequisites

- Python 3.10 or higher
- uv (for package management)
- C compiler (Xcode Command Line Tools on macOS)

## Building

1. Build the binary using uv:
```bash
uv run build.py
```

The standalone binary will be created in the `dist/` directory.

## Usage

After building, you can run the binary directly:
```bash
./dist/ansible --version
```

## Cleaning Build Artifacts

```bash
rm -rf *.build *.dist *.onefile-build dist/ build/
```

## Technical Details

- Uses Nuitka to compile Python code into a standalone executable
- Bundles core Ansible and essential dependencies
- Creates a single-file executable for easy distribution
- Binary size: ~50-100MB (includes Python interpreter and core dependencies)
- Note: Ansible collections are not included in the binary. Install them separately if needed.

## Platform Support

Currently builds for macOS. For Linux or Windows binaries, build on the respective platform.
