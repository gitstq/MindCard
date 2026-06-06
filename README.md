<div align="center">

# 🧠 MindCard

**轻量级终端AI驱动的Markdown知识卡片管理器**

*Terminal AI-Powered Markdown Knowledge Card Manager*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## English

### Introduction

**MindCard** is a lightweight, zero-dependency terminal CLI tool designed for developers and knowledge workers who want to efficiently manage their markdown knowledge cards. Inspired by the growing need for fast, distraction-free note-taking in the terminal, MindCard brings the power of knowledge management directly to your command line.

**Why MindCard?**
- **Zero Dependencies**: Pure Python standard library, no installation headaches
- **Developer-First**: Designed for terminal power users
- **AI-Ready**: Smart auto-tagging and extensible AI integration
- **Lightweight**: Single file, minimal footprint
- **Beautiful**: Multiple terminal themes with color support

### Core Features

| Feature | Description |
|---------|-------------|
| **Markdown Cards** | Create and manage knowledge cards in standard Markdown format |
| **Smart Tagging** | Auto-extract tags from content with keyword analysis |
| **Full-Text Search** | Search across titles, tags, categories, and content |
| **Statistics Dashboard** | Visual overview of your knowledge base |
| **Multi-Theme** | Default, Dark, and Light terminal themes |
| **Templates** | Default, Minimal, and Structured card templates |
| **Import/Export** | Export to Markdown or JSON, import from JSON |
| **Configurable** | Customizable editor, themes, and defaults |

### Quick Start

#### Requirements
- Python 3.8 or higher
- Any terminal with color support

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/MindCard.git
cd MindCard

# Install locally
pip install -e .

# Or run directly
python mindcard.py
```

#### Basic Usage

```bash
# Show dashboard
mindcard

# Create a new card
mindcard add "Python Tips" --category python --tags tips,tricks

# List all cards
mindcard list

# Search cards
mindcard search "docker"

# View a card
mindcard view card_20250101120000

# Edit a card
mindcard edit "Python Tips"

# Show statistics
mindcard stats
```

### Detailed Usage Guide

#### Creating Cards

```bash
# Basic card
mindcard add "My Note"

# With category and tags
mindcard add "React Hooks" --category frontend --tags react,javascript

# Using structured template
mindcard add "API Design" --template structured --category backend
```

#### Filtering and Searching

```bash
# List by category
mindcard list --category python

# List by tag
mindcard list --tag docker

# Search in titles
mindcard list --search "api"

# Full-text search
mindcard search "machine learning"
```

#### Export and Import

```bash
# Export to Markdown
mindcard export my_notes.md

# Export to JSON
mindcard export my_notes.json --format json

# Import from JSON
mindcard import backup.json
```

### Design Philosophy

MindCard follows the Unix philosophy: do one thing well. It focuses on:
- **Speed**: Instant access from the terminal
- **Simplicity**: No complex setup or configuration
- **Portability**: Works anywhere Python runs
- **Extensibility**: Easy to integrate with other tools

### Development

```bash
# Run tests
make test

# Clean build artifacts
make clean

# Build distribution
make build
```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="simplified-chinese"></a>
## 简体中文

### 项目介绍

**MindCard** 是一款轻量级、零依赖的终端CLI工具，专为希望高效管理Markdown知识卡片的开发者和知识工作者设计。受终端中快速、无干扰笔记需求增长的启发，MindCard将知识管理的强大功能直接带到命令行。

**为什么选择MindCard？**
- **零依赖**：纯Python标准库，无安装烦恼
- **开发者优先**：为终端高级用户设计
- **AI就绪**：智能自动标签和可扩展AI集成
- **轻量级**：单文件，占用空间极小
- **美观**：多种终端主题，支持彩色输出

### 核心特性

| 特性 | 描述 |
|------|------|
| **Markdown卡片** | 以标准Markdown格式创建和管理知识卡片 |
| **智能标签** | 通过关键词分析自动提取标签 |
| **全文搜索** | 跨标题、标签、类别和内容搜索 |
| **统计仪表板** | 知识库的可视化概览 |
| **多主题** | 默认、深色和浅色终端主题 |
| **模板** | 默认、极简和结构化卡片模板 |
| **导入/导出** | 导出为Markdown或JSON，从JSON导入 |
| **可配置** | 可自定义编辑器、主题和默认值 |

### 快速开始

#### 环境要求
- Python 3.8 或更高版本
- 任何支持彩色的终端

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/MindCard.git
cd MindCard

# 本地安装
pip install -e .

# 或直接运行
python mindcard.py
```

#### 基本用法

