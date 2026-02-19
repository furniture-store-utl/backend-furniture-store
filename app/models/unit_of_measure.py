from sqlalchemy.sql import func

from ..extensions import db


class UnitOfMeasure(db.Model):
    """
    Modelo de Unidades de medida para catálogo de referencias de unidades.

    Attributes:
          id_unit_of_measure: Identificador único de la unidad.
          name: Nombre de la unidad.
          active: Indica si la unidad está activo o no.
          abbreviation: Abreviatura de la unidad.

          created_at: Fecha de creación de la unidad.
          updated_at: Fecha de última actualización de la unidad.
          deleted_at: Fecha de eliminación lógica de la unidad.

          created_by: Usuario que creó la unidad.
          updated_by: Usuario que actualizó la unidad.
          deleted_by: Usuario que eliminó la unidad.
    """

    __tablename__ = 'unit_of_measures'

    id_unit_of_measure = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(10), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    deleted_by = db.Column(db.String(100), nullable=True)
