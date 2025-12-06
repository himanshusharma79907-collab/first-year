
import sqlite3

DB_NAME = "watchlist.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL,
            rating REAL,
            platform TEXT,
            review TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_title():
    print("\n--- Add New Title ---")
    title = input("Title name          : ").strip()
    type_ = input("Type (Movie/Anime)  : ").strip()
    status = input("Status (Watching/Completed/Plan to watch/Dropped): ").strip()
    platform = input("Platform (optional) : ").strip()
    rating_input = input("Rating 0-10 (optional, press Enter to skip): ").strip()
    review = input("Short review (optional): ").strip()

    rating = float(rating_input) if rating_input else None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO watchlist (title, type, status, rating, platform, review)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, type_, status, rating, platform, review))
    conn.commit()
    conn.close()
    print("✔ Added to watchlist!")

def show_all():
    print("\n--- Full Watchlist ---")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, type, status, rating, platform FROM watchlist")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No titles found.")
        return

    for row in rows:
        id_, title, type_, status, rating, platform = row
        print(f"[{id_}] {title} ({type_}) | {status} | Rating: {rating if rating is not None else '-'} | {platform or '-'}")

def show_by_status():
    status = input("\nEnter status to filter (Watching/Completed/Plan to watch/Dropped): ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT id, title, type, status, rating, platform
        FROM watchlist WHERE status = ?""", (status,))
    rows = cur.fetchall()
    conn.close()

    print(f"\n--- Titles with status: {status} ---")
    if not rows:
        print("No titles found.")
        return

    for row in rows:
        id_, title, type_, status, rating, platform = row
        print(f"[{id_}] {title} ({type_}) | Rating: {rating if rating is not None else '-'} | {platform or '-'}")

def update_status_rating():
    print("\n--- Update Status / Rating ---")
    try:
        id_ = int(input("Enter ID of title to update: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, status, rating FROM watchlist WHERE id = ?", (id_,))
    row = cur.fetchone()

    if not row:
        print("❌ No title found with that ID.")
        conn.close()
        return

    print(f"Current -> Title: {row[1]}, Status: {row[2]}, Rating: {row[3]}")
    new_status = input("New status (press Enter to keep same): ").strip()
    new_rating_input = input("New rating 0-10 (press Enter to keep same): ").strip()

    if not new_status:
        new_status = row[2]

    if new_rating_input:
        try:
            new_rating = float(new_rating_input)
        except ValueError:
            print("❌ Invalid rating. Keeping old rating.")
            new_rating = row[3]
    else:
        new_rating = row[3]

    cur.execute("UPDATE watchlist SET status = ?, rating = ? WHERE id = ?",
                (new_status, new_rating, id_))
    conn.commit()
    conn.close()
    print("✔ Updated successfully!")

def main():
    create_table()
    while True:
        print("\n=== Movie / Anime Watchlist ===")
        print("1. Add new title")
        print("2. Show full watchlist")
        print("3. Show by status")
        print("4. Update status/rating")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_title()
        elif choice == "2":
            show_all()
        elif choice == "3":
            show_by_status()
        elif choice == "4":
            update_status_rating()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
