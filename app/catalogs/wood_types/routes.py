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


