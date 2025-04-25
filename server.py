from flask import Flask, request
from threading import Thread

app = Flask(__name__)

visit_count = 0
bot_status = "En ligne"

@app.route('/', methods=['GET', 'POST'])
def home():
    global visit_count
    visit_count += 1

    username = ""
    if request.method == 'POST':
        username = request.form.get('username')

    return f'''
    <html>
      <head>
        <title>CF Games Bot</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
          }}
          p {{
            font-size: 24px;
          }}
          a {{
            font-size: 20px;
            color: #007bff;
            text-decoration: none;
          }}
          a:hover {{
            text-decoration: underline;
          }}
          .dark-theme {{
            background-color: #333;
            color: white;
          }}
        </style>
      </head>
      <body>
        <h1>CF Games Bot</h1>
        <p>Bot Discord open-source</p>
        <p><strong>Le bot est actuellement fonctionnel, version 1</strong></p>
        <p>Statut du bot : <strong>{bot_status}</strong></p>
        <p>Visites : {visit_count}</p>
        <p><br><br><br></p>
        
        <form method="POST" action="/">
          <input type="text" name="username" placeholder="Entrez votre pseudo" />
          <input type="submit" value="Envoyer" />
        </form>

        <p>{'Bienvenue, ' + username + '!' if username else ''}</p>

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

    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
