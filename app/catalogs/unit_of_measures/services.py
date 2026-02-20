"""
Servicios de lógica de negocio para unidades de medida.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from app.extensions import db
from app.models.role import UnitOfMeasure
from app.exceptions import ConflictError, ValidationError, NotFoundError


class UnitOfMeasureService:
    """Servicio para operaciones de negocio relacionadas con unidades de medida."""

    @staticmethod
    def get_all() -> list[UnitOfMeasure]:
        """
        Obtiene todas las unidades de medida activas.

        Returns:
            list[UnitOfMeasure]: Lista de objetos UnitOfMeasure activos
        """
        return UnitOfMeasure.query.filter_by(active=True).all()