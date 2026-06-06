#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindCard - Terminal AI-Powered Markdown Knowledge Card Manager
轻量级终端AI驱动的Markdown知识卡片管理器

A lightweight, zero-dependency CLI tool for managing markdown knowledge cards
with AI-powered tagging, smart search, and beautiful terminal UI.
"""

import argparse
import json
import os
import re
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"
__author__ = "MindCard Team"

# Configuration
CONFIG_DIR = Path.home() / ".mindcard"
CARDS_DIR = CONFIG_DIR / "cards"
CONFIG_FILE = CONFIG_DIR / "config.json"
INDEX_FILE = CONFIG_DIR / "index.json"

DEFAULT_CONFIG = {
    "editor": os.environ.get("EDITOR", "nano"),
    "theme": "default",
    "auto_tag": True,
    "ai_provider": "none",
    "ai_api_key": "",
    "ai_model": "",
    "default_category": "general",
    "date_format": "%Y-%m-%d %H:%M",
    "card_template": "default",
}

THEMES = {
    "default": {
        "primary": "\033[36m",      # Cyan
        "secondary": "\033[35m",    # Magenta
        "success": "\033[32m",      # Green
        "warning": "\033[33m",      # Yellow
        "error": "\033[31m",        # Red
        "info": "\033[34m",         # Blue
        "dim": "\033[90m",          # Gray
        "bold": "\033[1m",
        "reset": "\033[0m",
    },
    "dark": {
        "primary": "\033[38;5;81m",
        "secondary": "\033[38;5;183m",
        "success": "\033[38;5;114m",
        "warning": "\033[38;5;180m",
        "error": "\033[38;5;167m",
        "info": "\033[38;5;68m",
        "dim": "\033[38;5;240m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    },
    "light": {
        "primary": "\033[34m",
        "secondary": "\033[35m",
        "success": "\033[32m",
        "warning": "\033[33m",
        "error": "\033[31m",
        "info": "\033[36m",
        "dim": "\033[37m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }
}

CARD_TEMPLATES = {
    "default": """---
title: {title}
created: {created}
category: {category}
tags: {tags}
---

# {title}

## Summary

<!-- Write a brief summary here -->

## Details

<!-- Add detailed content here -->

## References

<!-- Add links or references -->
""",
    "minimal": """---
title: {title}
created: {created}
tags: {tags}
---

# {title}

<!-- Your content here -->
""",
    "structured": """---
title: {title}
created: {created}
updated: {created}
category: {category}
tags: {tags}
priority: medium
status: active
---

# {title}

## Problem Statement

<!-- What problem does this address? -->

## Solution

<!-- What is the solution or approach? -->

## Implementation

<!-- How to implement it -->

## Examples

```python
# Add code examples here
```

## Notes

<!-- Additional notes -->
"""
}


_id_counter = 0

def get_theme():
    """Get current theme colors."""
    config = load_config()
    theme_name = config.get("theme", "default")
    return THEMES.get(theme_name, THEMES["default"])


def color(text, color_name):
    """Apply color to text."""
    theme = get_theme()
    return f"{theme.get(color_name, '')}{text}{theme['reset']}"


def init_config():
    """Initialize configuration directory and files."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CARDS_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)

    if not INDEX_FILE.exists():
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump({"cards": [], "tags": [], "categories": []}, f, indent=2)


