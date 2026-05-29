import os
import threading
from flask import Flask
import config.config as config
import web.telegram as telegram
from coordinator import coordinator as coordinator

# 1. On crée un mini serveur web pour faire plaisir à Render
app = Flask('')

@app.route('/')
def home():
    return "Le robot Mercari tourne parfaitement !"

def run_web_server():
    # Render donne automatiquement un port dans les variables d'environnement
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. On lance le robot Mercari normal
def run_bot():
    print('Starting mercari-watchdog...')
    cfg = config.load()
    telegram_client = telegram.new_telegram_client(cfg.telegram_token, cfg.telegram_chat_id, False)
    simple_msg = "Nouveau produit trouve : {title} - {price}Yen - {url}"
    coordinator.start(cfg.searches, cfg.delay, simple_msg, cfg.change_rate, telegram_client)
    
if __name__ == "__main__":
    # On lance le serveur web dans un fil secondaire pour que Render reste content
    t = threading.Thread(target=run_web_server)
    t.start()
    
    # On lance ton robot principal
    run_bot()
