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
        self._storage[obj.id] = obj  # Guarda el objeto completo

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
