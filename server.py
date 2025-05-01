from flask import Flask, render_template_string
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CF GAMES</title>
        <style>
            body {
                background-color: #000;
                color: #fff;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }

            .content {
                padding: 40px 20px 100px;
                text-align: center;
            }

            h1 {
                font-size: 36px;
                margin-bottom: 10px;
            }

            h2 {
                font-size: 24px;
                margin-top: 40px;
            }

            p, a {
                font-size: 14px;
                color: #ddd;
                line-height: 1.6;
            }

            a {
                color: #4CAF50;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }

            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
            }

            button:hover {
                background-color: #45a049;
            }

            .footer {
                background-color: #111;
                text-align: center;
                padding: 20px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }

            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                padding-top: 60px;
            }

            .modal-content {
                background-color: #222;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
                max-width: 600px;
                color: white;
            }

            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }

            .close:hover,
            .close:focus {
                color: white;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <h1>CF GAMES</h1>
            <p>CF Games est le créateur de Créatif France et de Best Survie, deux serveurs MultiCraft. Je code aussi un bot Discord open source sur GitHub.</p>
            <p>Ce site est un blog perso, sans collecte de données, sans pubs et sans but commercial.</p>
            <p>GitHub : <a href="https://www.github.com/Creatif-France-Games/cf-games-bot/" target="_blank">cf-games-bot</a></p>

            <h2>Discord</h2>
            <a href="https://discord.gg/Zzcb9j8BTJ" target="_blank">
                <button>Rejoindre le serveur</button>
            </a>
            <p>Bot : en ligne</p>

            <h2>Serveurs MultiCraft</h2>
            <p>Best Survie : serveur PVP avec clan, expérience de survie avec système d'économie et deux niveaux de jeu. Code d'invitation : X72KP62P<p>
            <p>Créatif France : build libre sur un grand serveur. Code d'invitation : 432IBSK4.</p>
        </div>

        <div class="footer">
            <button id="info-btn">Mentions légales</button>
        </div>

        <div id="legal-modal" class="modal">
            <div class="modal-content">
                <span id="close-btn" class="close">&times;</span>
                <h2>Mentions légales</h2>
                <p><strong>Éditeur :</strong><br>CF GAMES (pseudo)<br>Email : creatif.france@outlook.com</p>
                <p><strong>Hébergeur :</strong><br>Render Services, Inc.<br>525 Brannan St Ste 300, San Francisco, CA 94107, USA<br>Tél : +1 415 830 4762<br>Email : abuse@render.com</p>
                <p><strong>GitHub :</strong><br><a href="https://www.github.com/Creatif-France-Games/cf-games-bot/" target="_blank">cf-games-bot</a></p>
                <p><strong>Responsabilité :</strong><br>L’éditeur s’efforce d’être exact, mais ne peut être tenu pour responsable des erreurs ou omissions.</p>
            </div>
        </div>

        <script>
            const modal = document.getElementById("legal-modal");
            document.getElementById("info-btn").onclick = () => modal.style.display = "block";
            document.getElementById("close-btn").onclick = () => modal.style.display = "none";
            window.onclick = e => { if (e.target == modal) modal.style.display = "none"; };
        </script>
    </body>
    </html>
    """)

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    run()
