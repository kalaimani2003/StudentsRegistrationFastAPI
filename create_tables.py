from app.database.connection import Base, engine
from app.models import student_model  # import all model files here

# Create all tables in the DB
print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully.")
