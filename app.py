#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, jsonify, redirect, render_template, request, abort, url_for
from models import db, migrate, TodoList, Todo
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate.init_app(app, db)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return redirect(url_for('get_all_lists', list_id=1))


@app.route("/lists/<list_id>")
def get_all_lists(list_id):
    lists = TodoList.query.all()
    current__list = TodoList.query.get(list_id)
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    return render_template('index.html', lists=lists, current__list=current__list, todos=todos)


#  TodoLists
#  ----------------------------------------------------------------
@app.route('/lists/create', methods=['POST'])
def create_todo_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_todo_list(list_id):
    error = False
    try:
        todolist = TodoList.query.get(list_id)
        for todo in todolist.todos:
            db.session.delete(todo)

        db.session.delete(todolist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})


@app.route('/lists/<list_id>/checked', methods=['POST'])
def update_list_status(list_id):
    error = False
    try:
        todolist = TodoList.query.get(list_id)
        for todo in todolist.todos:
            todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
        error = False
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('index'))


#  Todos
#  ----------------------------------------------------------------


@app.route('/todos/create', methods=['POST'])
def create_todos():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description,
                    completed=False, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route("/todos/<todo_id>/delete", methods=['DELETE'])
def delete_todos(todo_id):
    error = False
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'sucess': True})


@app.route('/todos/<todo_id>/checked', methods=['POST'])
def update_todo_status(todo_id):
    error = False
    try:
        checked = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = checked
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('index'))
