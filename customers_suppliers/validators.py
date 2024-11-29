from django.core.exceptions import ValidationError


class CustomValidators:
    @staticmethod
    def vadate_inn(value):
        """Проверка ИНН на корректность"""
        if not value.isdigit() or len(value) not in [10, 12]:
            raise ValidationError('Инн должен состоять из 10 или 12 цифр')
    
    @staticmethod
    def validate_phone(value):
        """Проверка номера телефона на корректность"""
        if not value.isdigit() or len(value) < 10:
            raise ValidationError('Номер телефона должен содержать не менее 10 цифр')
        
    @staticmethod
    def validate_kpp_for_ooo(supplier):
        """Проверка КПП для ООО"""
        if supplier.supplier_type == 'OOO' and not supplier.kpp:
            raise ValidationError('Поле КПП обязательно для поставщиков типа "ООО".')
        
    @staticmethod
    def validate_kpp_for_ooo_serializer(attrs):
        """Проверка КПП для ООО"""
        supplier_type = attrs.get('supplier_type')
        kpp = attrs.get('kpp')
    
        if supplier_type == 'OOO' and not kpp:
            raise ValidationError('Поле КПП обязательно для поставщиков типа "ООО".')