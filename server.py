from flask import Flask
from threading import Thread

app = Flask(__name__)

# Le statut du bot sera toujours "En ligne"
bot_status = "En ligne"

@app.route('/', methods=['GET'])
def home():
    return f'''
    <html>
      <head>
        <title>CF Games Bot</title>
        <style>
          /* Style global */
          * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
          }}

          /* Mise en forme du corps de la page */
          body {{
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 18px;
            margin-top: 50px;
          }}

          h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
          }}

          p {{
            font-size: 1.2rem;
            margin-bottom: 15px;
          }}

          a {{
            color: #007bff;
            font-size: 1.1rem;
            text-decoration: none;
          }}

          a:hover {{
            text-decoration: underline;
          }}

          /* Responsiveness */
          @media (max-width: 768px) {{
            body {{
              font-size: 16px;
            }}
            h1 {{
              font-size: 2.5rem;
            }}
          }}

          @media (max-width: 480px) {{
            body {{
              font-size: 14px;
            }}
            h1 {{
              font-size: 2rem;
            }}
          }}
        </style>
      </head>
      <body>
        <h1>CF Games Bot</h1>
        <p>Bot Discord open-source</p>
        <p><strong>Le bot est actuellement fonctionnel, version 1</strong></p>
        <p>Statut du bot : <strong>{bot_status}</strong></p>

        <p><a href="https://github.com/Creatif-France-Games/cf-games-bot" target="_blank">
          Code source : https://github.com/Creatif-France-Games/cf-games-bot
        </a></p>
      </body>
    </html>
    '''

# Fonction pour démarrer Flask dans un thread
def run():
    app.run(host='0.0.0.0', port=8080)

# Fonction keep_alive pour lancer le serveur dans un thread séparé
def keep_alive():
    t = Thread(target=run)
    t.start()

# Appel de la fonction keep_alive pour démarrer le serveur
if __name__ == "__main__":
    keep_alive()


    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
