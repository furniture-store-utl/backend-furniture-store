"""
Servicios de lógica de negocio para colores.
"""

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.color import Color
from app.exceptions import ConflictError, ValidationError


class ColorService:
    """Servicio para operaciones de negocio relacionadas con colores."""

    @staticmethod
    def create(data: dict) -> dict:
        """
        Crea un nuevo color en el catálogo.

        Args:
            data: Diccionario con los datos del color (name requerido)

        Returns:
            dict: Color creado serializado

        Raises:
            ValidationError: Si el nombre está vacío o no se proporciona
            ConflictError: Si ya existe un color con el mismo nombre
        """
        name = data.get("name")

        if not name or not name.strip():
            raise ValidationError("El nombre del color es requerido")

        name = name.strip()

        existing = Color.query.filter_by(name=name).first()
        if existing:
            raise ConflictError(f"Ya existe un color con el nombre '{name}'")

        color = Color(name=name)
        db.session.add(color)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictError(f"Ya existe un color con el nombre '{name}'")

        return color.to_dict()
