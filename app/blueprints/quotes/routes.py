from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import quotes_bp
from datetime import date
from app.forms.quotes_form import QuoteForm, DeleteForm
from app.models import UserQuotes, db
from app.utils.decorators import login_required

@quotes_bp.route("/")
@login_required
def quotes_list(): 
    username = session.get("username")
    user_quotes = UserQuotes.query.filter_by(username=username).order_by(UserQuotes.date.desc()).all()
    delete_form = DeleteForm()
    return render_template("quotes/quotes_list.html", user_quotes=user_quotes, delete_form=delete_form)

@quotes_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_quotes():    
    form = QuoteForm()
    if form.validate_on_submit():
        new_quote = UserQuotes(
            user_id=session["user_id"],
            username=session["username"],
            quotes=form.quotes.data,
            date=date.today()
        )
        
        db.session.add(new_quote)
        db.session.commit()
        flash("Quote added!", "Success")
        return redirect(url_for("quotes.quotes_list"))
    return render_template("quotes/quote_add.html", form=form)

@quotes_bp.route('/view/<int:quote_id>')
@login_required
def view_quote(quote_id):
    entry = UserQuotes.query.get_or_404(quote_id)
    return render_template("quotes/quote_read.html", entry=entry)

@quotes_bp.route("/<int:quote_id>/edit", methods=["GET", "POST"])
@login_required
def edit_quote(quote_id):
    entry = UserQuotes.query.get_or_404(quote_id)
    form = QuoteForm(obj=entry)
    
    if form.validate_on_submit():
        entry.quotes = form.quotes.data
        db.session.commit()
        flash("Quote entry updated!", "success")
        return redirect(url_for("quotes.quotes_list", quote_id=quote_id))
    return render_template("quotes/quote_edit.html", form=form, quote_id=quote_id)

@quotes_bp.route('/delete/<int:quote_id>', methods=['POST'])
@login_required
def delete_quote(quote_id):
    entry = UserQuotes.query.get_or_404(quote_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Quote entry deleted!", "info")
    return redirect(url_for("quotes.quotes_list"))
    
