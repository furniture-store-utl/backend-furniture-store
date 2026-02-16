"""
Utilidades para respuestas HTTP estandarizadas.

Este módulo proporciona funciones helper para generar respuestas
JSON consistentes en toda la API.
"""

from typing import Any, Optional

from flask import jsonify, Response


def success_response(
        data: Any = None,
        message: str = "Operación exitosa",
        status_code: int = 200
) -> tuple[Response, int]:
    """
    Genera una respuesta de éxito estandarizada.

    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje descriptivo de la operación
        status_code: Código HTTP de la respuesta

    Returns:
        Tuple con la respuesta JSON y el código de estado
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code


def error_response(
        message: str = "Ha ocurrido un error",
        status_code: int = 400,
        details: Optional[dict] = None
) -> tuple[Response, int]:
    """
    Genera una respuesta de error estandarizada.

    Args:
        message: Mensaje descriptivo del error
        status_code: Código HTTP del error
        details: Detalles adicionales del error

    Returns:
        Tuple con la respuesta JSON y el código de estado
    """
    response = {
        "success": False,
        "error": {
            "message": message,
            "code": status_code
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code


def paginated_response(
        data: list,
        page: int,
        per_page: int,
        total: int,
        message: str = "Datos obtenidos exitosamente"
) -> tuple[Response, int]:
    """
    Genera una respuesta paginada estandarizada.

    Args:
        data: Lista de datos de la página actual
        page: Número de página actual
        per_page: Elementos por página
        total: Total de elementos
        message: Mensaje descriptivo de la operación

    Returns:
        Tuple con la respuesta JSON y código 200
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    response = {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
    return jsonify(response), 200
