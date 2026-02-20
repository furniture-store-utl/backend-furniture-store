"""
Formularios para el módulo de roles.
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class RoleForm(FlaskForm):
    """Formulario para crear un rol."""

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre del rol es requerido"),
            Length(max=50, message="El nombre no puede exceder 50 caracteres"),
        ],
    )
