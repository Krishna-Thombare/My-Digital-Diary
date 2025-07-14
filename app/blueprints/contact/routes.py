from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from app import mail
from dotenv import load_dotenv
import os
from . import contact_bp
from app.forms.contact_form import ContactForm

load_dotenv()

@contact_bp.route("/contactus", methods=["GET", "POST"])
def contact_us():
    form = ContactForm()
    previous_url = request.referrer or url_for('home')

    if form.validate_on_submit():
        msg = Message(
            subject="New Contact Us Message",
            recipients=[os.getenv('MAIL_USERNAME')],  # where you want to receive the message
            body=f"Name: {form.name.data}\nEmail: {form.email.data}\nPhone: {form.phone_no.data}\nMessage:\n{form.message.data}"
        )
        
        mail.send(msg)
        
        flash("Thanks for reaching out! We'll get back to you soon.", "success")
        return redirect(previous_url)

    return render_template("contact/contact_us.html", form=form, back_url=previous_url)
