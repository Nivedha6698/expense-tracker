from app import create_app, db

# Use production config
app = create_app("prod")

with app.app_context():
    # Import ALL models so SQLAlchemy knows them
    from app.models import User, Expense

    db.create_all()
    print("✅ Tables created successfully")