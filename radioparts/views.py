from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import RadioPart, CartItem

# Custom LoginView if you need custom behavior
class CustomLoginView(LoginView):
    template_name = 'radioparts/login.html'

# Custom RegistrationView
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'radioparts/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'radioparts/register.html', {'form': form})

# View to list all radio parts
class PartsListView(View):
    def get(self, request):
        parts = RadioPart.objects.all()
        return render(request, 'parts_list.html', {'parts': parts})

# View to add a radio part to the cart
class AddToCartView(View):
    def post(self, request, pk):
        part = RadioPart.objects.get(pk=pk)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, part=part)
        return redirect('parts-list')

# View to remove a radio part from the cart
class RemoveFromCartView(View):
    def post(self, request, pk):
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.delete()
        return redirect('parts-list')

# Admin view to update radio part detail
@method_decorator(login_required, name='dispatch')
class AdminPartUpdateView(View):
    def get(self, request, pk):
        part = RadioPart.objects.get(pk=pk)
        return render(request, 'admin_part_update.html', {'part': part})

    def post(self, request, pk):
        part = RadioPart.objects.get(pk=pk)
        # Update part details based on form data
        return redirect('parts-list')
