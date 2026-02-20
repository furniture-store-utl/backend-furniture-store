"""
Formularios para el módulo de unidades de medida.
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class UnitOfMeasureForm(FlaskForm):
    """Formulario para crear una unidad de medida."""

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre de la unidad de medida es requerido"),
            Length(max=50, message="El nombre no puede exceder 50 caracteres"),
        ],
    )
