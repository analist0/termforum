# 🗣️ TermForum

**A beautiful terminal-based forum application with Markdown support and Glow rendering**

```
┌─────────────────────────────────────────────────────────────┐
│                      TermForum v0.1.0                        │
│              📋 Threads • 💬 Posts • 🎨 Markdown             │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Features

- 📋 **Threads & Posts** - Create and browse discussion threads
- 📁 **Categories** - Organize topics by category
- 🎨 **Markdown Support** - Write with full Markdown syntax
- 🌟 **Glow Rendering** - Beautiful markdown rendering via Glow
- ⌨️ **Vim Keybindings** - Navigate like a pro
- 🔍 **Search** - Find threads and posts instantly
- 👤 **User Profiles** - Track your contributions
- ⬆️ **Voting System** - Upvote/downvote threads and posts
- 🔖 **Bookmarks** - Save your favorite threads
- 🏷️ **Tags** - Categorize threads with tags
- 💾 **SQLite Database** - Fast and reliable storage
- 🎨 **Nerd Fonts Icons** - Beautiful UI with icons

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd ~
git clone https://github.com/analist0/termforum.git
cd termforum

# Install with pip
pip install -e .

# Or install dependencies manually
pip install textual rich markdown python-slugify click
```

### First Run

```bash
# Launch TermForum
termforum

# Or run directly
python -m termforum.main
```

### Requirements

- **Python 3.10+**
- **Glow** (for markdown rendering) - Install with:
  ```bash
  # Termux
  pkg install glow

  # macOS
  brew install glow

  # Linux
  # Download from: https://github.com/charmbracelet/glow/releases
  ```

## ⌨️ Keybindings

### Navigation
- `j/k` - Move down/up
- `g/G` - Go to top/bottom
- `Ctrl+d/u` - Page down/up
- `Enter` - Select item
- `Esc` - Go back
- `q` - Quit

### Actions
- `n` - New thread
- `r` - Reply to thread
- `R` - Reply to post
- `e` - Edit (own posts)
- `D` - Delete (own posts)
- `u` - Upvote
- `d` - Downvote
- `b` - Bookmark
- `/` - Search
- `?` - Help

### Screens
- `1` - Home
- `2` - Categories
- `3` - Search
- `4` - Profile
- `5` - Settings

### Editor
- `Ctrl+s` - Save
- `Ctrl+p` - Toggle preview
- `Ctrl+b` - Bold
- `Ctrl+i` - Italic
- `Ctrl+k` - Link
- `Ctrl+l` - Code block

## 📁 Project Structure

```
termforum/
├── termforum/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── app.py               # Textual app
│   ├── models/              # Data models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── thread.py
│   │   └── post.py
│   ├── storage/             # Database layer
│   │   ├── database.py
│   │   └── schema.sql
│   ├── ui/                  # UI components
│   │   ├── screens/         # Main screens
│   │   └── widgets/         # Reusable widgets
│   └── utils/               # Utilities
│       ├── glow.py          # Glow integration
│       └── keybindings.py   # Keybinding definitions
├── tests/                   # Tests
├── docs/                    # Documentation
├── pyproject.toml
├── README.md
└── LICENSE
```

## 🎨 Screenshots

*Coming soon...*

## 🔧 Configuration

Configuration file: `~/.config/termforum/config.json`

```json
{
  "theme": "dark",
  "vim_mode": true,
  "glow_style": "dark",
  "auto_save_drafts": true,
  "database_path": "~/.termforum/forum.db"
}
```

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

## 🐛 Known Issues

- Windows support is experimental (Textual limitation)
- Nested replies limited to 3 levels for readability

## 🚧 Roadmap

- [x] Basic thread/post functionality
- [x] Markdown support with Glow
- [x] SQLite database
- [ ] Real-time updates
- [ ] File uploads
- [ ] User mentions (@username)
- [ ] Email notifications
- [ ] GitHub Gist export
- [ ] Import from JSON
- [ ] Dark/Light themes
- [ ] Custom categories
- [ ] Moderator tools
- [ ] API for bots

---

**Made with ❤️ in Termux**
