from flask import render_template, request, redirect, url_for, session, flash
from . import ideas_bp
from datetime import date
from app.forms.ideas_form import IdeaForm, DeleteForm
from app.models import UserIdeas, db
from app.utils.decorators import login_required

@ideas_bp.route("/")
@login_required
def ideas_list(): 
    username = session.get("username")
    user_ideas = UserIdeas.query.filter_by(username=username).order_by(UserIdeas.date.desc()).all()
    delete_form = DeleteForm()
    return render_template("ideas/ideas_list.html", user_ideas=user_ideas, delete_form=delete_form)

@ideas_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        new_idea = UserIdeas(
            user_id=session["user_id"],
            username=session['username'], 
            ideas=form.ideas.data,
            date=date.today()
        )
        
        db.session.add(new_idea)
        db.session.commit()
        flash("Idea Added!", "Success")
        return redirect(url_for("ideas.ideas_list"))
    return render_template("ideas/idea_add.html", form=form)

@ideas_bp.route('/view/<int:idea_id>')
@login_required
def view_idea(idea_id):
    entry = UserIdeas.query.get_or_404(idea_id)
    return render_template("ideas/idea_read.html", entry=entry)

@ideas_bp.route("/<int:idea_id>/edit", methods=["GET", "POST"])
@login_required
def edit_idea(idea_id):
    entry = UserIdeas.query.get_or_404(idea_id)
    form = IdeaForm(obj=entry)
    
    if form.validate_on_submit():
        entry.ideas = form.ideas.data
        db.session.commit()
        flash("Idea entry updated!", "success")
        return redirect(url_for("ideas.ideas_list", idea_id=idea_id))
    return render_template("ideas/idea_edit.html", form=form, idea_id=idea_id)

@ideas_bp.route('/delete/<int:idea_id>', methods=['POST'])
@login_required
def delete_idea(idea_id):
    entry = UserIdeas.query.get_or_404(idea_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Idea entry deleted!", "info")
    return redirect(url_for("ideas.ideas_list"))
    
    
    
        