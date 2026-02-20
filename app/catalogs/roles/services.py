"""
Servicios de lógica de negocio para roles.
"""

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.role import Role
from app.exceptions import ConflictError, ValidationError


class RoleService:
    """Servicio para operaciones de negocio relacionadas con roles."""

    @staticmethod
    def get_all() -> list[Role]:
        """
        Obtiene todos los roles activos.

        Returns:
            list[Role]: Lista de objetos Role activos
        """
        return Role.query.filter_by(active=True).all()

