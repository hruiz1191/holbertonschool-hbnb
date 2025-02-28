import unittest
from app.models.base_model import BaseModel
from datetime import datetime
import uuid

class TestBaseModel(unittest.TestCase):
    def test_instance_creation(self):
        """Verifica que la instancia de BaseModel se crea correctamente"""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)
        self.assertIsInstance(obj.id, str)
        self.assertTrue(uuid.UUID(obj.id))  # Verifica si el ID es un UUID válido
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_save_method(self):
        """Verifica que `save()` actualiza el atributo `updated_at`"""
        obj = BaseModel()
        old_updated_at = obj.updated_at
        obj.save()
        self.assertNotEqual(old_updated_at, obj.updated_at)

    def test_update_method(self):  
        """Verifica que `update()` modifica correctamente los atributos"""
        obj = BaseModel()
        obj.update({"id": "1234"})  # Actualiza un atributo existente
        self.assertEqual(obj.id, "1234")  # Verifica que el cambio se hizo

if __name__ == "__main__":
    unittest.main()  
