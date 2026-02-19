"""
Formularios para el módulo de colores.
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ColorForm(FlaskForm):
    """Formulario para crear un color."""

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre del color es requerido"),
            Length(max=50, message="El nombre no puede exceder 50 caracteres"),
        ],
    )
