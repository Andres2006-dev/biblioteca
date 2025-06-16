from .usuarios import usuarios_bp
from .categoria import categoria_bp
from .autores import autores_bp
from .documentacion import documentacion_bp

def registrar_rutas(app):
    app.register_blueprint(usuarios_bp, url_prefix  ='/usuarios')
    app.register_blueprint(categoria_bp, url_prefix  ='/categorias')
    app.register_blueprint(autores_bp, url_prefix  ='/autores')
    app.register_blueprint(documentacion_bp, url_prefix  ='/documentacion')