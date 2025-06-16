from app import app
from modelos import db, Usuario

with app.app_context():
    usuarios = Usuario.query.all()
    if not usuarios:
        print("No hay usuarios en la base de datos.")
    else:
        for u in usuarios:
            print(f"id: {u.id}, legajo: {u.legajo}, dni: {u.dni}, dni últimos 4: {u.dni % 10000}")
