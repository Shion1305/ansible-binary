#!/usr/bin/env python3
"""
Build script for creating a standalone Ansible binary using Nuitka.
"""

import os
import sys
import subprocess
import shutil


def check_requirements():
    """Check if required tools are available."""
    try:
        import nuitka
        from nuitka.Version import getNuitkaVersion
        print(f"✓ Nuitka found: {getNuitkaVersion()}")
    except ImportError:
        print("✗ Nuitka not found. Please install requirements first.")
        print("  Run: uv pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        import ansible
        print(f"✓ Ansible found: {ansible.__version__}")
    except ImportError:
        print("✗ Ansible not found. Please install requirements first.")
        print("  Run: uv pip install -r requirements.txt")
        sys.exit(1)


def build_binary():
    """Build the standalone binary using Nuitka."""
    print("\n" + "="*60)
    print("Building Ansible standalone binary with Nuitka")
    print("="*60 + "\n")
    
    # Ensure dist directory exists
    os.makedirs("dist", exist_ok=True)
    
    # Get number of CPU cores
    try:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
    except:
        cpu_count = 4  # fallback
    
    print(f"Using {cpu_count} CPU cores for parallel compilation")
    
    # Nuitka command with options
    nuitka_cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--output-dir=dist",
        "--output-filename=ansible",
        
        # Include only essential ansible packages (not all collections)
        "--include-package=ansible",
        # Note: Removed ansible_collections to reduce compilation time
        # Users will need to install collections separately if needed
        
        # Include ansible data files (config, templates, etc.)
        "--include-package-data=ansible",
        
        # Include commonly used packages
        "--include-package=jinja2",
        "--include-package=yaml",
        "--include-package=packaging",
        "--include-package=resolvelib",
        
        # Performance optimizations
        f"--jobs={cpu_count}",  # Parallel compilation
        "--lto=yes",  # Link-time optimization
        "--assume-yes-for-downloads",
        "--show-progress",
        "--show-memory",
        
        # Disable some optimizations that are slow
        "--python-flag=no_docstrings",  # Remove docstrings
        
        # Input file
        "ansible_wrapper.py"
    ]
    
    print("Running Nuitka compilation...")
    print(f"Command: {' '.join(nuitka_cmd)}\n")
    
    try:
        result = subprocess.run(nuitka_cmd, check=True)
        print("\n" + "="*60)
        print("✓ Build completed successfully!")
        print("="*60)
        print(f"\nBinary location: dist/ansible")
        print("\nTo test the binary, run:")
        print("  ./dist/ansible --version")
        return 0
    except subprocess.CalledProcessError as e:
        print("\n" + "="*60)
        print("✗ Build failed!")
        print("="*60)
        return 1
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user")
        return 130


def main():
    """Main build function."""
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Not running in a virtual environment")
        print("It's recommended to run this in a virtual environment")
        response = input("Continue anyway? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            return 1
    
    check_requirements()
    return build_binary()


if __name__ == "__main__":
    sys.exit(main())
