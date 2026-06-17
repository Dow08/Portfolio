from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
from functools import lru_cache
from urllib.parse import urlparse
import bcrypt
import json
import os
import re
import boto3
from dotenv import load_dotenv
import pymysql

load_dotenv()

# ---------------------------------------------------------------------------
# SECRETS - récupérés depuis AWS Secrets Manager (jamais en dur dans le code)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_secret():
    """Charge le secret JSON (db + secret_key) depuis Secrets Manager.

    Mis en cache : un seul appel réseau pour toute la durée de vie du process.
    """
    secret_arn = os.environ.get("SECRET_ARN")
    if not secret_arn:
        return {}
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "eu-west-3"))
    response = client.get_secret_value(SecretId=secret_arn)
    return json.loads(response["SecretString"])


def get_secret_key():
    """Clé de signature des cookies Flask (F6/F8).

    Priorité : Secrets Manager > variable d'environnement. Aucune valeur par
    défaut triviale : on échoue volontairement plutôt que de signer les sessions
    avec une clé devinable (qui permettrait la forge de cookies).
    """
    key = _load_secret().get("secret_key") or os.environ.get("SECRET_KEY")
    if not key:
        raise RuntimeError(
            "SECRET_KEY absente. Fournir une clé forte et persistante via "
            "Secrets Manager (champ 'secret_key') ou la variable SECRET_KEY."
        )
    return key


app = Flask(__name__)
app.secret_key = get_secret_key()
app.permanent_session_lifetime = timedelta(days=7)

# Derrière Cloudflare (TLS) + ALB : on reconstruit le schéma https et l'IP
# cliente réelle à partir des en-têtes X-Forwarded-*. Indispensable pour que
# le cookie Secure et l'en-tête HSTS soient cohérents.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Durcissement des cookies de session (F4)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,   # inaccessible au JavaScript (anti-vol XSS)
    SESSION_COOKIE_SECURE=True,     # transmis uniquement sur HTTPS (TLS Cloudflare)
    SESSION_COOKIE_SAMESITE="Lax",  # limite les attaques CSRF
)

# ---------------------------------------------------------------------------
# EN-TÊTES DE SÉCURITÉ HTTP (F3) + masquage de version serveur (F2)
# ---------------------------------------------------------------------------

@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    # Ne pas divulguer la pile applicative ni sa version
    response.headers["Server"] = "PixelStore"
    return response

# ---------------------------------------------------------------------------
# POLITIQUE DE MOT DE PASSE (F7) - inspirée NIST SP 800-63B
# ---------------------------------------------------------------------------

# Petite liste de mots de passe triviaux refusés d'office.
COMMON_PASSWORDS = {
    "password", "motdepasse", "azertyuiop", "qwertyuiop", "123456789012",
    "azerty123456", "password1234", "administrateur", "pixelstore12",
}

def validate_password(pw):
    """Retourne un message d'erreur si le mot de passe est trop faible, sinon None."""
    if len(pw) < 12:
        return "Le mot de passe doit contenir au moins 12 caractères."
    if not re.search(r"[a-z]", pw):
        return "Le mot de passe doit contenir au moins une minuscule."
    if not re.search(r"[A-Z]", pw):
        return "Le mot de passe doit contenir au moins une majuscule."
    if not re.search(r"[0-9]", pw):
        return "Le mot de passe doit contenir au moins un chiffre."
    if not re.search(r"[^A-Za-z0-9]", pw):
        return "Le mot de passe doit contenir au moins un caractère spécial."
    if pw.lower() in COMMON_PASSWORDS:
        return "Ce mot de passe est trop courant. Choisissez-en un autre."
    return None

# ---------------------------------------------------------------------------
# REDIRECTION SÛRE (anti Open Redirect / CWE-601)
# ---------------------------------------------------------------------------

