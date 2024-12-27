import logging


from products.models import ProductInfo
from customers_suppliers.models import Customer
from rest_framework import viewsets




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='load_data.log')
logger = logging.getLogger('basket')




 
