"""Main entry point for TermForum"""

import click
from pathlib import Path
from .app import TermForumApp
from .storage import Database
from .utils import glow_available


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """TermForum - A beautiful TUI forum application"""
    pass


@cli.command()
@click.option("--db", default=None, help="Path to database file")
@click.option("--username", "-u", default=None, help="Login username")
def run(db, username):
    """Run TermForum application"""

    # Check if Glow is available
    if not glow_available():
        click.echo("⚠️  Warning: Glow not found. Markdown rendering will be limited.")
        click.echo("   Install with: pkg install glow (Termux) or brew install glow (macOS)")
        click.echo()

    # Initialize database
    if db is None:
        db = str(Path.home() / ".termforum" / "forum.db")

    database = Database(db)

    # Handle login/registration
    if username:
        user = database.get_user_by_username(username)
        if not user:
            click.echo(f"Creating new user: {username}")
            user = database.create_user(username)
    else:
        # Interactive login
        username = click.prompt("Enter your username", type=str)
        user = database.get_user_by_username(username)

        if not user:
            if click.confirm(f"User '{username}' not found. Create new account?"):
                user = database.create_user(username)
            else:
                click.echo("Login cancelled.")
                return

    # Run the app
    app = TermForumApp(database=database, current_user=user)
    app.run()


@cli.command()
@click.option("--db", default=None, help="Path to database file")
def init(db):
    """Initialize a new forum database"""
    if db is None:
        db = str(Path.home() / ".termforum" / "forum.db")

    db_path = Path(db)

    if db_path.exists():
        if not click.confirm(f"Database already exists at {db}. Recreate?"):
            click.echo("Initialization cancelled.")
            return
        db_path.unlink()

    click.echo(f"Creating new database at: {db}")
    database = Database(db)

    # Create admin user
    admin_username = click.prompt("Admin username", default="admin")
    admin_user = database.create_user(admin_username, is_admin=True)

    click.echo(f"✓ Database initialized successfully!")
    click.echo(f"✓ Admin user created: {admin_username}")
    click.echo(f"✓ Default categories created")

    stats = database.get_forum_stats()
    click.echo(f"\nForum stats:")
    click.echo(f"  Users: {stats['users']}")
    click.echo(f"  Categories: {stats['categories']}")
    click.echo(f"  Threads: {stats['threads']}")
    click.echo(f"  Posts: {stats['posts']}")


@cli.command()
@click.option("--db", default=None, help="Path to database file")
def stats(db):
    """Show forum statistics"""
    if db is None:
        db = str(Path.home() / ".termforum" / "forum.db")

    db_path = Path(db)
    if not db_path.exists():
        click.echo(f"Database not found at: {db}")
        click.echo("Run 'termforum init' to create a new database.")
        return

    database = Database(db)
    stats = database.get_forum_stats()

    click.echo("📊 Forum Statistics")
    click.echo("=" * 40)
    click.echo(f"👥 Users:      {stats['users']}")
    click.echo(f"📁 Categories: {stats['categories']}")
    click.echo(f"📋 Threads:    {stats['threads']}")
    click.echo(f"💬 Posts:      {stats['posts']}")
    click.echo(f"📝 Total:      {stats['total_content']}")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
