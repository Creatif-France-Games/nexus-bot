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
        <!-- Favicon via lien URL -->
        <link rel="icon" href="https://private-user-images.githubusercontent.com/207845454/437530336-54a16db6-dda0-4c9c-9797-d81b469fb46b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDU2MDA5MTIsIm5iZiI6MTc0NTYwMDYxMiwicGF0aCI6Ii8yMDc4NDU0NTQvNDM3NTMwMzM2LTU0YTE2ZGI2LWRkYTAtNGM5Yy05Nzk3LWQ4MWI0NjlmYjQ2Yi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNDI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDQyNVQxNzAzMzJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iMDA3NTY2MzViMmYzMzM1YWM1MTM1M2YyMThmMDE3NzcyNGUyNTEwOTIzNGFjM2NiMWI4YjU5NDQyNjhiOGY1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.YgY5g6P0njjSyDDza5efHov7tGWP2NJgbf5IbgyQpRs">
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
            background-color: #000; /* Fond noir */
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

          /* Accessibilité */
          .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            margin: -1px;
            padding: 0;
            border: 0;
            clip: rect(0, 0, 0, 0);
            overflow: hidden;
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

        <p><a href="https://github.com/Creatif-France-Games/cf-games-bot" target="_blank" aria-label="Voir le code source du bot">Code source : https://github.com/Creatif-France-Games/cf-games-bot</a></p>

        <!-- Ajout d'un message d'accessibilité -->
        <p class="sr-only">Cette page affiche le statut du bot en ligne. Vous pouvez voir le code source du projet sur GitHub.</p>
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

    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
