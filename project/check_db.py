#!/usr/bin/env python3
"""
Check database content
"""

import sqlite3
import json

def check_database():
    conn = sqlite3.connect('empowerverse_demo.db')
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Users in database: {user_count}")
    
    if user_count > 0:
        cursor.execute("SELECT username, first_name, last_name, user_type FROM users LIMIT 3")
        users = cursor.fetchall()
        print("Sample users:")
        for user in users:
            print(f"  - {user[1]} {user[2]} (@{user[0]}) - {user[3]}")
    
    # Check posts table
    cursor.execute("SELECT COUNT(*) FROM posts")
    post_count = cursor.fetchone()[0]
    print(f"\nPosts in database: {post_count}")
    
    if post_count > 0:
        cursor.execute("SELECT title, view_count, upvote_count FROM posts LIMIT 3")
        posts = cursor.fetchall()
        print("Sample posts:")
        for post in posts:
            print(f"  - \"{post[0]}\" - {post[1]} views, {post[2]} upvotes")
    
    # Check categories table
    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]
    print(f"\nCategories in database: {category_count}")
    
    if category_count > 0:
        cursor.execute("SELECT name, description FROM categories LIMIT 3")
        categories = cursor.fetchall()
        print("Sample categories:")
        for cat in categories:
            print(f"  - {cat[0]}: {cat[1]}")
    
    conn.close()

if __name__ == "__main__":
    check_database()