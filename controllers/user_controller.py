from flask import render_template, request, redirect, url_for
from extensions import db
from models.user import User

class UserController:

    @staticmethod
    def list_users():
        users = User.query.all()
        return render_template("users.html", users=users)

    @staticmethod
    def create_user():
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]

            novo_usuario = User(nome=nome, email=email)
            db.session.add(novo_usuario)
            db.session.commit()

            return redirect(url_for("list_users"))
        
        return render_template("create_user.html")

    @staticmethod
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)

        if request.method == "POST":
            user.nome = request.form["nome"]
            user.email = request.form["email"]
            db.session.commit()
            return redirect(url_for("list_users"))

        return render_template("edit_user.html", user=user)

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("list_users"))
