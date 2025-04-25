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
            /* Style général du footer */
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                text-align: center;
                background-color: #f1f1f1;
                padding: 20px;
            }

            .cf-games h1 {
                font-size: 36px;
                margin-bottom: 10px;
            }

            .cf-games p {
                font-size: 14px;
                color: #555;
            }

            .site-info p {
                font-size: 12px;
                margin-bottom: 10px;
            }

            /* Style du bouton */
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #45a049;
            }

            /* Style de la fenêtre modale */
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.4);
                padding-top: 60px;
            }

            .modal-content {
                background-color: #fefefe;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
                max-width: 600px;
            }

            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }

            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <!-- Ton contenu principal ici -->

        <div class="footer">
            <div class="cf-games">
                <h1>CF GAMES</h1>
                <p>CF Games est le créateur de Créatif France et de Best Survie, deux serveurs MultiCraft. Je code aussi un bot Discord open source sur GitHub.</p>
            </div>
            
            <div class="site-info">
                <p>Ce site est un blog perso, sans collecte de données, sans pubs et sans but commercial.</p>
                <button id="info-btn">Infos sur le site</button>
            </div>

            <div id="legal-modal" class="modal">
                <div class="modal-content">
                    <span id="close-btn" class="close">&times;</span>
                    <h2>Mentions légales</h2>
                    <p><strong>Éditeur :</strong><br>CF GAMES (pseudo)<br>Email : creatif.france@outlook.com</p>
                    <p><strong>Hébergeur :</strong><br>Render Services, Inc.<br>525 Brannan St Ste 300, San Francisco, CA 94107, USA<br>Tél : +1 415 830 4762<br>Email : abuse@render.com</p>
                    <p><strong>GitHub :</strong><br><a href="https://github.com/Creatif-France-Games/cf-games-bot" target="_blank">cf-games-bot</a></p>
                    <p><strong>Responsabilité :</strong><br>L’éditeur s’efforce d’être exact, mais ne peut être tenu pour responsable des erreurs ou omissions.</p>
                </div>
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
    """Lance le petit serveur Flask en arrière-plan."""
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    # Si tu veux juste lancer le serveur web seul :
    run()