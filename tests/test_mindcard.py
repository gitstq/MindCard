#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindCard - Unit Tests
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import mindcard


class TestMindCard(unittest.TestCase):
    """Test cases for MindCard."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="mindcard_test_")
        self.original_config_dir = mindcard.CONFIG_DIR
        self.original_cards_dir = mindcard.CARDS_DIR
        self.original_config_file = mindcard.CONFIG_FILE
        self.original_index_file = mindcard.INDEX_FILE

        # Override paths for testing
        mindcard.CONFIG_DIR = Path(self.test_dir)
        mindcard.CARDS_DIR = Path(self.test_dir) / "cards"
        mindcard.CONFIG_FILE = Path(self.test_dir) / "config.json"
        mindcard.INDEX_FILE = Path(self.test_dir) / "index.json"

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

        # Restore original paths
        mindcard.CONFIG_DIR = self.original_config_dir
        mindcard.CARDS_DIR = self.original_cards_dir
        mindcard.CONFIG_FILE = self.original_config_file
        mindcard.INDEX_FILE = self.original_index_file

    def test_init_config(self):
        """Test configuration initialization."""
        mindcard.init_config()
        self.assertTrue(mindcard.CONFIG_DIR.exists())
        self.assertTrue(mindcard.CARDS_DIR.exists())
        self.assertTrue(mindcard.CONFIG_FILE.exists())
        self.assertTrue(mindcard.INDEX_FILE.exists())

    def test_load_save_config(self):
        """Test configuration load and save."""
        mindcard.init_config()
        config = mindcard.load_config()
        self.assertIn("editor", config)
        self.assertIn("theme", config)

        config["theme"] = "dark"
        mindcard.save_config(config)

        config2 = mindcard.load_config()
        self.assertEqual(config2["theme"], "dark")

    def test_generate_id(self):
        """Test ID generation."""
        id1 = mindcard.generate_id()
        id2 = mindcard.generate_id()
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("card_"))

    def test_extract_frontmatter(self):
        """Test frontmatter extraction."""
        content = """---
title: Test
created: 2025-01-01
tags: ["test"]
---

# Test Content
"""
        fm, body = mindcard.extract_frontmatter(content)
        self.assertEqual(fm.get("title"), "Test")
        self.assertIn("# Test Content", body)

    def test_auto_extract_tags(self):
        """Test auto tag extraction."""
        content = "This is about Python and Docker. #testing #ai"
        tags = mindcard.auto_extract_tags(content)
        self.assertIn("python", tags)
        self.assertIn("docker", tags)
        self.assertIn("testing", tags)
        self.assertIn("ai", tags)

    def test_create_card(self):
        """Test card creation."""
        mindcard.init_config()
        card_id = mindcard.create_card("Test Card", "test", ["tag1", "tag2"])

        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 1)
        self.assertEqual(index["cards"][0]["title"], "Test Card")

        card_file = mindcard.CARDS_DIR / f"{card_id}.md"
        self.assertTrue(card_file.exists())

    def test_list_cards(self):
        """Test card listing."""
        mindcard.init_config()
        mindcard.create_card("Card 1", "cat1", ["tag1"])
        mindcard.create_card("Card 2", "cat2", ["tag2"])

        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 2)

    def test_delete_card(self):
        """Test card deletion."""
        mindcard.init_config()
        card_id = mindcard.create_card("Delete Me", "test", [])

        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 1)

        mindcard.delete_card(card_id)
        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 0)

    def test_search_cards(self):
        """Test card search."""
        mindcard.init_config()
        mindcard.create_card("Python Tips", "python", ["tips"])
        mindcard.create_card("Docker Guide", "docker", ["guide"])

        # We can't easily test search output, but we can test it doesn't crash
        # This is a basic smoke test
        try:
            mindcard.search_cards("python")
        except Exception as e:
            self.fail(f"search_cards raised {e}")

    def test_export_cards(self):
        """Test card export."""
        mindcard.init_config()
        mindcard.create_card("Export Test", "test", [])

        output_file = Path(self.test_dir) / "export.md"
        mindcard.export_cards(str(output_file), "md")
        self.assertTrue(output_file.exists())

    def test_card_templates(self):
        """Test card templates."""
        self.assertIn("default", mindcard.CARD_TEMPLATES)
        self.assertIn("minimal", mindcard.CARD_TEMPLATES)
        self.assertIn("structured", mindcard.CARD_TEMPLATES)

        template = mindcard.CARD_TEMPLATES["default"]
        self.assertIn("{title}", template)
        self.assertIn("{created}", template)

    def test_themes(self):
        """Test themes."""
        self.assertIn("default", mindcard.THEMES)
        self.assertIn("dark", mindcard.THEMES)
        self.assertIn("light", mindcard.THEMES)

        theme = mindcard.THEMES["default"]
        self.assertIn("primary", theme)
        self.assertIn("reset", theme)


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="mindcard_int_test_")
        self.original_config_dir = mindcard.CONFIG_DIR
        self.original_cards_dir = mindcard.CARDS_DIR
        self.original_config_file = mindcard.CONFIG_FILE
        self.original_index_file = mindcard.INDEX_FILE

        mindcard.CONFIG_DIR = Path(self.test_dir)
        mindcard.CARDS_DIR = Path(self.test_dir) / "cards"
        mindcard.CONFIG_FILE = Path(self.test_dir) / "config.json"
        mindcard.INDEX_FILE = Path(self.test_dir) / "index.json"

    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
        mindcard.CONFIG_DIR = self.original_config_dir
        mindcard.CARDS_DIR = self.original_cards_dir
        mindcard.CONFIG_FILE = self.original_config_file
        mindcard.INDEX_FILE = self.original_index_file

    def test_full_workflow(self):
        """Test complete workflow."""
        mindcard.init_config()

        # Create cards
        id1 = mindcard.create_card("Python Tips", "python", ["tips", "python"])
        id2 = mindcard.create_card("Docker Guide", "docker", ["docker", "devops"])
        id3 = mindcard.create_card("React Hooks", "frontend", ["react", "javascript"])

        # Verify index
        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 3)

        # Verify tags and categories
        self.assertIn("python", index["tags"])
        self.assertIn("docker", index["tags"])
        self.assertIn("python", index["categories"])
        self.assertIn("docker", index["categories"])

        # Delete one card
        mindcard.delete_card(id2)
        index = mindcard.load_index()
        self.assertEqual(len(index["cards"]), 2)

        # Export
        export_file = Path(self.test_dir) / "export.json"
        mindcard.export_cards(str(export_file), "json")
        self.assertTrue(export_file.exists())

        with open(export_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["total_cards"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
