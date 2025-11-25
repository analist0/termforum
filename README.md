# 🚀 TermForum Ultimate

**Advanced Terminal Forum for Developers, Hackers & Security Researchers**

```
┌─────────────────────────────────────────────────────────────┐
│                   TermForum Ultimate v0.1.0                  │
│         📋 Threads • 💬 Posts • 🤖 AI • 🎨 Markdown          │
│              Built for Programmers & Hackers                 │
└─────────────────────────────────────────────────────────────┘
```

> **3,756+ lines of code** | **30 files** | **13 developer categories** | **Ollama AI integration**

**🎯 Repository**: https://github.com/analist0/termforum

## ✨ Features

### 🎯 Core Features (Implemented)
- 📋 **Threads & Posts** - Full discussion system with nested replies
- 📁 **13 Developer Categories** - Programming, Security, AI, Web, Linux, Mobile, Cloud, Games, Resources
- 🎨 **Markdown Support** - Full Markdown syntax with code blocks
- 🌟 **Glow Rendering** - Beautiful markdown rendering via Glow
- ⌨️ **Vim Keybindings** - j/k navigation, Enter/Esc, professional workflow
- 💾 **SQLite Database** - Fast and reliable storage
- 🎨 **Rich UI** - Textual framework with beautiful styling
- 🤖 **Ollama AI Bot** - Built-in AI assistant with commands

### 🤖 AI Integration (Implemented)
- **@ai** - Mention AI for help
- **/summarize** - Summarize thread discussions
- **/ascii** - Generate ASCII art
- **/translate** - Translate content (Hebrew ⟷ English)
- **/help** - AI command help
- **Cloud Models** - deepseek-v3.1:671b, qwen3-coder:480b
- **Local Model** - qwen2.5-coder:7b (4.7 GB)

### 📱 Screens (Implemented)
- ✅ **Home Screen** - Forum stats, recent threads, activity feed
- ✅ **Categories Screen** - Browse all 13 categories
- ✅ **Thread View** - Full thread with nested replies (tree structure)

### 🚧 Coming Soon
- ⏳ **Thread Editor** - Create/edit threads with live preview
- ⏳ **Search Screen** - Find threads and posts
- ⏳ **User Profile** - View stats and history
- ⏳ **Settings Screen** - Themes (Dark, Kali, Matrix, Cyberpunk)
- ⏳ **Resources Library** - Cheat sheets, scripts, tutorials
- ⏳ **Built-in Tools** - ASCII generator, hex viewer, base64 encoder
- ⏳ **Voting System** - Upvote/downvote functionality
- ⏳ **Bookmarks** - Save favorite threads
- ⏳ **User Mentions** - @username with notifications
- ⏳ **Real-time Updates** - Live activity feed
- ⏳ **Export/Import** - GitHub Gist integration

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd ~
git clone https://github.com/analist0/termforum.git
cd termforum

# Install dependencies
pip install -e .
```

### First Run

```bash
# 1. Initialize database
python -m termforum.main init --db ~/.termforum/forum.db

# 2. Add developer categories (13 categories)
python update_categories.py

# 3. Create test data (optional)
python create_test_data.py

# 4. Run TermForum
python -m termforum.main run -u yossi

