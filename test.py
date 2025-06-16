from modelos import db, Usuario
from app import app

with app.app_context():
    usuarios = Usuario.query.all()
    print(f"Cantidad de trabajadores en la base: {len(usuarios)}")
    for u in usuarios:
        print(f"Legajo: {u.legajo}, DNI: {u.dni}, Nombre: {u.nombre}")
