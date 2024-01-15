from flask import render_template, request, redirect, session, flash, url_for
from app_flask.modelos.modelo_revistas import Revista
from app_flask import app

@app.route('/dashboard', methods=['GET'])
def desplegar_revistas():
    if 'id_usuario' not in session:
        return redirect('/')

    lista_revistas = Revista.obtener_todos()
    return render_template('dashboard.html', lista_revistas=lista_revistas)

@app.route('/new', methods=['GET'])
def desplegar_formulario_revistas():
    if 'id_usuario' not in session:
        return redirect('/')

    return render_template('new.html')

@app.route('/new', methods=['POST'])
def crear_revistas():
    if 'id_usuario' not in session:
        return redirect('/')

    titulo = request.form.get('titulo', '')
    descripcion = request.form.get('descripcion', '')

    nueva_revista = {
        'id_author': session['id_usuario'],
        'titulo': titulo,
        'descripcion': descripcion
    }

    if not Revista.validar_revistas(nueva_revista):
        flash('Error al crear la revista. Por favor, inténtalo de nuevo.', 'error_creacion_revista')
        return redirect('/new')

    id_revista = Revista.crear_revista(nueva_revista)

    if not id_revista:
        flash('Error al crear la revista.', 'error_creacion_revista')
    else:
        flash('Revista creada exitosamente.', 'success_creacion_revista')

    return redirect('/dashboard')

@app.route('/eliminar/revistas/<int:id>', methods=['POST'])
def eliminar_revistas(id):
    revistas = {'id': id}
    Revista.elimina_uno(revistas)
    return redirect('/dashboard')

@app.route('/formulario/editar/revistas/<int:id>', methods=['GET'])
def despliega_formulario_editar_revistas(id):
    if 'id_usuario' not in session:
        return redirect('/')

    datos = {'id': id}
    revistas = Revista.obtener_uno(datos)
    return render_template('formulario_editar_revistas.html', revistas=revistas)

@app.route('/editar/revistas/<int:id>', methods=['POST'])
def editar_revistas(id):
    if not Revista.validar_revistas(request.form):
        return redirect(f'/formulario/editar/revistas/{id}')
    editar_revistas = {
        **request.form,
        'id': id,
        'id_usuario': session['id_usuario']
    }
    Revista.actualizar_uno(editar_revistas)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def desplegar_detalle_revistas(id):
    if 'id_usuario' not in session:
        return redirect('/')

    id_usuario = session['id_usuario']
    
    revista = Revista.obtener_detalles_por_id_usuario(id_usuario, id)

    if revista is None:
        flash('No se encontró la revista.', 'error_revista_no_encontrada')
        return redirect('/dashboard')

    return render_template('show.html', revista=revista)

@app.route('/revistas/usuario', methods=['GET'])
def obtener_revistas_usuario():
    if 'id_usuario' not in session:
        return redirect('/')

    id_usuario = session['id_usuario']
    revistas_del_usuario = Revista.obtener_revistas_por_usuario(id_usuario)

    return render_template('revistas_usuario.html', revistas_del_usuario=revistas_del_usuario)

@app.route('/eliminar/revistas/<int:id>', methods=['POST'])
def eliminar_revista(id):
    revista = {'id': id}
    Revista.elimina_uno(revista)
    return redirect('/user/account')