import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from database.schema import add_notification_email

app = Flask(__name__)

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
    return render_template('index.html')

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
