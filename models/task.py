from extensions import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def toggle_status(self):
        self.status = "Concluído" if self.status == "Pendente" else "Pendente"

    def __repr__(self):
        return f"<Task {self.title} ({self.status})>"
