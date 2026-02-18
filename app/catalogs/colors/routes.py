"""
Rutas/Endpoints para el módulo de colores.
"""

from flask import flash, redirect, render_template, request, url_for

from . import colors_bp
from .services import ColorService
from app.exceptions import ConflictError, ValidationError


@colors_bp.route("/create", methods=["GET"])
def create_color_form():
    """
    Muestra el formulario para crear un nuevo color.

    Returns:
        HTML: Página con el formulario de creación de color
    """
    return render_template("colors/create.html")


@colors_bp.route("/create", methods=["POST"])
def create_color():
    """
    Crea un nuevo color en el catálogo.

    Form Data:
        name (str): Nombre del color (requerido)

    Returns:
        Redirect: Redirige al formulario de creación
    """
    data = {"name": request.form.get("name")}

    try:
        ColorService.create(data)
        flash("Color creado exitosamente", "success")
    except (ValidationError, ConflictError) as e:
        flash(e.message, "error")

    return redirect(url_for("colors.create_color_form"))
