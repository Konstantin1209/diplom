from django.utils.deprecation import MiddlewareMixin
import json

class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cart_data = request.COOKIES.get('cart')
        if cart_data:
            request.cart = json.loads(cart_data)
        else:
            request.cart = {}

    def process_response(self, request, response):
        if hasattr(request, 'cart'):
            response.set_cookie('cart', json.dumps(request.cart), max_age=3600)  
        return response