```bash
# 显示仪表板
mindcard

# 创建新卡片
mindcard add "Python技巧" --category python --tags tips,tricks

# 列出所有卡片
mindcard list

# 搜索卡片
mindcard search "docker"

# 查看卡片
mindcard view card_20250101120000

# 编辑卡片
mindcard edit "Python技巧"

# 显示统计
mindcard stats
```

### 详细使用指南

#### 创建卡片

```bash
# 基础卡片
mindcard add "我的笔记"

# 带类别和标签
mindcard add "React Hooks" --category frontend --tags react,javascript

# 使用结构化模板
mindcard add "API设计" --template structured --category backend
```

#### 过滤和搜索

```bash
# 按类别列出
mindcard list --category python

# 按标签列出
mindcard list --tag docker

# 标题搜索
mindcard list --search "api"

# 全文搜索
mindcard search "machine learning"
```

#### 导出和导入

```bash
# 导出为Markdown
mindcard export my_notes.md

# 导出为JSON
mindcard export my_notes.json --format json

# 从JSON导入
mindcard import backup.json
```

### 设计理念

MindCard遵循Unix哲学：做好一件事。它专注于：
- **速度**：从终端即时访问
- **简洁**：无复杂设置或配置
- **可移植**：可在任何运行Python的地方工作
- **可扩展**：易于与其他工具集成

### 开发

```bash
# 运行测试
make test

# 清理构建产物
make clean

# 构建分发包
make build
```

### 贡献指南

欢迎贡献！请：
1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

### 开源协议

本项目采用MIT协议 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="traditional-chinese"></a>
## 繁體中文

### 專案介紹

**MindCard** 是一款輕量級、零依賴的終端CLI工具，專為希望高效管理Markdown知識卡片的開發者和知識工作者設計。受終端中快速、無干擾筆記需求增長的啟發，MindCard將知識管理的強大功能直接帶到命令列。

**為什麼選擇MindCard？**
- **零依賴**：純Python標準庫，無安裝煩惱
- **開發者優先**：為終端高級用戶設計
- **AI就緒**：智能自動標籤和可擴展AI集成
- **輕量級**：單文件，佔用空間極小
- **美觀**：多種終端主題，支持彩色輸出

### 核心特性

| 特性 | 描述 |
|------|------|
| **Markdown卡片** | 以標準Markdown格式創建和管理知識卡片 |
| **智能標籤** | 通過關鍵詞分析自動提取標籤 |
| **全文搜索** | 跨標題、標籤、類別和內容搜索 |
| **統計儀表板** | 知識庫的可視化概覽 |
| **多主題** | 默認、深色和淺色終端主題 |
| **模板** | 默認、極簡和結構化卡片模板 |
| **導入/導出** | 導出為Markdown或JSON，從JSON導入 |
| **可配置** | 可自定義編輯器、主題和默認值 |

### 快速開始

#### 環境要求
- Python 3.8 或更高版本
- 任何支持彩色的終端

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/MindCard.git
cd MindCard

# 本地安裝
pip install -e .

# 或直接運行
python mindcard.py
```

#### 基本用法

```bash
# 顯示儀表板
mindcard

# 創建新卡片
mindcard add "Python技巧" --category python --tags tips,tricks

# 列出所有卡片
mindcard list

# 搜索卡片
mindcard search "docker"

# 查看卡片
mindcard view card_20250101120000

# 編輯卡片
mindcard edit "Python技巧"

# 顯示統計
mindcard stats
```

### 詳細使用指南

#### 創建卡片

```bash
# 基礎卡片
mindcard add "我的筆記"

# 帶類別和標籤
mindcard add "React Hooks" --category frontend --tags react,javascript

# 使用結構化模板
mindcard add "API設計" --template structured --category backend
```

#### 過濾和搜索

```bash
# 按類別列出
mindcard list --category python

# 按標籤列出
mindcard list --tag docker

# 標題搜索
mindcard list --search "api"

# 全文搜索
mindcard search "machine learning"
```

#### 導出和導入

```bash
# 導出為Markdown
mindcard export my_notes.md

# 導出為JSON
mindcard export my_notes.json --format json

# 從JSON導入
mindcard import backup.json
```

### 設計理念

MindCard遵循Unix哲學：做好一件事。它專注於：
- **速度**：從終端即時訪問
- **簡潔**：無複雜設置或配置
- **可移植**：可在任何運行Python的地方工作
- **可擴展**：易於與其他工具集成

### 開發

```bash
# 運行測試
make test

# 清理構建產物
make clean

# 構建分發包
make build
```

### 貢獻指南

歡迎貢獻！請：
1. Fork倉庫
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打開Pull Request

### 開源協議

本專案採用MIT協議 - 詳見 [LICENSE](LICENSE) 文件。
