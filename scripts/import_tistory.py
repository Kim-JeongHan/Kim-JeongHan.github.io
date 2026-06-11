#!/usr/bin/env python3
"""Compatibility wrapper for the Tistory importer."""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).with_name("blog") / "import_tistory.py"), run_name="__main__")
