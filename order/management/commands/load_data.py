import logging
from django.core.management.base import BaseCommand
import yaml
from order.models import Category, Product, ProductInfo, Parameter, ProductParameter
from customers_suppliers.models import Supplier

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='load_data.log', encoding='utf-8')
logger = logging.getLogger(__name__)
logger.info('Логирование настроено успешно.')

class Command(BaseCommand):
    help = 'Загрузка данных из YAML файла'

    def handle(self, *args, **kwargs):
        try:
            with open(r'shop1.yaml', 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                logger.info('YAML файл успешно загружен.')

            # Загрузка категорий
            for category in data['categories']:
                category_obj, created = Category.objects.get_or_create(id=category['id'], name=category['name'])
                if created:
                    logger.info(f'Создана новая категория: {category_obj.name} (ID: {category_obj.id})')
                else:
                    logger.info(f'Категория уже существует: {category_obj.name} (ID: {category_obj.id})')

            # Загрузка товаров
            for good in data['goods']:
                category = Category.objects.get(id=good['category'])
                product, created = Product.objects.get_or_create(
                    id=good['id'],
                    name=good['name'],
                    category=category
                )
                if created:
                    logger.info(f'Создан новый продукт: {product.name} (ID: {product.id})')
                else:
                    logger.info(f'Продукт уже существует: {product.name} (ID: {product.id})')

                # Загрузка информации о продукте для каждого магазина
                for shop in data.get('shop', []):  # Проходим по каждому магазину
                    try:
                        supplier = Supplier.objects.get(id=shop['id'])  # Получаем экземпляр поставщика
                        product_info = ProductInfo.objects.create(
                            model=good['model'],
                            external_id=good['id'],
                            product=product,
                            shop=supplier,  # Используем экземпляр поставщика
                            quantity=good['quantity'],
                            price=good['price'],
                            price_rrc=good['price_rrc']
                        )
                        logger.info(f'Создана информация о продукте для: {product.name} (ID: {product.id}) в магазине {supplier.name_organization}')

                        # Загрузка параметров продукта
                        parameters = good.get('parameters', {})
                        for param_name, param_value in parameters.items():
                            parameter, created = Parameter.objects.get_or_create(name=param_name)
                            ProductParameter.objects.create(
                                product_info=product_info,
                                parameter=parameter,
                                value=param_value
                            )
                            logger.info(f'Создан параметр {param_name} со значением {param_value} для продукта {product.name}')

                    except Supplier.DoesNotExist:
                        logger.error(f'Поставщик с ID {shop["id"]} не найден.')

            self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
            logger.info('Данные успешно загружены!')

        except Exception as e:
            logger.error(f'Произошла ошибка: {e}')
            self.stdout.write(self.style.ERROR('Произошла ошибка при загрузке данных. Проверьте лог для получения деталей.'))