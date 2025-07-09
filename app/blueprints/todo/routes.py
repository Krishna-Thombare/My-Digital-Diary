from flask import render_template, request, redirect, url_for, session, flash
from . import todo_bp
from app.forms.todo_form import TodoForm
from app.models import db, UserTodoList
from datetime import date
from app.utils.decorators import login_required

@todo_bp.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    form = TodoForm()

    if form.validate_on_submit():
        new_task = UserTodoList(
            user_id=session['user_id'],
            username=session['username'],
            tasks=form.task.data,
            status=False,
            date=date.today()
        )
        
        db.session.add(new_task)
        db.session.commit()
        flash("Task added!", "success")
        return redirect(url_for('todo.todo'))

    todos = UserTodoList.query.filter_by(user_id=session['user_id']).all()
    return render_template('todo/todo.html', form=form, todos=todos)

# Toggle Status - Check Box Tick
@todo_bp.route('/toggle/<int:todo_id>', methods=['POST'])
@login_required
def toggle_status(todo_id):
    task = UserTodoList.query.get_or_404(todo_id)

    # Ensure task belongs to the logged-in user
    if task.user_id != session.get('user_id'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('todo.todo'))

    task.status = not task.status
    db.session.commit()
    return redirect(url_for('todo.todo'))
    
# Delete Task
@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete_task(todo_id):
    task = UserTodoList.query.get_or_404(todo_id)

    if task.user_id != session.get('user_id'):
        flash("Unauthorized access!", "danger")
        return redirect(url_for('todo.todo'))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo.todo'))

    

