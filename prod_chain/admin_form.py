from typing import Any
from django import forms

from loguru import logger

from .validators import RoleValidator, DutyCheckValidator, ProductListValidator


class ProdMapAdminForm(forms.ModelForm):
    """
    Форма для админ панели
    """
    def clean(self) -> dict[str, Any]:
        logger.debug(f'ProdMapAdminForm get attrs {self.cleaned_data}')
        if any(self.errors):
            return
        
        role_validator = RoleValidator('prod_object',
                                       'supplier',
                                       self,
                                       )
        duty_validator = DutyCheckValidator('duty',
                                            self,
                                            )
        product_validator = ProductListValidator('products',
                                                 'supplier',
                                                 self,
                                                 )
        role_validator(self.cleaned_data,
                       self.instance,
                       )
        duty_validator(self.cleaned_data)
        product_validator(self.cleaned_data,
                          self.instance,
                          )
