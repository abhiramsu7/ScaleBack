# scaleback/scaleback.py
import reflex as rx
from scaleback.model import FoodLog
from scaleback.geminibackend import analyze_meal

class AppState(rx.State):
    """The state holds the variables that change in your app."""
    user_input: str = ""
    is_loading: bool = False
    daily_calories_consumed: int = 0
    daily_goal: int = 2000 

    # 🛠️ THE FIX: We explicitly create the setter function here
    def update_text(self, text: str):
        self.user_input = text

    def log_food(self):
        """Fires when the user hits 'Enter' or clicks Log."""
        if not self.user_input:
            return

        self.is_loading = True
        yield 

        # Send the text to the Gemini Brain
        macro_data = analyze_meal(self.user_input)

        # Extract the calories (default to 0 if something fails)
        calories = macro_data.get("calories", 0)

        # Update the app state
        self.daily_calories_consumed += calories
        self.user_input = "" 
        self.is_loading = False


def index() -> rx.Component:
    """The main Dashboard UI."""
    return rx.center(
        rx.vstack(
            rx.heading("ScaleBack", size="8", color="white"),
            
            rx.text(
                f"{AppState.daily_goal - AppState.daily_calories_consumed} kcal remaining", 
                color="gray", 
                size="4"
            ),

            # 🛠️ THE FIX: Update the on_change right here
            rx.input(
                placeholder="What did you eat? (e.g., 2 rotis and paneer)",
                value=AppState.user_input,
                on_change=AppState.update_text,  # <--- Changed this line
                width="100%",
                bg="#1e1e1e", 
                color="white",
                border="1px solid #333"
            ),
            
            rx.button(
                "Log Meal",
                on_click=AppState.log_food,
                loading=AppState.is_loading,
                width="100%",
                color_scheme="gray"
            ),
            
            spacing="4",
            width="100%",
            max_width="400px",
            padding="20px",
            align_items="center",
        ),
        bg="black", 
        min_height="100vh",
    )

app = rx.App()
app.add_page(index, title="ScaleBack - Zero Bloat")