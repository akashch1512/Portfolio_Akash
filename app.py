import os
import time
import razorpay
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from database.schema import add_notification_email

app = Flask(__name__)
load_dotenv()

APPOINTMENT_AMOUNT_PAISE = 10000
APPOINTMENT_CURRENCY = "INR"

def get_razorpay_client():
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        return None, "Razorpay keys are missing. Check your .env file."
    return razorpay.Client(auth=(key_id, key_secret)), None

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the main single-page portfolio.
    You can pass dynamic data here later (e.g., fetching real stats).
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        wants_json = (
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            or request.accept_mimetypes.best == 'application/json'
        )

        if not email:
            if wants_json:
                return jsonify({"ok": False, "message": "Please enter a valid email."}), 400
            return redirect(url_for('home'))

        try:
            add_notification_email(email)
        except Exception:
            if wants_json:
                return jsonify({"ok": False, "message": "Could not save email. Try again."}), 500
            return redirect(url_for('home'))

        if wants_json:
            return jsonify({"ok": True, "message": "Thanks! You are on the list."})
        return redirect(url_for('home'))
    return render_template('index.html', razorpay_key_id=os.getenv("RAZORPAY_KEY_ID", ""))

@app.route('/api/razorpay/order', methods=['POST'])
def create_razorpay_order():
    client, error = get_razorpay_client()
    if error:
        return jsonify({"ok": False, "message": error}), 500

    receipt_id = f"appointment_{int(time.time())}"
    payload = {
        "amount": APPOINTMENT_AMOUNT_PAISE,
        "currency": APPOINTMENT_CURRENCY,
        "receipt": receipt_id,
        "payment_capture": 1
    }

    try:
        order = client.order.create(payload)
    except Exception:
        return jsonify({"ok": False, "message": "Could not create Razorpay order."}), 500

    return jsonify({
        "ok": True,
        "orderId": order.get("id"),
        "amount": order.get("amount"),
        "currency": order.get("currency"),
        "keyId": os.getenv("RAZORPAY_KEY_ID", ""),
        "name": "Akash Chaudhari",
        "description": "Book an appointment"
    })

@app.route('/api/razorpay/verify', methods=['POST'])
def verify_razorpay_payment():
    client, error = get_razorpay_client()
    if error:
        return jsonify({"ok": False, "message": error}), 500

    data = request.get_json(silent=True) or {}
    required_fields = ("razorpay_order_id", "razorpay_payment_id", "razorpay_signature")
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"ok": False, "message": "Missing payment verification fields."}), 400

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
    except Exception:
        return jsonify({"ok": False, "message": "Payment verification failed."}), 400

    return jsonify({"ok": True})

# --- SEO: sitemap + robots ---
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('templates', 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('templates', 'robots.txt', mimetype='text/plain')

# FUTURE EXPANSION EXAMPLE:
# @app.route('/projects')
# def projects():
#     return render_template('projects.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    debug = os.getenv('FLASK_DEBUG') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
