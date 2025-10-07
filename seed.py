from app import app, db

def create_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("- users")
        print("- recipes")
        print("- favorites")
        print("- ratings")
        print("\nYou can now run the Flask app with: python app.py")

if __name__ == '__main__':
    create_database()