from flask import Flask, flash, session, request, redirect, render_template, url_for

from db.data_layer import create_project, get_all_projects, get_project, update_project, delete_project
from db.data_layer import create_task, get_all_tasks, get_task, update_task, delete_task

app = Flask(__name__)


@app.route('/')
def index():
    projects = get_all_projects()
    return render_template('index.html', all_projects=projects)

@app.route('/create', methods=['POST'])
def project_add():
    title = request.form['title']
    create_project(title)
    return redirect(url_for('index'))

@app.route('/edit/<project_id>', methods=['GET', 'POST'])
def project_edit(project_id):
    if request.method == 'POST':
        update_project(project_id, request.form['title'])
        return redirect(url_for('index'))
    
    project = get_project(project_id)
    return render_template('edit_project.html', project=project)

@app.route('/delete/<project_id>')
def project_delete():
    delete_project(project_id)
    return redirect(url_for('index'))

@app.route('/project/<project_id>')
def task_all(project_id):
    project = get_project(project_id)
    tasks = get_all_tasks(project_id)
    return render_template('task.html', project=project, all_tasks=tasks)

@app.route('/project/<project_id>', methods=['POST'])
def task_add(project_id):
    description = request.form['description']
    create_task(project_id, description)
    return redirect(url_for('task_all'), project_id=project_id)

@app.route('/project/<project_id>/task/<task_id>/delete')
def task_delete(project_id, task_id):
    delete_task(task_id)
    return redirect(url_for('task_all', project_id=project_id))

@app.route('/project/<project_id>/task/<task_id>/edit', methods=['GET', 'POST'])
def task_edit(project_id, task_id):
    project = get_project(project_id)
    task = get_task(task_id)

    if request.method == 'POST':
        description = request.form['description']
        update_task(task_id, description)
        return redirect(url_for('task_all', project_id=project_id))

    return render_template('edit_task.html', project=project, task=task)

app.run(debug=True)