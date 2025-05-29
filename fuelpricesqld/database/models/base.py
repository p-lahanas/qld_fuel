# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Create an SQLite database engine; replace with your database URL
engine = create_engine(
    'postgresql://username:password@localhost:5432/default_database', echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a model class that inherits from Base


class User(Base):
    __tablename__ = 'users'  # Define the name of the table

    id = Column(Integer, primary_key=True)  # Define the primary key column
    name = Column(String)  # Define a regular column
    age = Column(Integer)  # Define another column


# Create a session factory
Session = sessionmaker(bind=engine)

# Create the tables in the database
Base.metadata.create_all(engine)
