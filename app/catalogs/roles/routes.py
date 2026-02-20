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


@roles_bp.route("/create", methods=["GET", "POST"])
def create_role():
    """
    Muestra el formulario y crea un nuevo rol en el catálogo.

    GET: Renderiza el formulario de creación.
    POST: Valida el formulario, crea el rol y redirige.

    Returns:
        GET - HTML: Página con el formulario de creación de rol
        POST - Redirect: Redirige al formulario con mensaje flash
    """
    form = RoleForm()

    if form.validate_on_submit():
        data = {"name": form.name.data}
        try:
            RoleService.create(data)
            flash("Rol creado exitosamente", "success")
            return redirect(url_for("roles.create_role"))
        except ConflictError as e:
            flash(e.message, "error")

    return render_template("roles/create.html", form=form)
