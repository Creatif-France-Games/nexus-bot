from flask import Flask, render_template_string, send_from_directory
from threading import Thread
import os

app = Flask(__name__)

# Route pour le favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CF GAMES</title>
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
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
            
            <h2>Discord</h2>
            <a href="https://discord.gg/Zzcb9j8BTJ" target="_blank">
                <button>Rejoindre le serveur</button>
            </a>
            <p>Bot : en ligne</p>

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
