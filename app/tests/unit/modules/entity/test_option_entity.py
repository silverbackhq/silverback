"""
Option Entity Test Cases
"""

from django.test import TestCase
from app.modules.entity.option_entity import Option_Entity


class Test_Option_Entity(TestCase):

    def test_insert_one(self):
        option_entity = Option_Entity()
        option = option_entity.insert_one({
            "key": "key1",
            "value": "value1",
            "autoload": True
        })
        self.assertTrue(option)
        self.assertTrue(option.id > 1)

    def test_insert_many(self):
        option_entity = Option_Entity()
        self.assertTrue(option_entity.insert_many([
            {"key": "key2", "value": "value2", "autoload": False},
            {"key": "key3", "value": "value3"},
            {"key": "key4", "value": "value4", "autoload": True},
            {"key": "key5", "value": "value5", "autoload": True}
        ]))

    def test_get_one_by_id(self):
        option_entity = Option_Entity()
        option = option_entity.insert_one({
            "key": "key6",
            "value": "value6",
            "autoload": True
        })

        self.assertEqual(option_entity.get_one_by_id(option.id), option)
        self.assertEqual(option_entity.get_one_by_id(option.id).key, "key6")
        self.assertFalse(option_entity.get_one_by_id(1000))

    def test_get_one_by_key(self):
        option_entity = Option_Entity()
        option = option_entity.insert_one({
            "key": "key7",
            "value": "value7",
            "autoload": True
        })
        self.assertEqual(option_entity.get_one_by_key("key7"), option)
        self.assertEqual(option_entity.get_one_by_key("key7").key, "key7")
        self.assertFalse(option_entity.get_one_by_key("not_found_key"))

    def test_get_many_by_autoload(self):
        option_entity = Option_Entity()
        self.assertTrue(option_entity.insert_many([
            {"key": "key2", "value": "value2", "autoload": False},
            {"key": "key3", "value": "value3"},
            {"key": "key4", "value": "value4", "autoload": True},
            {"key": "key5", "value": "value5", "autoload": True}
        ]))
        self.assertEqual(option_entity.get_many_by_autoload(True).count(), 2)
        self.assertEqual(option_entity.get_many_by_autoload(False).count(), 2)

    def test_update_value_by_id(self):
        option_entity = Option_Entity()
        option = option_entity.insert_one({
            "key": "key8",
            "value": "value8",
            "autoload": True
        })
        self.assertTrue(option_entity.update_value_by_id(option.id, "new_value8"))
        self.assertFalse(option_entity.update_value_by_id(700, "new_value8"))

    def test_update_value_by_key(self):
        option_entity = Option_Entity()
        option_entity.insert_one({
            "key": "key9",
            "value": "value9",
            "autoload": True
        })
        self.assertTrue(option_entity.update_value_by_key("key9", "new_value9"))
        self.assertFalse(option_entity.update_value_by_key("not_found_key", "new_value9"))

    def test_delete_one_by_id(self):
        option_entity = Option_Entity()
        option = option_entity.insert_one({
            "key": "key10",
            "value": "value10",
            "autoload": True
        })
        self.assertTrue(option_entity.delete_one_by_id(option.id))
        self.assertFalse(option_entity.delete_one_by_id(600))

    def test_delete_one_by_key(self):
        option_entity = Option_Entity()
        option_entity.insert_one({
            "key": "key11",
            "value": "value11",
            "autoload": True
        })
        self.assertTrue(option_entity.delete_one_by_key("key11"), 1)
        self.assertFalse(option_entity.delete_one_by_key("key12"))
