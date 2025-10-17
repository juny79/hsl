#!/usr/bin/env python3
"""Generate a dated checklist markdown file from a template."""
import sys, pathlib, datetime, shutil

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_checklist_md.py <TEMPLATE_MD> <OUT_DIR>")
        sys.exit(2)
    template = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    target = out_dir / f"checklist-{today}.md"
    shutil.copy(template, target)
    print(f"Generated: {target}")

if __name__ == '__main__':
    main()