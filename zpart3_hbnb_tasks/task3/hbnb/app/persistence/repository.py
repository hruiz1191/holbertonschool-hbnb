from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, obj):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Agrega un objeto al almacenamiento."""
        if not hasattr(obj, "id"):
            print("[ERROR] El objeto agregado no tiene un atributo 'id'.")
            return
        self._storage[obj.id] = obj
        print(f"[DEBUG] Objeto agregado al almacenamiento con ID: {obj.id}")
        print(f"[DEBUG] Estado actual del almacenamiento: {self._storage}")

    def get(self, obj_id):
        """Obtiene un objeto por su ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Obtiene todos los objetos almacenados."""
        return list(self._storage.values())

    def update(self, obj_id, obj):
        """Actualiza un objeto en el almacenamiento."""
        if obj_id in self._storage:
            self._storage[obj_id] = obj

    def delete(self, obj_id):
        """Elimina un objeto del almacenamiento."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_user_by_email(self, email):
        """Busca un usuario por email en el almacenamiento."""
        print(f"[DEBUG] Buscando usuario con email: {email}")
        print(f"[DEBUG] Contenido actual del almacenamiento: {self._storage}")

        for user in self._storage.values():
            if getattr(user, 'email', None) == email:
                print(f"[DEBUG] Usuario encontrado: {user.to_dict()}")
                return user

        print(f"[DEBUG] Usuario con email {email} NO encontrado.")
        return None

    def get_review_by_user_and_place(self, user_id, place_id):
        """Busca si un usuario ya ha reseñado un lugar."""
        for review in self._storage.values():
            if getattr(review, 'user_id', None) == user_id and getattr(review, 'place_id', None) == place_id:
                return review
        return None

