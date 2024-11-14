# color_themes.py

def get_categorical_colors(theme_name="theme1"):
    themes = {
        "theme1": ["#FF5733", "#33FF57", "#3357FF", "#F39C12", "#8E44AD"],
        "theme2": ["#4B0082", "#FFD700", "#ADFF2F", "#00CED1", "#FF4500"]
    }
    return themes.get(theme_name, themes["theme1"])

def get_continuous_colors(gradient_name="warm_gradient"):
    gradients = {
        "warm_gradient": ["#FFFFFF", "#FF7F50", "#FF4500"],
        "cool_gradient": ["#E0FFFF", "#00CED1", "#1E90FF"]
    }
    return gradients.get(gradient_name, gradients["warm_gradient"])
