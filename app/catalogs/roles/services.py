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
    
    @staticmethod
    def create(data: dict) -> dict:
        """
        Crea un nuevo rol en el catálogo.

        Args:
            data: Diccionario con los datos del rol (name requerido)

        Returns:
            dict: Rol creado serializado

        Raises:
            ValidationError: Si el nombre está vacío o no se proporciona
            ConflictError: Si ya existe un rol con el mismo nombre
        """
        name = data.get("name")

        if not name or not name.strip():
            raise ValidationError("El nombre del rol es requerido")

        name = name.strip()

        existing = Role.query.filter_by(name=name).first()
        if existing:
            raise ConflictError(f"Ya existe un rol con el nombre '{name}'")

        role = Role(name=name)
        db.session.add(role)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictError(f"Ya existe un rol con el nombre '{name}'")

        return role.to_dict()

