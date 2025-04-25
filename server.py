from flask import Flask, render_template_string

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

        <!-- Section de bas de page -->
        <div class="footer">
            <div class="cf-games">
                <h1>CF GAMES</h1>
                <p>CF Games est le créateur de Créatif France et de Best Survie, deux serveurs MultiCraft. De plus, je code un bot discord open source dispo sur GitHub.</p>
            </div>
            
            <div class="site-info">
                <p>Ce site est un blog personnel. Il ne collecte aucune donnée personnelle, ne contient aucune publicité, et n’a aucun but commercial.</p>
                <button id="info-btn">Infos sur le site</button>
            </div>

            <!-- Fenêtre modale pour afficher les mentions légales -->
            <div id="legal-modal" class="modal">
                <div class="modal-content">
                    <span id="close-btn" class="close">&times;</span>
                    <h2>Mentions légales</h2>
                    <p><strong>Éditeur du site :</strong><br>CF GAMES (pseudo)<br>Email : creatif.france@outlook.com</p>
                    <p><strong>Hébergeur :</strong><br>Render Services, Inc.<br>Adresse : 525 Brannan Street Ste 300, San Francisco, CA 94107, États-Unis<br>Téléphone : +1 415 830 4762<br>Email : abuse@render.com</p>
                    <p><strong>GitHub :</strong><br><a href="https://github.com/Creatif-France-Games/cf-games-bot" target="_blank">https://github.com/Creatif-France-Games/cf-games-bot</a></p>
                    <p><strong>Responsabilité :</strong><br>L’éditeur s’efforce d’assurer l’exactitude des informations publiées, mais ne saurait être tenu responsable des erreurs ou omissions. Les liens externes sont fournis à titre informatif et n’engagent pas la responsabilité de l’éditeur.</p>
                </div>
            </div>
        </div>

        <script>
            // Récupère les éléments nécessaires
            var modal = document.getElementById("legal-modal");
            var btn = document.getElementById("info-btn");
            var span = document.getElementById("close-btn");

            // Lorsque l'utilisateur clique sur le bouton, ouvre la modale
            btn.onclick = function() {
                modal.style.display = "block";
            }

            // Lorsque l'utilisateur clique sur (x), ferme la modale
            span.onclick = function() {
                modal.style.display = "none";
            }

            // Lorsque l'utilisateur clique n'importe où en dehors de la modale, la ferme
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)