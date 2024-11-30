from app.extensions import Config

def conditional_print(message):
    if Config.ENABLE_PRINTS:
        print(f" * {message}")