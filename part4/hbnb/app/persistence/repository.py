from app import db
from abc import ABC, abstractmethod

class Repository(ABC):
    """Interfaz base para los repositorios"""

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

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """Implementación del repositorio con SQLAlchemy"""

    def __init__(self, model):
        from app import db  # Importación dentro del constructor para evitar importación circular
        self.db = db
        self.model = model

    def add(self, obj):
        """Agrega un objeto a la base de datos"""
        self.db.session.add(obj)
        self.db.session.commit()

    def get(self, obj_id):
        """Obtiene un objeto por su ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Obtiene todos los objetos de la base de datos"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Actualiza un objeto existente"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.session.commit()

    def delete(self, obj_id):
        """Elimina un objeto por su ID"""
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Obtiene un objeto filtrando por un atributo específico"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

