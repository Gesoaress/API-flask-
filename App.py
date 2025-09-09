from flask import Flask, render_template
import os
from extensions import db
from controllers.user_controller import UserController
from controllers.task_controller import TaskController


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "users.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from models.user import User
        from models.task import Task   # <— importante
        db.create_all()

    @app.route("/")
    def index():
        return render_template("index.html")

    # Rotas de Usuários
    app.add_url_rule("/users", view_func=UserController.list_users, methods=["GET"], endpoint="list_users")
    app.add_url_rule("/users/new", view_func=UserController.create_user, methods=["GET", "POST"], endpoint="create_user")
    app.add_url_rule("/users/edit/<int:user_id>", view_func=UserController.edit_user, methods=["GET", "POST"], endpoint="edit_user")
    app.add_url_rule("/users/delete/<int:user_id>", view_func=UserController.delete_user, methods=["POST"], endpoint="delete_user")

    # Rotas de Tarefas
    app.add_url_rule("/tasks", view_func=TaskController.list_tasks, methods=["GET"], endpoint="list_tasks")
    app.add_url_rule("/tasks/new", view_func=TaskController.create_task, methods=["GET", "POST"], endpoint="create_task")
    app.add_url_rule("/tasks/update/<int:task_id>", view_func=TaskController.update_task_status, methods=["POST"], endpoint="update_task_status")
    app.add_url_rule("/tasks/delete/<int:task_id>", view_func=TaskController.delete_task, methods=["POST"], endpoint="delete_task")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
