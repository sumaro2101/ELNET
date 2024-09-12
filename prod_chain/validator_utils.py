from typing import Any, Dict, List

from rest_framework.serializers import ModelSerializer


def get_value(field: str,
              attrs: Dict,
              serializer: ModelSerializer,
              ) -> Any:
    """
    Функция выполняющая получение значения
    исходя из того что - пользователь желает изменить поле
    или пользователь просто не указал его
    """
    try:
        value = attrs[field]
    except KeyError:
        if serializer.instance:
            instance = serializer.instance
            field = instance._meta.get_field(field)
            value = field.value_from_object(instance)
        else:
            field = instance.model._meta.get_field(field)
            if field.has_default():
                value = field.default
            else:
                value = None

    return value


def tigger_to_check(attrs: Dict,
                    *fields: List,
                    ) -> bool:
    """Тригер если проверка нужна
    """
    need_check = False
    for field in fields:
        if field in attrs.keys():
            need_check = True
    return need_check
