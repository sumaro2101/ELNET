from rest_framework.validators import ValidationError

from django.db.models import QuerySet, Model
from django import forms

from typing import Any, List, Optional, Union

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

    @logger.catch(reraise=True)
    def __init__(self,
                 current_obj: str,
                 supplier: str,
                 admin_form: Optional[forms.ModelForm] = None,
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
        self.admin_form = admin_form

    @logger.catch(reraise=True, exclude=ValidationError)
    def _check_role(self,
                    current_obj: Contact,
                    supplier: Optional[ProdMap],
                    admin_form: Optional[forms.ModelForm],
                    ):
        """Проверка аерархии ролей
        """
        role = current_obj.role
        logger.debug(f'{self.__class__.__name__} get role: {role} and supplier: {supplier}')
        if supplier:
            supplier_role = supplier.prod_object.role
            logger.debug(f'{self.__class__.__name__} get supplier_role: {supplier_role}')
            if role == self.FACTORY and supplier_role != self.FACTORY:
                if not admin_form:
                    raise ValidationError(
                        dict(
                            prod_object=f'Завод может быть первым по иерархии или идти после завода',
                            ),
                        )
                else:
                    admin_form.add_error(self.current_obj,
                                         forms.ValidationError(
                                             'Завод может быть первым по иерархии или идти после завода',
                                             ),
                                         )
        else:
            if role != self.FACTORY:
                if not admin_form:
                    raise ValidationError(
                        dict(
                            prod_object=f'Первым в иерархии может быть только завод',
                            ),
                        )
                else:
                    admin_form.add_error(self.current_obj,
                                        forms.ValidationError(
                                            'Первым в иерархии может быть только завод',
                                            ),
                                        )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.current_obj, self.supplier)
        if need_check:
            current_obj = get_value(self.current_obj, attrs, serializer)
            supplier = get_value(self.supplier, attrs, serializer)
            self._check_role(current_obj=current_obj,
                             supplier=supplier,
                             admin_form=self.admin_form)


class DutyCheckValidator:
    """
    Валидатор проверки долга
    """

    @logger.catch(reraise=True)
    def __init__(self,
                 duty: str,
                 admin_form: Optional[forms.ModelForm] = None,
                 ) -> None:
        if not isinstance(duty, str):
            raise DontCorrectFieldTypeValidator(
                f'{duty} должен быть строкой',
                )
        self.duty = duty
        self.admin_form = admin_form

    @logger.catch(reraise=True, exclude=ValidationError)
    def _check_duty_decimal(self,
                            duty: Decimal,
                            admin_form: forms.ModelForm,
                            ):
        logger.debug(f'{self.__class__.__name__} get value duty: {duty}')
        if duty is not None:
            if duty < 0:
                if not admin_form:
                    raise ValidationError(
                        dict(duty='Значение не может быть меньше нуля'),
                    )
                else:
                    admin_form.add_error(self.duty,
                                         forms.ValidationError('Значение не может быть меньше нуля'))
        else:
            if not admin_form:
                raise ValidationError(
                    dict(duty='Значение не может быть пустым')
                )
            else:
                admin_form.add_error(self.duty,
                                         forms.ValidationError('Значение не может быть пустым'))

    def __call__(self, attrs) -> Any:
        if self.duty in attrs:
            duty = attrs['duty']
            self._check_duty_decimal(duty=duty,
                                     admin_form=self.admin_form,
                                     )


class ProductListValidator:
    """
    Валидатор списка товаров
    """
    requires_context = True

    @logger.catch(reraise=True)
    def __init__(self,
                 products: str,
                 supplier: str,
                 admin_form: Optional[forms.ModelForm] = None,
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
        self.admin_form = admin_form

    @logger.catch(reraise=True)
    def _handle_queryset_to_pk_set(self,
                                    supplier_products: Union[QuerySet[Product],
                                                             List[Model]],
                                    ) -> set[int]:
        if isinstance(supplier_products, list):
            list_of_pk = (item.pk for item in supplier_products)
        else:
            list_of_pk = (item[0] for item in supplier_products.values_list('pk'))
        return set(list_of_pk)

    @logger.catch(reraise=True)
    def _get_sets_to_check(self,
                           products: Union[list[int], QuerySet[Product]],
                           supplier_products: QuerySet[Product],
                           ) -> tuple[set[int]]:
        set_of_supp_prod = self._handle_queryset_to_pk_set(supplier_products)
        if isinstance(products, (QuerySet, List)):
            set_of_prod = self._handle_queryset_to_pk_set(products)
        else:
            set_of_prod = set(products)
        return set_of_prod, set_of_supp_prod

    @logger.catch(reraise=True, exclude=ValidationError)
    def _check_correct_list_products(self,
                                     products: list[int],
                                     supplier_products: QuerySet[Product],
                                     admin_form: forms.ModelForm,
                                     ):
        products, supplier_products = self._get_sets_to_check(
            products=products,
            supplier_products=supplier_products,
        )
        logger.debug(f'{self.__class__.__name__}: products: {products}')
        logger.debug(f'{self.__class__.__name__}: supplier_products: {supplier_products}')
        has_extra_products = products - supplier_products
        if has_extra_products:
            if not admin_form:
                raise ValidationError(
                    dict(products='Вы можете указать только те продукты которые есть у поставщика')
                )
            else:
                admin_form.add_error(self.products,
                                     forms.ValidationError(
                                         'Вы можете указать только те продукты которые есть у поставщика',
                                         ),
                                     )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.products, self.supplier)
        if need_check:
            products = get_value(self.products, attrs, serializer)
            supplier = get_value(self.supplier, attrs, serializer)
            if supplier:
                supplier_products = supplier.products.all()
                logger.debug(f'{self.__class__.__name__}: attrs {attrs}')
                self._check_correct_list_products(products=products,
                                                  supplier_products=supplier_products,
                                                  admin_form=self.admin_form
                                                  )
