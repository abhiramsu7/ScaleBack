# rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="scaleback",
    db_url="sqlite:///reflex.db", # We will change this to Supabase later!
)