def load_config():
    """Load configuration."""
    init_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """Save configuration."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_index():
    """Load card index."""
    init_config()
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index):
    """Save card index."""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def generate_id():
    """Generate unique card ID."""
    import time
    global _id_counter
    _id_counter += 1
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    millis = int(time.time() * 1000) % 1000
    return f"card_{timestamp}_{millis:03d}_{_id_counter:04d}"


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        fm = {}
        for line in fm_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm, content[match.end():]
    return {}, content


def auto_extract_tags(content):
    """Auto-extract tags from content using keyword analysis."""
    tags = set()

    # Common tech keywords
    tech_keywords = {
        'python': 'python', 'javascript': 'javascript', 'js': 'javascript',
        'typescript': 'typescript', 'ts': 'typescript', 'java': 'java',
        'go': 'golang', 'rust': 'rust', 'c++': 'cpp', 'cpp': 'cpp',
        'react': 'react', 'vue': 'vue', 'angular': 'angular',
        'docker': 'docker', 'kubernetes': 'kubernetes', 'k8s': 'kubernetes',
        'aws': 'aws', 'azure': 'azure', 'gcp': 'gcp', 'cloud': 'cloud',
        'ai': 'ai', 'ml': 'machine-learning', 'machine learning': 'machine-learning',
        'llm': 'llm', 'api': 'api', 'rest': 'rest-api', 'graphql': 'graphql',
        'database': 'database', 'sql': 'sql', 'nosql': 'nosql',
        'security': 'security', 'testing': 'testing', 'devops': 'devops',
        'git': 'git', 'github': 'github', 'ci/cd': 'cicd',
        'frontend': 'frontend', 'backend': 'backend', 'fullstack': 'fullstack',
        'linux': 'linux', 'bash': 'bash', 'shell': 'shell',
        'algorithm': 'algorithm', 'data structure': 'data-structure',
        'performance': 'performance', 'optimization': 'optimization',
        'debugging': 'debugging', 'refactoring': 'refactoring',
        'design pattern': 'design-pattern', 'architecture': 'architecture',
        'microservices': 'microservices', 'serverless': 'serverless',
        'blockchain': 'blockchain', 'web3': 'web3',
    }

    content_lower = content.lower()
    for keyword, tag in tech_keywords.items():
        if keyword in content_lower:
            tags.add(tag)

    # Extract hashtags
    hashtag_pattern = r'#(\w+)'
    hashtags = re.findall(hashtag_pattern, content)
    tags.update(hashtags)

    return sorted(list(tags))


def create_card(title, category=None, tags=None, template=None):
    """Create a new knowledge card."""
    config = load_config()
    card_id = generate_id()
    created = datetime.now().strftime(config.get("date_format", "%Y-%m-%d %H:%M"))

    category = category or config.get("default_category", "general")
    tags = tags or []

    template_name = template or config.get("card_template", "default")
    template_content = CARD_TEMPLATES.get(template_name, CARD_TEMPLATES["default"])

    tags_str = json.dumps(tags) if tags else "[]"
    content = template_content.format(
        title=title,
        created=created,
        category=category,
        tags=tags_str
    )

    card_file = CARDS_DIR / f"{card_id}.md"
    with open(card_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Update index
    index = load_index()
    card_info = {
        "id": card_id,
        "title": title,
        "created": created,
        "category": category,
        "tags": tags,
        "file": str(card_file),
    }
    index["cards"].append(card_info)

    # Update tags and categories
    for tag in tags:
        if tag not in index["tags"]:
            index["tags"].append(tag)
    if category not in index["categories"]:
        index["categories"].append(category)

    save_index(index)

    print(color(f"✅ Card created successfully!", "success"))
    print(color(f"   ID: {card_id}", "info"))
    print(color(f"   Title: {title}", "primary"))
    print(color(f"   Category: {category}", "secondary"))
    print(color(f"   File: {card_file}", "dim"))

    return card_id


def edit_card(card_id):
    """Edit a knowledge card."""
    index = load_index()
    card = None
    for c in index["cards"]:
        if c["id"] == card_id or c["title"] == card_id:
            card = c
            break

    if not card:
        print(color(f"❌ Card not found: {card_id}", "error"))
        return

    config = load_config()
    editor = config.get("editor", os.environ.get("EDITOR", "nano"))
    card_file = Path(card["file"])

    if not card_file.exists():
        print(color(f"❌ Card file not found: {card_file}", "error"))
        return

    # Update frontmatter with updated timestamp
    with open(card_file, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = extract_frontmatter(content)
    if fm:
        updated = datetime.now().strftime(config.get("date_format", "%Y-%m-%d %H:%M"))
        new_fm = []
        for key, value in fm.items():
            if key == "updated":
                new_fm.append(f"updated: {updated}")
            else:
                new_fm.append(f"{key}: {value}")
        if "updated" not in fm:
            new_fm.append(f"updated: {updated}")
        new_content = "---\n" + "\n".join(new_fm) + "\n---\n" + body
        with open(card_file, "w", encoding="utf-8") as f:
            f.write(new_content)

    subprocess.call([editor, str(card_file)])

    # Re-index after edit
    with open(card_file, "r", encoding="utf-8") as f:
        new_content = f.read()

    fm, _ = extract_frontmatter(new_content)
    if fm:
        card["title"] = fm.get("title", card["title"])
        card["category"] = fm.get("category", card["category"])
        tags_str = fm.get("tags", "[]")
        try:
            card["tags"] = json.loads(tags_str) if tags_str.startswith("[") else [tags_str]
        except:
            card["tags"] = tags_str.strip("[]").replace('"', '').split(", ") if tags_str != "[]" else []

    save_index(index)
    print(color(f"✅ Card updated: {card['title']}", "success"))


def delete_card(card_id):
    """Delete a knowledge card."""
    index = load_index()
    card = None
    card_idx = -1
    for i, c in enumerate(index["cards"]):
        if c["id"] == card_id or c["title"] == card_id:
            card = c
            card_idx = i
            break

    if not card:
        print(color(f"❌ Card not found: {card_id}", "error"))
        return

    card_file = Path(card["file"])
    if card_file.exists():
        card_file.unlink()

    index["cards"].pop(card_idx)
    save_index(index)

    print(color(f"🗑️  Card deleted: {card['title']}", "warning"))


def list_cards(category=None, tag=None, search=None):
    """List knowledge cards with filters."""
    index = load_index()
    cards = index["cards"]

    if category:
        cards = [c for c in cards if c.get("category") == category]
    if tag:
        cards = [c for c in cards if tag in c.get("tags", [])]
    if search:
        search_lower = search.lower()
        cards = [c for c in cards if search_lower in c.get("title", "").lower()]

    if not cards:
        print(color("📭 No cards found.", "dim"))
        return

    print(color("\n📚 Knowledge Cards", "bold"))
    print(color("=" * 60, "dim"))

    for card in cards:
        tags_str = ", ".join(card.get("tags", [])) or "none"
        print(color(f"\n📝 {card['title']}", "primary"))
        print(color(f"   ID: {card['id']}", "dim"))
        print(color(f"   Category: {card.get('category', 'general')}", "secondary"))
        print(color(f"   Tags: {tags_str}", "info"))
        print(color(f"   Created: {card.get('created', 'unknown')}", "dim"))

    print(color(f"\n📊 Total: {len(cards)} cards", "success"))


def view_card(card_id):
    """View a knowledge card."""
    index = load_index()
    card = None
    for c in index["cards"]:
        if c["id"] == card_id or c["title"] == card_id:
            card = c
            break

    if not card:
        print(color(f"❌ Card not found: {card_id}", "error"))
        return

    card_file = Path(card["file"])
    if not card_file.exists():
        print(color(f"❌ Card file not found: {card_file}", "error"))
        return

    with open(card_file, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = extract_frontmatter(content)

    print(color(f"\n📝 {card['title']}", "bold"))
    print(color("=" * 60, "dim"))

    if fm:
        for key, value in fm.items():
            print(color(f"{key}: ", "secondary") + color(value, "info"))
        print(color("-" * 60, "dim"))

    # Simple markdown rendering
    lines = body.strip().split('\n')
    for line in lines:
        line = line.rstrip()
        if line.startswith('# '):
            print(color(line, "bold"))
        elif line.startswith('## '):
            print(color(line, "primary"))
        elif line.startswith('### '):
            print(color(line, "secondary"))
        elif line.startswith('```'):
            print(color(line, "dim"))
        elif line.startswith('- ') or line.startswith('* '):
            print(color(f"  • {line[2:]}", "info"))
        elif line.startswith('> '):
            print(color(f"  │ {line[2:]}", "dim"))
        elif line.strip():
            print(line)

    print(color("=" * 60, "dim"))


def search_cards(query):
    """Search cards by content."""
    index = load_index()
    results = []

    query_lower = query.lower()

    for card in index["cards"]:
        score = 0
        card_file = Path(card["file"])

        # Title match (highest priority)
        if query_lower in card.get("title", "").lower():
            score += 10

        # Tag match
        for tag in card.get("tags", []):
            if query_lower in tag.lower():
                score += 5

        # Category match
        if query_lower in card.get("category", "").lower():
            score += 3

        # Content match
        if card_file.exists():
            try:
                with open(card_file, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    if query_lower in content:
                        score += 2
            except:
                pass

        if score > 0:
            results.append((score, card))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        print(color(f"🔍 No results found for: '{query}'", "warning"))
        return

    print(color(f"\n🔍 Search Results for '{query}'", "bold"))
    print(color("=" * 60, "dim"))

    for score, card in results:
        tags_str = ", ".join(card.get("tags", [])) or "none"
        print(color(f"\n📝 {card['title']} (score: {score})", "primary"))
        print(color(f"   ID: {card['id']}", "dim"))
        print(color(f"   Category: {card.get('category', 'general')}", "secondary"))
        print(color(f"   Tags: {tags_str}", "info"))

    print(color(f"\n📊 Found {len(results)} results", "success"))


def show_stats():
    """Show knowledge base statistics."""
    index = load_index()
    cards = index["cards"]

    total_cards = len(cards)
    total_tags = len(index.get("tags", []))
    total_categories = len(index.get("categories", []))

    # Category distribution
    cat_counts = {}
    tag_counts = {}
    for card in cards:
        cat = card.get("category", "general")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        for tag in card.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print(color("\n📊 MindCard Knowledge Base Statistics", "bold"))
    print(color("=" * 50, "dim"))
    print(color(f"📚 Total Cards: {total_cards}", "primary"))
    print(color(f"🏷️  Total Tags: {total_tags}", "secondary"))
    print(color(f"📁 Categories: {total_categories}", "info"))

    if cat_counts:
        print(color("\n📁 Category Distribution:", "bold"))
        for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * min(count, 20)
            print(color(f"  {cat:20s} {bar} {count}", "info"))

    if tag_counts:
        print(color("\n🏷️  Top Tags:", "bold"))
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(color(f"  #{tag:20s} {count}", "secondary"))


def export_cards(output_path, format_type="md"):
    """Export cards to a single file."""
    index = load_index()
    cards = index["cards"]

    if format_type == "md":
        with open(output_path, "w", encoding="utf-8") as out:
            out.write("# MindCard Knowledge Base Export\n\n")
            out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            out.write("---\n\n")

            for card in cards:
                card_file = Path(card["file"])
                if card_file.exists():
                    with open(card_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    out.write(content)
                    out.write("\n\n---\n\n")

    elif format_type == "json":
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_cards": len(cards),
            "cards": []
        }
        for card in cards:
            card_file = Path(card["file"])
            if card_file.exists():
                with open(card_file, "r", encoding="utf-8") as f:
                    content = f.read()
                card_data = dict(card)
                card_data["content"] = content
                export_data["cards"].append(card_data)

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(export_data, out, indent=2, ensure_ascii=False)

    print(color(f"✅ Exported {len(cards)} cards to {output_path}", "success"))


def import_cards(input_path):
    """Import cards from a file."""
    path = Path(input_path)
    if not path.exists():
        print(color(f"❌ File not found: {input_path}", "error"))
        return

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        imported = 0
        for card_data in data.get("cards", []):
            title = card_data.get("title", "Untitled")
            category = card_data.get("category", "general")
            tags = card_data.get("tags", [])
            content = card_data.get("content", "")

            card_id = generate_id()
            card_file = CARDS_DIR / f"{card_id}.md"
            with open(card_file, "w", encoding="utf-8") as f:
                f.write(content)

            index = load_index()
            card_info = {
                "id": card_id,
                "title": title,
                "created": card_data.get("created", datetime.now().strftime("%Y-%m-%d %H:%M")),
                "category": category,
                "tags": tags,
                "file": str(card_file),
            }
            index["cards"].append(card_info)
            save_index(index)
            imported += 1

        print(color(f"✅ Imported {imported} cards", "success"))


def show_dashboard():
    """Show interactive dashboard."""
    index = load_index()
    cards = index["cards"]

    print(color("\n" + "=" * 60, "dim"))
    print(color("  🧠 MindCard - Knowledge Card Manager", "bold"))
    print(color("  " + "─" * 56, "dim"))

    # Recent cards
    recent = sorted(cards, key=lambda x: x.get("created", ""), reverse=True)[:5]
    print(color("\n  📚 Recent Cards:", "primary"))
    for card in recent:
        print(color(f"     • {card['title']}", "info"))

    # Stats
    print(color(f"\n  📊 Total: {len(cards)} cards | {len(index.get('tags', []))} tags | {len(index.get('categories', []))} categories", "secondary"))

    # Quick commands
    print(color("\n  ⌨️  Quick Commands:", "bold"))
    print(color("     mindcard add <title>     - Create new card", "dim"))
    print(color("     mindcard list            - List all cards", "dim"))
    print(color("     mindcard search <query>  - Search cards", "dim"))
    print(color("     mindcard stats           - Show statistics", "dim"))
    print(color("     mindcard config          - Configure settings", "dim"))

    print(color("\n" + "=" * 60, "dim"))


def configure():
    """Interactive configuration."""
    config = load_config()

    print(color("\n⚙️  MindCard Configuration", "bold"))
    print(color("=" * 50, "dim"))

    print(color(f"\n1. Editor: {config.get('editor', 'nano')}", "info"))
    print(color("2. Theme: " + config.get('theme', 'default'), "info"))
    print(color("3. Auto-tag: " + str(config.get('auto_tag', True)), "info"))
    print(color("4. Default Category: " + config.get('default_category', 'general'), "info"))
    print(color("5. Card Template: " + config.get('card_template', 'default'), "info"))

    print(color("\n💡 Edit config file directly:", "dim"))
    print(color(f"   {CONFIG_FILE}", "info"))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MindCard - Terminal AI-Powered Markdown Knowledge Card Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mindcard add "Python Tips" --category python --tags tips,tricks
  mindcard list --category python
  mindcard search "docker"
  mindcard view card_20250101120000
  mindcard edit "Python Tips"
  mindcard stats
        """
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new knowledge card")
    add_parser.add_argument("title", help="Card title")
    add_parser.add_argument("--category", "-c", help="Card category")
    add_parser.add_argument("--tags", "-t", help="Comma-separated tags")
    add_parser.add_argument("--template", help="Card template (default, minimal, structured)")

    # List command
    list_parser = subparsers.add_parser("list", help="List knowledge cards")
    list_parser.add_argument("--category", "-c", help="Filter by category")
    list_parser.add_argument("--tag", "-t", help="Filter by tag")
    list_parser.add_argument("--search", "-s", help="Search in titles")

    # View command
    view_parser = subparsers.add_parser("view", help="View a knowledge card")
    view_parser.add_argument("card_id", help="Card ID or title")

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a knowledge card")
    edit_parser.add_argument("card_id", help="Card ID or title")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a knowledge card")
    delete_parser.add_argument("card_id", help="Card ID or title")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search knowledge cards")
    search_parser.add_argument("query", help="Search query")

    # Stats command
    subparsers.add_parser("stats", help="Show knowledge base statistics")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export cards")
    export_parser.add_argument("output", help="Output file path")
    export_parser.add_argument("--format", "-f", choices=["md", "json"], default="md", help="Export format")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import cards")
    import_parser.add_argument("input", help="Input file path")

    # Config command
    subparsers.add_parser("config", help="Show configuration")

    # Dashboard command (default)
    subparsers.add_parser("dashboard", help="Show dashboard")

    args = parser.parse_args()

    # Initialize
    init_config()

    if args.command == "add":
        tags = args.tags.split(",") if args.tags else []
        create_card(args.title, args.category, tags, args.template)
    elif args.command == "list":
        list_cards(args.category, args.tag, args.search)
    elif args.command == "view":
        view_card(args.card_id)
    elif args.command == "edit":
        edit_card(args.card_id)
    elif args.command == "delete":
        delete_card(args.card_id)
    elif args.command == "search":
        search_cards(args.query)
    elif args.command == "stats":
        show_stats()
    elif args.command == "export":
        export_cards(args.output, args.format)
    elif args.command == "import":
        import_cards(args.input)
    elif args.command == "config":
        configure()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
