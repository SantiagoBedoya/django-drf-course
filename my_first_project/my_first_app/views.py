from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Car

# Create your views here.
class CarListView(TemplateView):
    template_name = "my_first_app/car_list.html"

    def get_context_data(self):
        car_list = Car.objects.all()
        return {
            "car_list": car_list
        }

def my_view(request):
    car_list = Car.objects.all()
    context = {
        "car_list": car_list
    }
    return render(request, "my_first_app/car_list.html", context)


def my_test_view(request, *args, **kwargs):
    print("args:", args)
    print("kwargs", kwargs)
    return HttpResponse("")
