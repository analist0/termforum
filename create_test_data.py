"""Create test data for TermForum"""

from termforum.storage import Database
from termforum.utils.ascii_art import create_banner
from pathlib import Path

# Initialize database
db_path = str(Path.home() / ".termforum" / "forum.db")
db = Database(db_path)

print(create_banner("TERMFORUM"))
print("Creating test data...\n")

# Get admin user
admin = db.get_user_by_username("yossi")
if not admin:
    print("Error: Admin user not found!")
    exit(1)

# Create some test users
print("Creating users...")
users = []
for name in ["alice", "bob", "charlie", "dave"]:
    try:
        user = db.create_user(name, avatar="👨‍💻" if name != "alice" else "👩‍💻")
        users.append(user)
        print(f"  ✓ Created user: {user.display_name}")
    except Exception as e:
        print(f"  ✗ User {name} might already exist")
        user = db.get_user_by_username(name)
        if user:
            users.append(user)

# Get categories
categories = db.list_categories()
print(f"\n✓ Found {len(categories)} categories")

# Create test threads
print("\nCreating threads...")
threads_data = [
    {
        "title": "Welcome to TermForum!",
        "content": """# Welcome! 🎉

This is **TermForum** - a beautiful terminal-based forum application.

## Features:
- 📋 Threads & Posts
- 🎨 Markdown Support
- 📁 Categories
- 🔍 Search
- ⬆️ Voting System

Feel free to explore and create your own threads!
""",
        "category": "Announcements",
        "user": admin
    },
    {
        "title": "How to use Markdown?",
        "content": """## Markdown Guide

Here's a quick guide to Markdown syntax:

### Headings
```
# H1
## H2
### H3
```

### Text Formatting
- **Bold**: `**bold**`
- *Italic*: `*italic*`
- `Code`: `` `code` ``

### Lists
- Item 1
- Item 2
- Item 3

### Code Blocks
\`\`\`python
def hello():
    print("Hello, TermForum!")
\`\`\`

Enjoy writing!
""",
        "category": "General",
        "user": users[0] if users else admin
    },
    {
        "title": "Need help with installation",
        "content": """I'm trying to install TermForum but running into some issues.

Can someone help me with the installation process?

Thanks!
""",
        "category": "Support",
        "user": users[1] if len(users) > 1 else admin
    },
    {
        "title": "Random thoughts...",
        "content": """Just wanted to share some random thoughts about terminal applications.

I love how **fast** and **lightweight** they are compared to GUI apps!

What do you think?
""",
        "category": "Off-Topic",
        "user": users[2] if len(users) > 2 else admin
    },
]

threads = []
for thread_data in threads_data:
    # Find category
    category = next((c for c in categories if c.name == thread_data["category"]), categories[0])

    thread = db.create_thread(
        title=thread_data["title"],
        content=thread_data["content"],
        user_id=thread_data["user"].id,
        category_id=category.id
    )
    threads.append(thread)
    print(f"  ✓ Created thread: {thread.title}")

# Create some replies
print("\nCreating replies...")
replies_data = [
    {
        "thread": 0,
        "user": users[0] if users else admin,
        "content": "Thanks for creating this forum! Looks amazing! 🎉"
    },
    {
        "thread": 0,
        "user": users[1] if len(users) > 1 else admin,
        "content": "I agree! This is exactly what I was looking for."
    },
    {
        "thread": 1,
        "user": users[2] if len(users) > 2 else admin,
        "content": "Great guide! Very helpful for beginners."
    },
    {
        "thread": 2,
        "user": admin,
        "content": "Sure! What error message are you getting?\n\nPlease share more details about your system."
    },
    {
        "thread": 3,
        "user": users[0] if users else admin,
        "content": "Totally agree! Terminal apps are the best! 💻"
    },
]

for reply_data in replies_data:
    if reply_data["thread"] < len(threads):
        thread = threads[reply_data["thread"]]
        post = db.create_post(
            thread_id=thread.id,
            user_id=reply_data["user"].id,
            content=reply_data["content"]
        )
        print(f"  ✓ Created reply in: {thread.title}")

# Show final stats
print("\n" + "="*60)
stats = db.get_forum_stats()
print("📊 Forum Statistics:")
print(f"  👥 Users:      {stats['users']}")
print(f"  📁 Categories: {stats['categories']}")
print(f"  📋 Threads:    {stats['threads']}")
print(f"  💬 Posts:      {stats['posts']}")
print("="*60)

print("\n✅ Test data created successfully!")
print("\nRun: python -m termforum.main run -u yossi")
