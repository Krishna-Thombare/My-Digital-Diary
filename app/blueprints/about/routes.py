from flask import render_template, request, url_for
from . import about_bp

@about_bp.route("/aboutus")
def about_us():
    previous_url = request.referrer or url_for('home')    # Used to return the user to the exact page they came from
    return render_template("about/about_us.html", back_url=previous_url)
