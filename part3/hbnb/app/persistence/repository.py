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
        print(f"[DEBUG] Usuario agregado al almacenamiento con ID: {obj.id}")
        print(f"[DEBUG] Almacenamiento actual: {self._storage}")

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, obj):
        if obj_id in self._storage:
            self._storage[obj_id] = obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_user_by_email(self, email):
        """Busca un usuario por email en el almacenamiento."""
        print(f"[DEBUG] Buscando usuario con email: {email}")
        print(f"[DEBUG] Contenido actual del almacenamiento: {self._storage}")

        for user in self._storage.values():
            print(f"[DEBUG] Revisando usuario en almacenamiento: {user.to_dict()}")  
            if getattr(user, 'email', None) == email:
                print(f"[DEBUG] Usuario encontrado: {user.to_dict()}")
                return user

        print(f"[DEBUG] Usuario con email {email} NO encontrado.")
        return None
