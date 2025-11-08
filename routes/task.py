from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task

#
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/", methods=["GET"])
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@tasks_bp.route("/add", methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    else:
        flash('Title cannot be empty', 'warning')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.get_or_404(task_id)
    
    # Cycle through statuses: Pending -> Working -> Done -> Pending
    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Done'
    else:
        task.status = 'Pending'
    
    db.session.commit()
    flash(f'Task status updated to {task.status}', 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=["POST"])
def clear_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared', 'info')
    return redirect(url_for('tasks.view_tasks'))
