""""
Rutas/Endpoints para el módulo de tipos de madera.
"""
from flask import flash, redirect, render_template, url_for
from . import woods_types_bp
from .forms import WoodTypeForm 
from .services import WoodTypeService
from app.exceptions import ConflictError


@woods_types_bp.route("/", methods=["GET"])
def list_wood_types():
    """
    Muestra la lista de tipos de madera del catálogo.

    Returns:
        HTML: Página con la lista de tipos de madera
    """
    wood_types = WoodTypeService.get_all()
    return render_template("wood_types/list.html", wood_types=wood_types)

@woods_types_bp.route("/create", methods=["GET", "POST"])
def create_wood_type(): 
    """
    Muestra el formulario y crea un nuevo tipo de madera en el catálogo.

    GET: Renderiza el formulario de creación.
    POST: Valida el formulario, crea el tipo de madera y redirige.
    Returns:
        GET - HTML: Página con el formulario de creación de tipo de madera
        POST - Redirect: Redirige al formulario con mensaje flash
    """
    form = WoodTypeForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        try:
            WoodTypeService.create(data)
            flash("Tipo de madera creado exitosamente", "success")
            return redirect(url_for("woods_types.create_wood_type"))
        except ConflictError as e:
            flash(e.message, "error")

    return render_template("wood_types/create.html", form=form)
