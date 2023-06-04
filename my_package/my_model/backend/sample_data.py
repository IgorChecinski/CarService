from backend.database import SessionLocal
from backend.models import User, Comment

# Create a database session
db = SessionLocal()

# Create sample users
user1 = User( name = "Tomasz")
user2 = User( name = "Bartosz")

# Create sample comments
comment1 = Comment(content="Good Service", commentator=user1)
comment2 = Comment(content="Rude employee", commentator=user2)

# Add the objects to the session
db.add(user1)
db.add(user2)
db.add(comment1)
db.add(comment2)

# Commit the changes to the database
db.commit()

# Close the session
db.close()
