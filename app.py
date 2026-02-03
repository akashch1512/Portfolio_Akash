import os

from flask import Flask, render_template

app = Flask(__name__)

# --- Routes ---

@app.route('/')
def home():
    """
    Renders the main single-page portfolio.
    You can pass dynamic data here later (e.g., fetching real stats).
    """
    return render_template('index.html')

# FUTURE EXPANSION EXAMPLE:
# @app.route('/projects')
# def projects():
#     return render_template('projects.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    debug = os.getenv('FLASK_DEBUG') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
