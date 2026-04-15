#!/usr/bin/env python3
"""
PRD Reviewer Agent 一键部署脚本

将核心评审技能文件部署到各平台的标准目录。

用法:
    python3 deploy.py [平台]

支持的平台:
    all          - 部署到所有平台（默认）
    claude-code  - 部署到 Claude Code
    trae         - 部署到 TRAE
    openclaw     - 部署到 OpenClaw
    hermes       - 部署到 Hermes Agent

示例:
    python3 deploy.py all
    python3 deploy.py claude-code
"""

import os
import shutil
import sys
from pathlib import Path


# 获取脚本所在目录（项目根目录）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "prd-reviewer"

# 核心文件路径
CORE_SKILL = PROJECT_ROOT / "core" / "SKILL.md"
REFERENCES_DIR = PROJECT_ROOT / "references"

# 平台部署目标
PLATFORMS = {
    "claude-code": {
        "global": Path.home() / ".claude" / "skills" / SKILL_NAME,
        "project": Path.cwd() / ".claude" / "skills" / SKILL_NAME,
        "agents": Path.cwd() / ".agents" / "skills" / SKILL_NAME,
    },
    "trae": {
        "global": Path.home() / ".trae" / "skills" / SKILL_NAME,
        "project": Path.cwd() / ".trae" / "skills" / SKILL_NAME,
    },
    "openclaw": {
        "skill": Path.home() / ".openclaw" / "workspace" / "skills" / SKILL_NAME,
        "agent": Path.home() / ".openclaw" / "agents" / "prd-reviewer",
    },
    "hermes": {
        "skill": Path.home() / ".hermes" / "skills" / SKILL_NAME,
        "soul": Path.home() / ".hermes" / "SOUL.md",
    },
}


def copy_skill(dest_dir: Path, include_references: bool = True):
    """复制 SKILL.md 和参考文档到目标目录。"""
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 复制 SKILL.md
    shutil.copy2(CORE_SKILL, dest_dir / "SKILL.md")
    print(f"  ✅ {dest_dir / 'SKILL.md'}")

    # 复制参考文档
    if include_references and REFERENCES_DIR.exists():
        ref_dir = dest_dir / "references"
        ref_dir.mkdir(exist_ok=True)
        for ref_file in REFERENCES_DIR.iterdir():
            if ref_file.is_file():
                shutil.copy2(ref_file, ref_dir / ref_file.name)
                print(f"  ✅ {ref_dir / ref_file.name}")


def deploy_platform(platform: str, target: str = None):
    """部署到指定平台。"""
    print(f"\n📦 部署到 {platform}...")
    config = PLATFORMS.get(platform)
    if not config:
        print(f"  ❌ 未知平台: {platform}")
        return

    for name, dest in config.items():
        if target and name != target:
            continue

        # OpenClaw 特殊处理：只复制 agent.md
        if platform == "openclaw":
            if name == "agent":
                agent_dest = dest
                agent_dest.mkdir(parents=True, exist_ok=True)
                agent_md = PROJECT_ROOT / "platforms" / "openclaw" / "agent.md"
                if agent_md.exists():
                    shutil.copy2(agent_md, agent_dest / "agent.md")
                    print(f"  ✅ {agent_dest / 'agent.md'}")
                continue
            if name == "skill":
                copy_skill(dest)
                continue

        # Hermes 特殊处理
        if platform == "hermes":
            if name == "soul":
                soul_md = PROJECT_ROOT / "platforms" / "hermes" / "SOUL.md"
                if soul_md.exists():
                    # 不覆盖已有的 SOUL.md
                    if dest.exists():
                        backup = dest.with_suffix(".md.bak")
                        print(f"  ⚠️  已存在的 SOUL.md 备份到 {backup}")
                        shutil.copy2(dest, backup)
                    shutil.copy2(soul_md, dest)
                    print(f"  ✅ {dest}")
                continue
            if name == "skill":
                copy_skill(dest)
                continue

        # Claude Code / TRAE: 部署到第一个可用目录
        copy_skill(dest)
        break  # 只部署到一个位置


def main():
    platform = sys.argv[1] if len(sys.argv) > 1 else "all"

    # 检查核心文件是否存在
    if not CORE_SKILL.exists():
        print(f"❌ 核心文件不存在: {CORE_SKILL}")
        print("   请确保在项目根目录下运行此脚本。")
        sys.exit(1)

    print("=" * 50)
    print("PRD Reviewer Agent - 一键部署")
    print("=" * 50)

    if platform == "all":
        for p in PLATFORMS:
            deploy_platform(p)
    else:
        if platform not in PLATFORMS:
            print(f"❌ 不支持的平台: {platform}")
            print(f"   支持的平台: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        deploy_platform(platform)

    print("\n" + "=" * 50)
    print("🎉 部署完成！")
    print("=" * 50)
    print("\n各平台使用方式：")
    print("  Claude Code: 将 SKILL.md 放入 .claude/skills/ 或 .agents/skills/")
    print("  TRAE:        将 SKILL.md 放入 .trae/skills/")
    print("  OpenClaw:    openclaw agents add prd-reviewer --identity <agent.md>")
    print("  Hermes:      将 SKILL.md 放入 ~/.hermes/skills/")


if __name__ == "__main__":
    main()
