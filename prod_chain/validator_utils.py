from typing import Any, Dict, List

from loguru import logger
from rest_framework.serializers import ModelSerializer


@logger.catch(reraise=True)
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
    logger.debug(f'From func {get_value.__name__} From field {field} get value {value}')
    return value

@logger.catch(reraise=True)
def tigger_to_check(attrs: Dict,
                    *fields: List,
                    ) -> bool:
    """Тригер если проверка нужна
    """
    need_check = False
    for field in fields:
        if field in attrs.keys():
            need_check = True
    logger.debug(f'From func {tigger_to_check.__name__} Need to check - {need_check} for fields {fields} in attrs {attrs}')
    return need_check
