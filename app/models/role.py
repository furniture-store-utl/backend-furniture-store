from sqlalchemy.sql import func
from ..extensions import db

class Role(db.Model):
    """
    Modelo de Rol para la gestión de permisos y perfiles de usuario.

    Attributes:
          id_role: Identificador único del rol.
          name: Nombre del rol (ej. 'Admin', 'Editor', 'Viewer').
          active: Indica si el rol está activo o no.

          created_at: Fecha de creación del rol.
          updated_at: Fecha de última actualización del rol.
          deleted_at: Fecha de eliminación lógica del rol.

          created_by: Usuario que creó el rol.
          updated_by: Usuario que actualizó el rol.
          deleted_by: Usuario que eliminó el rol.
    """

    __tablename__ = 'roles'

    id_role = db.Column(db.Integer, primary_key=True)
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
            dict: Representación del rol en formato diccionario
        """
        return {
            "id_role": self.id_role,
            "name": self.name,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }