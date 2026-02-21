"""
Rutas/Endpoints para el módulo de unidades de medida.
"""

from flask import flash, redirect, render_template, request, url_for

from app.catalogs import unit_of_measures
from app.catalogs.unit_of_measures.forms import UnitOfMeasureForm
from app.catalogs.unit_of_measures.services import UnitOfMeasureService
from app.models import role

from . import unit_of_measures_bp
from .forms import UnitOfMeasureForm
from .services import UnitOfMeasureService
from app.exceptions import ConflictError, NotFoundError, ValidationError


@unit_of_measures_bp.route("/", methods=["GET"])
def list_unit_of_measures():
    """
    Muestra la lista de unidades de medida del catálogo.

    Returns:
        HTML: Página con la lista de unidades de medida
    """
    unit_of_measures = UnitOfMeasureService.get_all()
    return render_template("unit_of_measures/list.html", unit_of_measures=unit_of_measures)

@unit_of_measures_bp.route("/create", methods=["GET", "POST"])
def create_unit_of_measure():
    """
    Muestra el formulario para crear una nueva unidad de medida y crea una nueva unidad de medida en el catálogo.

    GET: Muestra el formulario de creación.
    POST: Valida el formulario y crea una nueva unidad de medida.

    Returns:
        GET - HTML: Página con el formulario de creación.
        POST - REDIRECT: Redirige al formulario de creación con mensaje flash.
    """
    form = UnitOfMeasureForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "abbreviation": form.abbreviation.data,
            "active": form.active.data
        }
        try:
            UnitOfMeasureService.create(data)
            flash("Unidad de medida creada exitosamente", "success")
            return redirect(url_for("unit_of_measures.list_unit_of_measures"))
        except (ConflictError, ValidationError) as e:
            flash(str(e), "danger")

    
    return render_template("unit_of_measures/create.html", form=form)