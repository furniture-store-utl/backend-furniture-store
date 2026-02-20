"""
Servicios de lógica de negocio para tipos de madera.
"""

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.exceptions import ConflictError, ValidationError
from app.models.wood_type import WoodType

class WoodTypeService:
    """Servicio para operaciones de negocio relacionadas con tipos de madera."""

    @staticmethod
    def get_all() -> list[WoodType]:
        """
        Obtiene todos los tipos de madera activos.

        Returns:
            list[WoodType]: Lista de objetos WoodType activos
        """
        return WoodType.query.filter_by(active=True).all()

