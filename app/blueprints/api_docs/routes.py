from flask import render_template
from flask_login import login_required
from . import api_docs_bp

@api_docs_bp.route("/api_docs")
@login_required
def api_docs():
    return render_template('api_docs/api_docs.html')