# Or use any username you created
```

### 📖 Full Demo Guide

See **[RUN_DEMO.md](RUN_DEMO.md)** for complete demo instructions, keyboard shortcuts, and troubleshooting.

### Requirements

- **Python 3.10+**
- **Glow** (for markdown rendering):
  ```bash
  # Termux
  pkg install glow

  # macOS
  brew install glow

  # Linux
  # Download from: https://github.com/charmbracelet/glow/releases
  ```
- **Ollama** (optional, for AI features):
  ```bash
  # Install Ollama
  curl -fsSL https://ollama.com/install.sh | sh

  # Pull a model
  ollama pull qwen2.5-coder:7b

  # Or use cloud models (no installation needed)
  # deepseek-v3.1:671b-cloud
  # qwen3-coder:480b-cloud
  ```

## ⌨️ Keybindings

### ✅ Implemented

**Global:**
- `1` - Home
- `2` - Categories
- `3` - Search (coming soon)
- `4` - Profile (coming soon)
- `5` - Settings (coming soon)
- `n` - New Thread (coming soon)
- `q` - Quit
- `?` - Help

**Navigation:**
- `j` - Move down
- `k` - Move up
- `Enter` - Select
- `Esc` - Back

### ⏳ Coming Soon

**Thread Actions:**
- `r` - Reply
- `u` - Upvote
- `d` - Downvote
- `b` - Bookmark
- `e` - Edit (own posts)
- `D` - Delete (own posts)

**Editor:**
- `Ctrl+s` - Save
- `Ctrl+p` - Toggle preview
- `Ctrl+b` - Bold
- `Ctrl+i` - Italic
- `Ctrl+k` - Link
- `Ctrl+l` - Code block

## 📁 13 Developer Categories

1. 💬 **General** - General discussions
2. 📢 **Announcements** - Important announcements
3. 🆘 **Support** - Help and support
4. 🎲 **Off-Topic** - Off-topic discussions
5. 💻 **Programming** - Programming languages, algorithms, best practices
6. 🔐 **Security & Hacking** - Pentesting, ethical hacking, vulnerabilities
7. 🤖 **AI & Machine Learning** - LLMs, neural networks, AI tools
8. 🌐 **Web Development** - Frontend, backend, full-stack
9. 🐧 **Linux & Terminal** - CLI tools, shell scripting, system administration
10. 📱 **Mobile Development** - iOS, Android, React Native
11. ☁️ **Cloud & DevOps** - Docker, Kubernetes, CI/CD, infrastructure
12. 🎮 **Game Development** - Unity, Unreal, game engines
13. 📚 **Resources & Tutorials** - Learning materials, documentation, guides

## 💻 Tech Stack

### Core
- **Python 3.10+** - Main language
- **Textual 0.50.0+** - Terminal UI framework
- **Rich 13.7.0+** - Text formatting and styling
- **SQLite3** - Embedded database
- **Click** - CLI framework

### UI & Graphics
- **Glow** - Markdown rendering (external)
- **pyfiglet** - ASCII art generation
- **art** - ASCII art library
- **asciimatics** - Terminal animations
- **blessed** - Advanced terminal control
- **prompt-toolkit** - Enhanced input

### AI Integration
- **Ollama** - Local LLM inference (external)
- **aiohttp** - Async HTTP for Ollama API

### Utilities
- **python-slugify** - URL-safe slugs
- **markdown** - Markdown processing
- **Pillow** - Image processing for ASCII conversion

## 📁 Project Structure

```
termforum/
├── termforum/
│   ├── __init__.py
│   ├── main.py              # CLI entry point (Click)
│   ├── app.py               # Main Textual application
│   ├── models/              # Data models (dataclasses)
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── category.py      # Category model
│   │   ├── thread.py        # Thread model
│   │   └── post.py          # Post model with nested replies
│   ├── storage/             # Database layer
│   │   ├── __init__.py
│   │   └── database.py      # SQLite database manager
│   ├── ai/                  # AI integration
│   │   ├── __init__.py
│   │   ├── ollama_client.py # Ollama API client
│   │   ├── ai_bot.py        # AI bot logic
│   │   ├── commands.py      # Command parser
│   │   └── prompts.py       # System prompts (Hebrew/English)
│   ├── ui/                  # UI components
│   │   ├── screens/         # Main screens
│   │   │   ├── __init__.py
│   │   │   ├── home.py      # Home screen (stats, threads)
│   │   │   ├── categories.py # Categories browser
│   │   │   └── thread_view.py # Thread view with nested replies
│   │   └── widgets/         # Reusable widgets (TBD)
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── glow.py          # Glow markdown rendering
│       └── ascii_art.py     # ASCII art utilities
├── update_categories.py     # Script to add 13 categories
├── create_test_data.py      # Script to create test data
├── pyproject.toml           # Project dependencies
├── README.md                # This file
├── RUN_DEMO.md              # Complete demo guide
├── ULTIMATE_DESIGN.md       # Full design document
└── .gitignore
```

**Stats:**
- 📦 **30 files**
- 📝 **3,756+ lines of code**
- 🧩 **12 dependencies**
- 🎨 **13 categories**

## 🎨 Screenshots

### Home Screen
```
╭─────────────────────────────────────────────────────────────╮
│ 🏠 Forum Home                                                │
│                                                              │
│ 📊 Forum Stats:                                              │
│ • 5 Users  • 4 Threads  • 5 Posts  • 13 Categories          │
│                                                              │
│ 📋 Recent Threads:                                           │
│   [1] 💻 Getting Started with Python - alice (2 posts)      │
│   [2] 🔐 Security Best Practices - bob (1 post)             │
│   [3] 🤖 Local LLMs with Ollama - charlie (1 post)          │
│   [4] 🌐 Modern Web Development - dave (1 post)             │
│                                                              │
│ [Enter] Open  [J/K] Navigate  [2] Categories  [Q] Quit      │
╰─────────────────────────────────────────────────────────────╯
```

### Categories Screen
```
╭─────────────────────────────────────────────────────────────╮
│ 📁 Forum Categories                                          │
│                                                              │
│ 💬 General                                                   │
│    General discussions                                       │
│    📋 0 threads • 💬 0 posts                                 │
│                                                              │
│ 💻 Programming                                               │
│    Programming languages, algorithms, best practices        │
│    📋 1 threads • 💬 2 posts                                 │
│                                                              │
│ 🔐 Security & Hacking                                        │
│    Pentesting, ethical hacking, vulnerabilities             │
│    📋 1 threads • 💬 1 posts                                 │
│                                                              │
│ [Enter] Open  [J/K] Navigate  [Esc] Back                    │
╰─────────────────────────────────────────────────────────────╯
```

## 🔧 Configuration

Configuration file: `~/.termforum/forum.db` (SQLite database)

All settings stored in database. Future config file planned for themes and preferences.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

- Built with [Textual](https://github.com/Textualize/textual) by [@willmcgugan](https://github.com/willmcgugan)
- Markdown rendering by [Glow](https://github.com/charmbracelet/glow)
- Icons from [Nerd Fonts](https://www.nerdfonts.com/)

## 🚧 Roadmap

### ✅ Phase 1: Core Foundation (COMPLETED)
- [x] Data models (User, Category, Thread, Post)
- [x] SQLite database with foreign keys
- [x] 13 developer-focused categories
- [x] Nested replies (tree structure)
- [x] Home screen (stats + threads)
- [x] Categories screen
- [x] Thread view screen
- [x] Vim keybindings (j/k navigation)
- [x] Markdown support
- [x] Glow integration
- [x] Ollama AI integration
- [x] AI commands (@ai, /summarize, /ascii, /translate)
- [x] Test data generation
- [x] Git repository
- [x] GitHub repository

### 🔄 Phase 2: Editing & Creation (IN PROGRESS)
- [ ] Thread editor (create/edit threads)
- [ ] Post editor (create replies)
- [ ] Live markdown preview
- [ ] Code syntax highlighting
- [ ] Image upload support
- [ ] File attachments

### 📋 Phase 3: Advanced Features
- [ ] Search (threads, posts, users)
- [ ] User profiles (stats, history)
- [ ] Voting system (upvote/downvote)
- [ ] Bookmarks
- [ ] User mentions (@username)
- [ ] Notifications system
- [ ] Real-time updates
- [ ] Moderation tools (pin, lock, delete)

### 🎨 Phase 4: UI Enhancements
- [ ] Multiple themes (Dark, Kali, Matrix, Cyberpunk)
- [ ] Animations and transitions
- [ ] Custom category colors
- [ ] Avatar system
- [ ] Emoji picker
- [ ] Split-view mode

### 🛠️ Phase 5: Developer Tools
- [ ] Resources library
- [ ] Built-in tools (hex viewer, base64, ASCII generator)
- [ ] Code snippet manager
- [ ] Cheat sheets browser
- [ ] Terminal emulator integration
- [ ] Git integration

### 🌐 Phase 6: Integration & Export
- [ ] GitHub Gist export
- [ ] JSON import/export
- [ ] RSS feed
- [ ] API for bots
- [ ] Webhook support
- [ ] Email notifications

## 🐛 Known Issues

- Windows support is experimental (Textual limitation)
- Ollama cloud models may have latency
- Glow required for markdown rendering

---

**Made with ❤️ in Termux**
