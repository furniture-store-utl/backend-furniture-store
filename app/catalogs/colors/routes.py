"""
Rutas/Endpoints para el módulo de colores.
"""

from flask import flash, redirect, render_template, url_for

from . import colors_bp
from .forms import ColorForm
from .services import ColorService
from app.exceptions import ConflictError


@colors_bp.route("/", methods=["GET"])
def list_colors():
    """
    Muestra la lista de colores del catálogo.

    Returns:
        HTML: Página con la lista de colores
    """
    colors = ColorService.get_all()
    return render_template("colors/list.html", colors=colors)


@colors_bp.route("/create", methods=["GET", "POST"])
def create_color():
    """
    Muestra el formulario y crea un nuevo color en el catálogo.

    GET: Renderiza el formulario de creación.
    POST: Valida el formulario, crea el color y redirige.

    Returns:
        GET - HTML: Página con el formulario de creación de color
        POST - Redirect: Redirige al formulario con mensaje flash
    """
    form = ColorForm()

    if form.validate_on_submit():
        data = {"name": form.name.data}
        try:
            ColorService.create(data)
            flash("Color creado exitosamente", "success")
            return redirect(url_for("colors.create_color"))
        except ConflictError as e:
            flash(e.message, "error")

    return render_template("colors/create.html", form=form)
