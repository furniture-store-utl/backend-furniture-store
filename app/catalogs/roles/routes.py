"""
Rutas/Endpoints para el módulo de roles.
"""

from flask import flash, redirect, render_template, url_for

from . import roles_bp
from .forms import RoleForm
from .services import RoleService
from app.exceptions import ConflictError


@roles_bp.route("/", methods=["GET"])
def list_roles():
    """
    Muestra la lista de roles del catálogo.

    Returns:
        HTML: Página con la lista de roles
    """
    roles = RoleService.get_all()
    return render_template("roles/list.html", roles=roles)
