from django.forms import ModelForm

from orders.models import OrderProduct

class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product']
