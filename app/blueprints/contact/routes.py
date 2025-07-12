from flask import render_template, request, redirect, url_for, flash
from . import contact_bp
from app.forms.contact_form import ContactForm

@contact_bp.route("/contactus", methods=["GET", "POST"])
def contact_us():
    form = ContactForm()
    previous_url = request.referrer or url_for('home')

    if form.validate_on_submit():
        # Optionally, save to DB or send an email here
        flash("Thanks for reaching out! We'll get back to you soon.", "success")
        return redirect(previous_url)

    return render_template("contact/contact_us.html", form=form, back_url=previous_url)
