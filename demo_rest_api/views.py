from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        # Devuelve únicamente los elementos activos
        active_items = [
            item for item in data_list
            if item.get('is_active', False)
        ]

        return Response(
            {
                "message": "Listado de usuarios activos.",
                "data": active_items
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data

        # Validación
        if 'name' not in data or 'email' not in data:
            return Response(
                {
                    "error": "Los campos 'name' y 'email' son obligatorios."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        nuevo = {
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "email": data["email"],
            "is_active": True
        }

        data_list.append(nuevo)

        return Response(
            {
                "message": "Usuario creado correctamente.",
                "data": nuevo
            },
            status=status.HTTP_201_CREATED
        )


class DemoRestApiItem(APIView):

    def _find_item(self, item_id):
        for item in data_list:
            if item.get("id") == item_id:
                return item
        return None

    def put(self, request, id=None):
        data = request.data
        item_id = data.get("id") or id

        if not item_id:
            return Response(
                {"error": "El campo 'id' es obligatorio en el cuerpo de la solicitud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if "name" not in data or "email" not in data:
            return Response(
                {"error": "Los campos 'name' y 'email' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = self._find_item(item_id)
        if item is None:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        item["name"] = data["name"]
        item["email"] = data["email"]
        item["is_active"] = data.get("is_active", item.get("is_active", True))

        return Response(
            {"message": "Elemento reemplazado correctamente.", "data": item},
            status=status.HTTP_200_OK
        )

    def patch(self, request, id=None):
        data = request.data
        item_id = data.get("id") or id

        if not item_id:
            return Response(
                {"error": "El campo 'id' es obligatorio en el cuerpo de la solicitud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not any(field in data for field in ["name", "email", "is_active"]):
            return Response(
                {"error": "Debe enviar al menos uno de los campos: 'name', 'email' o 'is_active'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = self._find_item(item_id)
        if item is None:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if "name" in data:
            item["name"] = data["name"]
        if "email" in data:
            item["email"] = data["email"]
        if "is_active" in data:
            item["is_active"] = data["is_active"]

        return Response(
            {"message": "Elemento actualizado parcialmente.", "data": item},
            status=status.HTTP_200_OK
        )

    def delete(self, request, id=None):
        data = request.data
        item_id = data.get("id") or id

        if not item_id:
            return Response(
                {"error": "El campo 'id' es obligatorio en el cuerpo de la solicitud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = self._find_item(item_id)
        if item is None:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        item["is_active"] = False

        return Response(
            {"message": "Elemento eliminado lógicamente.", "data": item},
            status=status.HTTP_200_OK
        )