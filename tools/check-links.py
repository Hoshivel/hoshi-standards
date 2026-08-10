#!/usr/bin/env python3
"""檢查 Markdown 裡的相對連結是否指得到東西。

一條指向不存在檔案的相對連結，在 GitHub 上會安靜地 404，而 diff 上看不出來——
這正是需要一個會失敗的檢查的那一類問題。

用法：
    tools/check-links.py            # 從倉庫根跑
    tools/check-links.py --root docs

只用標準庫。

> **註**：這支腳本原本是寫在 workflow 裡的一段 shell。那一版有兩個問題：
> `grep` 在一份**沒有任何連結**的文件上回傳 1，配上 `pipefail` 會讓整支 CI
> 紅掉——而沒有連結的文件完全正常；另外它把 python 用巢狀 heredoc 塞進
> YAML 的區塊純量裡，縮排過的結束符不會結束 heredoc。
> **兩個問題都只有真的跑過才會發現**，所以它現在是一支跑得起來的腳本。
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

LINK = re.compile(r"\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def broken_links(root: pathlib.Path) -> list[str]:
    broken: list[str] = []
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts:
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for target in LINK.findall(text):
            if target.startswith(SKIP_PREFIXES):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            if not (md.parent / path).exists():
                broken.append(f"{md}: {target}")
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description="檢查 Markdown 的相對連結")
    parser.add_argument("--root", default=".", help="要掃描的目錄（預設為當前目錄）")
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    if not root.is_dir():
        print(f"找不到目錄 {root}。")
        return 1

    broken = broken_links(root)
    for b in broken:
        print(f"::error::連結指不到 {b}")
    print(f"檢查完畢，{len(broken)} 條壞連結。")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
