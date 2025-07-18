from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from . import journal_bp
from datetime import date, datetime
from app.forms.journal_form import JournalForm, DeleteForm
from app.models import db, UserJournal
from flask import jsonify
from app.utils.decorators import login_required

# Journal Entries Listing
@journal_bp.route("/")
@login_required
def journal_list():
    username = session.get("username")
    journals = UserJournal.query.filter_by(username=username).order_by(UserJournal.date.desc()).all()
    delete_form = DeleteForm()
    return render_template("journal/journal_list.html", journals=journals, delete_form=delete_form)

# Adding New Journal Entry
@journal_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_journal():
    form = JournalForm()
    today = datetime.now()
    date_str = f"{today.day} {today.strftime('%B, %Y')}"
    if form.validate_on_submit():
        new_entry = UserJournal(
            user_id=session["user_id"],
            username=session["username"],
            topic_name=form.topic_name.data,
            journal_texts=form.journal_texts.data,
            date=date.today()
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("Journal entry saved!", "success")
        return redirect(url_for("journal.journal_list"))
    return render_template("journal/journal_add.html", form=form, current_date=date_str)

# Viewing Juornal Entry
@journal_bp.route("/view/<int:journal_id>")
@login_required
def view_journal(journal_id):
    entry = UserJournal.query.get_or_404(journal_id)
    return render_template("journal/journal_read.html", entry=entry)

# Edit Journal Entry
@journal_bp.route("/view/<int:journal_id>/edit", methods=["GET", "POST"])
@login_required
def edit_journal(journal_id):
    entry = UserJournal.query.get_or_404(journal_id)
    form = JournalForm(obj=entry)
    
    if form.validate_on_submit():
        entry.topic_name = form.topic_name.data
        entry.journal_texts = form.journal_texts.data
        db.session.commit()
        flash("Journal entry updated!", "success")
        return redirect(url_for("journal.view_journal", journal_id=journal_id))
    return render_template("journal/journal_edit.html", form=form, journal_id=journal_id, entry=entry)

# Delete Journal Entry
@journal_bp.route("/delete/<int:journal_id>", methods=["POST"])
@login_required
def delete_journal(journal_id):
    entry = UserJournal.query.get_or_404(journal_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Journal entry deleted.", "info")
    return redirect(url_for("journal.journal_list"))

# Summarize Journal Entry
@journal_bp.route("/get-journal-content/<int:journal_id>")
def get_journal_content(journal_id):
    entry = UserJournal.query.get_or_404(journal_id)
    return jsonify({"journal_texts": entry.journal_texts})

