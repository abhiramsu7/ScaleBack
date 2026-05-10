# scaleback/models.py
import reflex as rx
from datetime import datetime

class UserConfig(rx.Model): # <--- Removed table=True
    """Static user profile for background calculations."""
    name: str 
    age: int
    height_cm: float
    weight_kg: float
    gender: str 
    activity_multiplier: float 

class FoodLog(rx.Model): # <--- Removed table=True
    """Tracks nutritional intake via AI NLP parsing."""
    user_id: int 
    raw_input: str
    calories: int
    protein: int
    carbs: int
    fats: int
    created_at: datetime = datetime.now()