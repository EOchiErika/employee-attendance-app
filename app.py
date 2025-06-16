from datetime import datetime, date 
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

from modelos import db
from modelos import Usuario, Registro


@app.route('/inicio.html', methods = ['GET', 'POST'])
def inicio():
        return render_template('inicio.html')

@app.route('/entrada.html', methods = ['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        trabajador = Usuario.query.filter_by(legajo=request.form['legajo']).first()
        if not trabajador:
            ret = render_template('entrada.html', error="Legajo incorrecto")
        elif trabajador.dni[-4:] != request.form['dni']:
            ret = render_template('entrada.html', error = "DNI incorrecto")
        else:
            hoy = date.today()
            entrada_registrada = Registro.query.filter_by(idtrabajador=trabajador.id, fecha=hoy).first()
            if entrada_registrada:
                ret = render_template('entrada.html', error="Ya registraste una entrada hoy")
            else:
                entrada_nueva = Registro(fecha=hoy, horaentrada=datetime.now().time(), dependencia=request.form['dependencia'], idtrabajador=trabajador.id)
                db.session.add(entrada_nueva)
                db.session.commit()
                ret = render_template('entrada.html', mensaje="Entrada registrada con exito")
    else:
        ret = render_template('entrada.html')
    return ret 

@app.route('/salida.html', methods=['GET', 'POST'])
def salida():
    if request.method == 'POST':
        dni = request.form.get('dni')
        legajo = request.form.get('legajo')
        registrar = request.form.get('registrar')
        confirmar = request.form.get('confirmar')
        trabajador = Usuario.query.filter_by(legajo=legajo).first()
        if not trabajador:
            return render_template('salida.html', error="Legajo incorrecto")
        elif trabajador.dni[-4:] != dni:
            return render_template('salida.html', error="DNI incorrecto")
        else: 
            hoy = date.today()
            entrada_registrada = Registro.query.filter_by(idtrabajador=trabajador.id, fecha=hoy).first()
        if not entrada_registrada:
            return render_template('salida.html', error="No registraste una entrada")
        if registrar:
            return render_template('salida.html', registrar=True, dependencia=entrada_registrada.dependencia, dni=dni, legajo=legajo)
        if confirmar:
            entrada_registrada.horasalida = datetime.now().time()
            db.session.commit()
            return render_template('salida.html', mensaje="Salida registrada con éxito")
    return render_template('salida.html')

@app.route('/consulta.html', methods = ['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        fechaInicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
        fechaFin = datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date()      
        dni=request.form['dni']
        trabajador = Usuario.query.filter_by(legajo=request.form['legajo']).first()
        if not trabajador:
            ret = render_template('consulta.html', error="Legajo incorrecto")
        elif trabajador.dni[-4:] != dni:
            ret = render_template('consulta.html', error="DNI incorrecto")
        else: 
            registros = Registro.query.filter(Registro.idtrabajador == trabajador.id, Registro.fecha.between(fechaInicio, fechaFin)).order_by(Registro.fecha, Registro.horaentrada).all()
            ret = render_template('registros.html', registros=registros)
    else:
        ret = render_template('consulta.html')
    return ret

if __name__ == '__main__':
    app.run(debug=True)