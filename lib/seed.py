#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie 

# Create Companies
apple = Company(name="Apple", founding_year=1976)
amazon = Company(name="Amazon", founding_year=1994)
facebook = Company(name="Facebook", founding_year=2004)

# Create Devs
alice = Dev(name="Alice")
bob = Dev(name="Bob")
charlie = Dev(name="Charlie")

# Create Freebies
freebie1 = Freebie(
    item_name="Headphones",
    value=180,
    company=amazon,
    dev=bob
)

freebie2 = Freebie(
    item_name="T-shirt",
    value=120,
    company=apple,
    dev=charlie
)

freebie3 = Freebie(
    item_name="Laptop",
    value=1000,
    company=facebook,
    dev=alice
)

freebie4 = Freebie(
    item_name="Sticker Pack",
    value=30,
    company=amazon,
    dev=charlie
)

# Database connection
engine = create_engine('sqlite:///freebies.db')  
Session = sessionmaker(bind=engine)
session = Session()

# Save to database
session.add_all([
    apple, amazon, facebook,
    alice, bob, charlie,
    freebie1, freebie2, freebie3, freebie4
])

session.commit()
