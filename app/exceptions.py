"""
Módulo de excepciones personalizadas para el manejo centralizado de errores.

Este módulo define excepciones específicas del dominio de negocio
que permiten un manejo consistente de errores en toda la aplicación.
"""

from flask import jsonify


class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(self, message: str, status_code: int = 500, payload: dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        """Convierte la excepción a un diccionario para la respuesta JSON."""
        response = {
            "success": False,
            "error": {
                "message": self.message,
                "code": self.status_code
            }
        }
        if self.payload:
            response["error"]["details"] = self.payload
        return response


class ValidationError(AppException):
    """Excepción para errores de validación de datos de entrada."""

    def __init__(self, message: str = "Datos de entrada inválidos", payload: dict = None):
        super().__init__(message, status_code=400, payload=payload)


class NotFoundError(AppException):
    """Excepción para recursos no encontrados."""

    def __init__(self, message: str = "Recurso no encontrado", payload: dict = None):
        super().__init__(message, status_code=404, payload=payload)


class ConflictError(AppException):
    """Excepción para conflictos de datos (ej: duplicados)."""

    def __init__(self, message: str = "Conflicto con el recurso existente", payload: dict = None):
        super().__init__(message, status_code=409, payload=payload)


class UnauthorizedError(AppException):
    """Excepción para accesos no autorizados."""

    def __init__(self, message: str = "No autorizado", payload: dict = None):
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(AppException):
    """Excepción para accesos prohibidos."""

    def __init__(self, message: str = "Acceso prohibido", payload: dict = None):
        super().__init__(message, status_code=403, payload=payload)


class DatabaseError(AppException):
    """Excepción para errores de base de datos."""

    def __init__(self, message: str = "Error en la base de datos", payload: dict = None):
        super().__init__(message, status_code=500, payload=payload)


class BusinessLogicError(AppException):
    """Excepción para errores de lógica de negocio."""

    def __init__(self, message: str = "Error en la lógica de negocio", payload: dict = None):
        super().__init__(message, status_code=422, payload=payload)


def register_error_handlers(app):
    """
    Registra los manejadores de errores globales en la aplicación Flask.

    Args:
        app: Instancia de la aplicación Flask
    """

    @app.errorhandler(AppException)
    def handle_app_exception(error):
        """Manejador para excepciones personalizadas de la aplicación."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Manejador para errores 400 Bad Request."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Solicitud incorrecta",
                "code": 400
            }
        }), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        """Manejador para errores 404 Not Found."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Recurso no encontrado",
                "code": 404
            }
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Manejador para errores 405 Method Not Allowed."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Método no permitido",
                "code": 405
            }
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Manejador para errores 500 Internal Server Error."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Error interno del servidor",
                "code": 500
            }
        }), 500