def safe_redirect_target(target, fallback="/"):
    """N'autorise qu'une redirection vers un chemin INTERNE.

    Toute URL absolue (http://, //evil.com, etc.) est rejetée pour empêcher
    la redirection d'une victime vers un site de phishing depuis un lien
    PixelStore légitime.
    """
    if not target:
        return fallback
    parsed = urlparse(target)
    # Pas de schéma (http/https/...) ni de domaine (netloc) : chemin local seul.
    # Doit commencer par "/" mais pas par "//" (qui désigne un autre hôte).
    if parsed.scheme or parsed.netloc:
        return fallback
    if not target.startswith("/") or target.startswith("//"):
        return fallback
    return target

# ---------------------------------------------------------------------------
# CONFIG RDS via Secrets Manager
# ---------------------------------------------------------------------------

def get_db_credentials():
    creds = _load_secret()
    if creds:
        return {
            "host":     os.environ.get("DB_HOST"),
            "user":     creds["username"],
            "password": creds["password"],
            "database": creds["dbname"],
        }
    # Fallback local (dev)
    return {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "user":     os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", "password"),
        "database": os.environ.get("DB_NAME", "pixelstore_db"),
    }

def get_db():
    creds = get_db_credentials()
    return pymysql.connect(
        host=creds["host"],
        user=creds["user"],
        password=creds["password"],
        database=creds["database"],
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )

# ---------------------------------------------------------------------------
# INIT DB - tables + données produits
# ---------------------------------------------------------------------------

PRODUCTS_DATA = [
    (1, "Apple",   "iPhone 16 Pro Max", 1329, "L'iPhone le plus puissant jamais conçu. Puce A18 Pro, écran Super Retina XDR 6,9\", système de caméra pro avec zoom optique 5x et enregistrement vidéo 4K 120fps. Titane de qualité spatiale.", '{"Écran":"6,9\\" OLED 120Hz","Processeur":"A18 Pro","RAM":"8 Go","Stockage":"256 Go / 512 Go / 1 To","Batterie":"4685 mAh","OS":"iOS 18"}', "iphone16promax.jpg", "Nouveau",    "#1a1a2e"),
    (2, "Apple",   "iPhone 16 Pro",     1129, "Puissance pro dans un format compact. Puce A18 Pro, écran 6,3\" avec ProMotion 120Hz, triple caméra avec mode macro et bouton Action personnalisable.",                                          '{"Écran":"6,3\\" OLED 120Hz","Processeur":"A18 Pro","RAM":"8 Go","Stockage":"128 Go / 256 Go / 512 Go","Batterie":"3582 mAh","OS":"iOS 18"}', "iphone16pro.jpg",     "Nouveau",    "#1a1a2e"),
    (3, "Apple",   "iPhone 16",          869, "L'iPhone pour tout le monde. Puce A16 Bionic, magnifique écran 6,1\", système de double caméra et une autonomie toute la journée.",                                                              '{"Écran":"6,1\\" OLED 60Hz","Processeur":"A16 Bionic","RAM":"6 Go","Stockage":"128 Go / 256 Go / 512 Go","Batterie":"3279 mAh","OS":"iOS 18"}',  "iphone16.jpg",        None,         "#1a1a2e"),
    (4, "Samsung", "Galaxy S25 Ultra",  1449, "Le summum de l'innovation Samsung. S Pen intégré, capteur 200 MP, puce Snapdragon 8 Elite, écran Dynamic AMOLED 6,9\" et batterie 5000 mAh pour une autonomie exceptionnelle.",                '{"Écran":"6,9\\" AMOLED 120Hz","Processeur":"Snapdragon 8 Elite","RAM":"12 Go","Stockage":"256 Go / 512 Go / 1 To","Batterie":"5000 mAh","OS":"Android 15"}', "s25ultra.jpg",   "Best-seller", "#0d1b2a"),
    (5, "Samsung", "Galaxy S25+",       1119, "Grand écran, grande puissance. Le Galaxy S25+ offre un écran Dynamic AMOLED 6,7\", la puissance du Snapdragon 8 Elite et une recharge rapide 45W.",                                            '{"Écran":"6,7\\" AMOLED 120Hz","Processeur":"Snapdragon 8 Elite","RAM":"12 Go","Stockage":"256 Go / 512 Go","Batterie":"4900 mAh","OS":"Android 15"}',    "s25plus.jpg",    "Nouveau",     "#0d1b2a"),
    (6, "Samsung", "Galaxy Z Fold 6",   1899, "Le futur est pliable. Le Galaxy Z Fold 6 se transforme d'un smartphone compact en une tablette 7,6\". Multitâche avancé, S Pen compatible et charnière ultra-résistante.",                     '{"Écran":"7,6\\" AMOLED 120Hz (déplié)","Processeur":"Snapdragon 8 Gen 3","RAM":"12 Go","Stockage":"256 Go / 512 Go","Batterie":"4400 mAh","OS":"Android 14"}', "zfold6.jpg",  "Premium",     "#0d1b2a"),
    (7, "Google",  "Pixel 9 Pro XL",    1099, "L'IA au service de la photo. Le Pixel 9 Pro XL embarque Google Gemini Nano, le meilleur appareil photo Android avec Magic Eraser, et 7 ans de mises à jour garanties.",                        '{"Écran":"6,8\\" OLED 120Hz","Processeur":"Google Tensor G4","RAM":"16 Go","Stockage":"128 Go / 256 Go / 1 To","Batterie":"5060 mAh","OS":"Android 15"}',    "pixel9proxl.jpg","Nouveau",    "#1a2e1a"),
    (8, "Google",  "Pixel 9 Pro",        999, "Compact et ultra-puissant. Le Pixel 9 Pro combine la puissance de Gemini AI, un triple capteur photo et un design raffiné dans un format 6,3\" parfaitement maniable.",                         '{"Écran":"6,3\\" OLED 120Hz","Processeur":"Google Tensor G4","RAM":"16 Go","Stockage":"128 Go / 256 Go / 512 Go","Batterie":"4700 mAh","OS":"Android 15"}',   "pixel9pro.jpg",  None,         "#1a2e1a"),
    (9, "Google",  "Pixel 9",            799, "L'intelligence artificielle accessible à tous. Le Pixel 9 offre les fonctionnalités IA de Google, un superbe appareil photo et Android pur avec 7 ans de mises à jour.",                        '{"Écran":"6,3\\" OLED 60Hz","Processeur":"Google Tensor G4","RAM":"12 Go","Stockage":"128 Go / 256 Go","Batterie":"4700 mAh","OS":"Android 15"}',             "pixel9.jpg",     None,         "#1a2e1a"),
]

def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                email         VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                name          VARCHAR(100) NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                brand       VARCHAR(50)  NOT NULL,
                name        VARCHAR(100) NOT NULL,
                price       DECIMAL(10,2) NOT NULL,
                description TEXT,
                specs       JSON,
                image_url   VARCHAR(255),
                badge       VARCHAR(50),
                color       VARCHAR(20)
            )
        """)
        cursor.execute("SELECT COUNT(*) as cnt FROM products")
        if cursor.fetchone()["cnt"] == 0:
            for p in PRODUCTS_DATA:
                pid, brand, name, price, desc, specs, img, badge, color = p
                image_url = f"/static/img/{img}"
                cursor.execute("""
                    INSERT INTO products (id, brand, name, price, description, specs, image_url, badge, color)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (pid, brand, name, price, desc, specs, image_url, badge, color))
    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def get_product_by_id(product_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
    conn.close()
    if product and isinstance(product.get("specs"), str):
        product["specs"] = json.loads(product["specs"])
    return product

def get_all_products(brand_filter=None):
    conn = get_db()
    with conn.cursor() as cursor:
        if brand_filter and brand_filter != "tous":
            cursor.execute("SELECT * FROM products WHERE LOWER(brand) = %s ORDER BY id", (brand_filter.lower(),))
        else:
            cursor.execute("SELECT * FROM products ORDER BY id")
        products = cursor.fetchall()
    conn.close()
    for p in products:
        if isinstance(p.get("specs"), str):
            p["specs"] = json.loads(p["specs"])
    return products

def get_cart_details():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_product_by_id(int(pid))
        if product:
            subtotal = float(product["price"]) * qty
            total += subtotal
            items.append({**product, "qty": qty, "subtotal": subtotal})
    return items, total

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    brand_filter = request.args.get("brand", "tous")
    products = get_all_products(brand_filter)
    return render_template("index.html", products=products, active_filter=brand_filter)


@app.route("/product/<int:product_id>")
def product(product_id):
    p = get_product_by_id(product_id)
    if not p:
        return redirect(url_for("index"))
    return render_template("product.html", product=p)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("index"))

    error = None
    mode = request.args.get("mode", "login")

    if request.method == "POST":
        action      = request.form.get("action")
        email       = request.form.get("email", "").strip()
        password_str = request.form.get("password", "")
        password    = password_str.encode("utf-8")

        if action == "login":
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
            conn.close()
            if user and bcrypt.checkpw(password, user["password_hash"].encode("utf-8")):
                session.permanent = True
                session["user"] = {"email": user["email"], "name": user["name"]}
                return redirect(url_for("index"))
            else:
                error = "Email ou mot de passe incorrect."
                mode = "login"

        elif action == "register":
            confirm = request.form.get("confirm", "")
            name    = request.form.get("name", "").strip()
            pw_error = validate_password(password_str)
            if not email or not password_str or not name:
                error = "Tous les champs sont obligatoires."
                mode = "register"
            elif password_str != confirm:
                error = "Les mots de passe ne correspondent pas."
                mode = "register"
            elif pw_error:
                error = pw_error
                mode = "register"
            else:
                hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
                try:
                    conn = get_db()
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s)",
                            (email, hashed, name)
                        )
                    conn.commit()
                    conn.close()
                    session.permanent = True
                    session["user"] = {"email": email, "name": name}
                    return redirect(url_for("index"))
                except pymysql.err.IntegrityError:
                    # Message volontairement générique : ne pas confirmer
                    # l'existence d'un compte pour cet email (anti-énumération, F5).
                    error = "Impossible de créer le compte avec ces informations."
                    mode = "register"

    return render_template("login.html", error=error, mode=mode)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/cart")
