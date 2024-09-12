from rest_framework.validators import ValidationError

from django.db.models import QuerySet

from typing import Any, Optional, Union

from decimal import Decimal

from loguru import logger

from .exeptions import DontCorrectFieldTypeValidator
from .validator_utils import get_value, tigger_to_check

from .models import Contact, ProdMap, Product


class RoleValidator:
    """
    Проверка роли
    0 -> только завод,
    1 -> завод, если 0 - завод или другое
    """
    requires_context = True
    FACTORY = 'factory'

    def __init__(self,
                 current_obj: str,
                 supplier: str,
                 ) -> None:
        if not isinstance(current_obj, str):
            raise DontCorrectFieldTypeValidator(
                f'{current_obj} должен быть строкой',
                )
        if not isinstance(supplier, str):
            raise DontCorrectFieldTypeValidator(
                f'{supplier} должен быть строкой',
                )
        self.current_obj = current_obj
        self.supplier = supplier

    @logger.catch
    def _check_role(self,
                    current_obj: Contact,
                    supplier: Optional[ProdMap],
                    ):
        """Проверка аерархии ролей
        """
        role = current_obj.role
        if supplier:
            supplier_role = supplier.current_obj.role
            if role == self.FACTORY and supplier_role != self.FACTORY:
                raise ValidationError(
                    dict(
                        prod_object=f'Завод может быть первым по иерархии или идти после завода',
                        ),
                    )
        else:
            if role != self.FACTORY:
                raise ValidationError(
                    dict(
                        prod_object=f'Первым в иерархии может быть только завод',
                        ),
                    )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.current_obj, self.supplier)
        if need_check:
            current_obj = get_value(self.current_obj, attrs, serializer)
            supplier = get_value(self.supplier, attrs, serializer)
            self._check_role(current_obj=current_obj,
                             supplier=supplier)


class DutyCheckValidator:
    """
    Валидатор проверки долга
    """
    
    def __init__(self,
                 duty: str,
                 ) -> None:
        if not isinstance(duty, str):
            raise DontCorrectFieldTypeValidator(
                f'{duty} должен быть строкой',
                )
        self.duty = duty

    @logger.catch
    def _check_duty_decimal(self,
                            duty: Decimal,
                            ):
        if duty is not None:
            if duty < 0:
                raise ValidationError(
                    dict(duty='Значение не может быть меньше нуля'),
                )
        else:
            raise ValidationError(
                dict(duty='Значение не может быть пустым')
            )

    def __call__(self, attrs) -> Any:
        if self.duty in attrs:
            duty = attrs['duty']
            self._check_duty_decimal(duty=duty)


class ProductListValidator:
    """
    Валидатор списка товаров
    """
    requires_context = True

    def __init__(self,
                 products: str,
                 supplier: str,
                 ) -> None:
        if not isinstance(products, str):
            raise DontCorrectFieldTypeValidator(
                f'{products} должен быть строкой',
                )
        if not isinstance(supplier, str):
            raise DontCorrectFieldTypeValidator(
                f'{supplier} должен быть строкой',
                )
        self.products = products
        self.supplier = supplier

    @logger.catch(reraise=True)
    def _handle_queryset_to_pk_set(self,
                                    supplier_products: QuerySet[Product],
                                    ) -> set[int]:
        list_of_pk = (item[0] for item in supplier_products.values_list('pk'))
        return set(list_of_pk)

    @logger.catch(reraise=True)
    def _get_sets_to_check(self,
                           products: Union[list[int], QuerySet[Product]],
                           supplier_products: QuerySet[Product],
                           ) -> tuple[set[int]]:
        set_of_supp_prod = self._handle_queryset_to_pk_set(supplier_products)
        if isinstance(products, QuerySet):
            set_of_prod = self._handle_queryset_to_pk_set(products)
        else:
            set_of_prod = set(products)
        return set_of_prod, set_of_supp_prod

    @logger.catch(reraise=True)
    def _check_correct_list_products(self,
                                     products: list[int],
                                     supplier_products: QuerySet[Product],
                                     ):
        products, supplier_products = self._get_sets_to_check(
            products=products,
            supplier_products=supplier_products,
        )
        logger.debug(f'ProductListValidator: products: {products}')
        logger.debug(f'ProductListValidator: supplier_products: {supplier_products}')
        has_extra_products = products - supplier_products
        if has_extra_products:
            raise ValidationError(
                dict(products='Вы можете указать только те продукты которые есть у поставщика')
            )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.products, self.supplier)
        if need_check:
            products = get_value(self.products, attrs, serializer)
            supplier = get_value(self.supplier, attrs, serializer)
            if supplier:
                supplier_products = supplier.products.all()
                logger.debug(f'ProductListValidator: attrs {attrs}')
                self._check_correct_list_products(products=products,
                                                  supplier_products=supplier_products,
                                                  )
