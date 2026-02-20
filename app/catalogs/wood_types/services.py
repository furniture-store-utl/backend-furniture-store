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

    @staticmethod
    def create(data: dict) -> dict:
        """
        Crea un nuevo tipo de madera en el catálogo.

        Args:
            data: Diccionario con los datos del tipo de madera (name requerido)

        Returns:
            dict: Tipo de madera creado serializado

        Raises:
            ValidationError: Si el nombre está vacío o no se proporciona
            ConflictError: Si ya existe un tipo de madera con el mismo nombre
        """
        name = data.get("name")

        if not name or not name.strip():
            raise ValidationError("El nombre del tipo de madera es requerido")

        name = name.strip()

        existing = WoodType.query.filter_by(name=name).first()
        if existing:
            raise ConflictError(f"Ya existe un tipo de madera con el nombre '{name}'")

        wood_type = WoodType(name=name)
        db.session.add(wood_type)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictError(f"Ya existe un tipo de madera con el nombre '{name}'")

        return wood_type.to_dict()
