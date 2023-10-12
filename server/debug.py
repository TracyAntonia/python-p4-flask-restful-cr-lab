#!/usr/bin/env python3

from app import app, db 
from models import Plant

if __name__ == '__main__':
    with app.app_context():
        # You can access your Flask app and database here
        plants = Plant.query.all()
        print("All Plants:")
        for plant in plants:
            print(f"Name: {plant.name}, Image: {plant.image}, Price: {plant.price}")
        
        # Debugging session
        import ipdb; ipdb.set_trace()