def cart():
    items, total = get_cart_details()
    return render_template("cart.html", items=items, total=total)


@app.route("/cart/add", methods=["POST"])
def cart_add():
    # Entrées robustes : un product_id/qty non numérique ne doit pas faire un 500.
    try:
        product_id = int(request.form.get("product_id", ""))
        qty = int(request.form.get("qty", 1))
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    # Le produit doit exister et la quantité être raisonnable.
    if qty < 1 or qty > 99 or not get_product_by_id(product_id):
        return redirect(url_for("index"))

    product_id = str(product_id)
    cart = session.get("cart", {})
    cart[product_id] = min(cart.get(product_id, 0) + qty, 99)
    session["cart"] = cart

    # Redirection validée : jamais vers un domaine externe (anti Open Redirect).
    next_url = safe_redirect_target(request.form.get("next"), url_for("index"))
    return redirect(next_url)


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    product_id = str(request.form.get("product_id"))
    cart = session.get("cart", {})
    if product_id in cart:
        del cart[product_id]
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart/count")
def cart_count():
    cart  = session.get("cart", {})
    count = sum(cart.values())
    return jsonify({"count": count})


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------

# En production l'application est servie par Gunicorn (`gunicorn app:app`),
# le bloc __main__ n'est donc PAS exécuté. On initialise la base au chargement
# du module pour couvrir les deux cas (Gunicorn et exécution directe).
try:
    init_db()
except Exception as exc:  # pragma: no cover - dépend de la disponibilité RDS
    print(f"[init_db] initialisation différée: {exc}")

if __name__ == "__main__":
    # Démarrage local uniquement. debug désactivé (F2) : jamais de serveur de
    # développement ni de debugger interactif exposé.
    app.run(host="127.0.0.1", port=5000, debug=False)