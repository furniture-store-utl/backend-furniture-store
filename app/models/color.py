from sqlalchemy.sql import func

from ..extensions import db


class Color(db.Model):
    """
    Modelo de Color para catálogo de referencias de colores.

    Attributes:
          id_color: Identificador único del color.
          name: Nombre del color.
          active: Indica si el color está activo o no.

          created_at: Fecha de creación del color.
          updated_at: Fecha de última actualización del color.
          deleted_at: Fecha de eliminación lógica del color.

          created_by: Usuario que creó el color.
          updated_by: Usuario que actualizó el color.
          deleted_by: Usuario que eliminó el color.
    """

    __tablename__ = 'colors'

    id_color = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
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

    def to_dict(self) -> dict:
        """
        Serializa el modelo a diccionario.

        Returns:
            dict: Representación del color en formato diccionario
        """
        return {
            "id_color": self.id_color,
            "name": self.name,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
