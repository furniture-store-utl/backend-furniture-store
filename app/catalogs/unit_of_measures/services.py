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
    
    @staticmethod
    def create(data: dict) -> dict:
        """
        Crea una nueva unidad de medida.

        Args:
            data (dict): Diccionario con los datos de la unidad de medida a crear

        Returns:
            dict: La unidad de medida creada

        Raises:
            ValidationError: Si los datos proporcionados no son válidos
            ConflictError: Si ya existe una unidad de medida con el mismo nombre
        """
        name = data.get("name", "")
        
        if not name or not name.strip():
            raise ValidationError("El nombre de la unidad de medida es requerido")
        
        name = name.strip()

        existing = UnitOfMeasure.query.filter(func.lower(UnitOfMeasure.name) == func.lower(name)).first()
        if existing:
            raise ConflictError(f"Ya existe una unidad de medida con el nombre '{name}'")
        
        unit_of_measure = UnitOfMeasure(name=name)
        db.session.add(unit_of_measure)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictError("Ocurrió un error al crear la unidad de medida. Intente nuevamente.")
        
        return unit_of_measure.to_dict()