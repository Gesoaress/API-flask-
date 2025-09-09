from flask import render_template, request, redirect, url_for, abort
from extensions import db
from models.task import Task
from models.user import User

class TaskController:

    @staticmethod
    def list_tasks():
        tasks = Task.query.order_by(Task.id.desc()).all()
        return render_template("tasks.html", tasks=tasks)

    @staticmethod
    def create_task():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            user_id = request.form.get("user_id", type=int)

            if not title or not user_id:
                # validação simples
                users = User.query.order_by(User.nome.asc()).all()
                msg = "Título e Usuário são obrigatórios."
                return render_template("create_task.html", users=users, error=msg, form=request.form)

            # garante que o usuário existe
            user = User.query.get(user_id)
            if not user:
                users = User.query.order_by(User.nome.asc()).all()
                msg = "Usuário informado não existe."
                return render_template("create_task.html", users=users, error=msg, form=request.form)

            task = Task(title=title, description=description, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("list_tasks"))

        # GET: carrega usuários para o <select>
        users = User.query.order_by(User.nome.asc()).all()
        return render_template("create_task.html", users=users)

    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if not task:
            abort(404)
        task.toggle_status()
        db.session.commit()
        return redirect(url_for("list_tasks"))

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            abort(404)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("list_tasks"))
