#!/usr/bin/env python3
"""Package only distributable source; no runtime state, private files or caches."""
from pathlib import Path
import zipfile

root=Path(__file__).resolve().parents[1]
source=root/'plugin'
out=root/'dist'/'crossborder-purchase-0.1.0.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(source.rglob('*')):
        rel=path.relative_to(source)
        if not path.is_file() or path.is_symlink():continue
        if any(part in ('private','__pycache__','.git') for part in rel.parts):continue
        if path.suffix not in ('.md','.py','.json'):continue
        archive.write(path,Path('crossborder-purchase')/rel)
print(out)
