"""Update database with new categories for developers"""

from termforum.storage import Database
from pathlib import Path

db_path = str(Path.home() / ".termforum" / "forum.db")
db = Database(db_path)

print("🔄 Updating categories for TermForum Ultimate...\n")

# New categories for developers, hackers, and security researchers
new_categories = [
    {
        "name": "Programming",
        "slug": "programming",
        "description": "Python, JavaScript, Go, Rust, C++ and more",
        "icon": "💻",
        "color": "#3B82F6",
        "position": 10
    },
    {
        "name": "Security & Hacking",
        "slug": "security-hacking",
        "description": "Pentesting, CTF, Exploits, Tools",
        "icon": "🔐",
        "color": "#EF4444",
        "position": 11
    },
    {
        "name": "AI & Machine Learning",
        "slug": "ai-ml",
        "description": "LLMs, Ollama, RAG, Training, Fine-tuning",
        "icon": "🤖",
        "color": "#8B5CF6",
        "position": 12
    },
    {
        "name": "Web Development",
        "slug": "web-dev",
        "description": "Frontend, Backend, APIs, Security",
        "icon": "🌐",
        "color": "#10B981",
        "position": 13
    },
    {
        "name": "Linux & Terminal",
        "slug": "linux-terminal",
        "description": "Termux, Shell, Automation, CLI Tools",
        "icon": "🐧",
        "color": "#F59E0B",
        "position": 14
    },
    {
        "name": "Mobile Development",
        "slug": "mobile-dev",
        "description": "Android, iOS, React Native, Flutter",
        "icon": "📱",
        "color": "#EC4899",
        "position": 15
    },
    {
        "name": "Cloud & DevOps",
        "slug": "cloud-devops",
        "description": "AWS, Docker, Kubernetes, CI/CD",
        "icon": "☁️",
        "color": "#06B6D4",
        "position": 16
    },
    {
        "name": "Game Development",
        "slug": "game-dev",
        "description": "Unity, Unreal, Godot, Mods",
        "icon": "🎮",
        "color": "#A855F7",
        "position": 17
    },
    {
        "name": "Resources & Tutorials",
        "slug": "resources",
        "description": "Cheat sheets, Guides, Scripts",
        "icon": "📚",
        "color": "#14B8A6",
        "position": 18
    },
]

for cat_data in new_categories:
    try:
        # Check if already exists by checking all categories
        existing_cats = db.list_categories()
        exists = any(c.slug == cat_data["slug"] for c in existing_cats)

        if exists:
            print(f"  ⏭️  {cat_data['icon']} {cat_data['name']} - Already exists")
        else:
            cat = db.create_category(**cat_data)
            print(f"  ✅ {cat.icon} {cat.name} - Created")
    except Exception as e:
        print(f"  ❌ {cat_data['name']} - Error: {e}")

print("\n📊 Category Summary:")
categories = db.list_categories()
for cat in categories:
    print(f"  {cat.icon} {cat.name} ({cat.threads_count} threads)")

print(f"\n✅ Total categories: {len(categories)}")
print("🎉 Categories updated successfully!")
