#!/usr/bin/env python3
"""html-style-roulette · 随机抽取一个浅色 HTML 报告版式。

用法:
    python3 pick_style.py            # 抽一个版式，打印 JSON
    python3 pick_style.py --history  # 只看最近使用记录

行为:
  1. 读同目录 styles.json，只取浅色版式（excluded_dark 永不入选）
  2. 排除「最近连续使用」的版式（usage.log 中最近一条），避免连续两次同款
  3. random.choice 抽取（真随机，非顺序轮换）
  4. 追加写入 usage.log（时间戳 + 版式 id），供下次排除与回顾
"""
import json
import random
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
STYLES = HERE / "styles.json"
LOG = HERE / "usage.log"


def main() -> None:
    data = json.loads(STYLES.read_text(encoding="utf-8"))
    styles = data["styles"]

    # 最近使用记录：最后一行为最近一次
    recent: list[str] = []
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    recent.append(parts[1])

    last = recent[-1] if recent else None
    pool = [s for s in styles if s["id"] != last]

    if not pool:  # 理论上不会发生（版式数 > 1）
        pool = styles

    pick = random.choice(pool)

    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} {pick['id']}\n")

    print(json.dumps({
        "id": pick["id"],
        "name": pick["name"],
        "tokens": pick["tokens"],
        "excluded_last": last,
        "times_used": recent.count(pick["id"]) + 1,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--history" in sys.argv:
        print(LOG.read_text(encoding="utf-8") if LOG.exists() else "(空)")
    else:
        main()
