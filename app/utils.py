from config import Config

def conditional_print(message):
    if Config.ENABLE_PRINTS:
        print(message)
