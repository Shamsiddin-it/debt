from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Debt, ReturnDebt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect,render
from django.shortcuts import render
from django.http import HttpResponse
from .sms_utils import send_sms
from django.db.models import Sum
from django.core.management import call_command
from django.http import JsonResponse
from django.views import View

class RunMigrationsView(View):
    def get(self, request, *args, **kwargs):
        try:
            call_command('makemigrations')
            call_command('migrate')
            call_command('migrate sessions')
            return JsonResponse({'status': 'success', 'message': 'Migrations applied successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class DebtListView(ListView):
    model = Debt
    template_name = 'debts/debt_list.html'
    context_object_name = 'debts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_debt = Debt.objects.aggregate(Sum('amount'))['amount__sum']
        context['total_debt'] = total_debt if total_debt else 0.00  

        debtors = Debt.objects.filter(is_active=True).values('customer_name').distinct().count()
        context['debtors'] = debtors
        return context

class ActiveListView(ListView):
    model = Debt
    template_name = 'actives.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actives = Debt.objects.filter(is_active = True).all()
        context["actives"] = actives
        return context

class PaidListView(ListView):
    model = Debt
    template_name = 'paids.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paids = Debt.objects.filter(is_active = False).all()
        context["paids"] = paids
        return context
    
class DebtDetailView(DetailView):
    model = Debt
    template_name = 'debts/debt_detail.html'
    context_object_name = 'debt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        debt = self.get_object()
        context['payments'] = ReturnDebt.objects.filter(debt=debt)
        return context

class DebtCreateView(CreateView):
    model = Debt
    fields = ['customer_name', 'amount', 'description','duration_date']
    template_name = 'debts/debt_form.html'
    success_url = reverse_lazy('debt_list')
    def form_valid(self, form):
        debt = form.save(commit=False)
        debt.user = self.request.user
        return super().form_valid(form)
    

class ReturnDebtCreateView(CreateView):
    model = ReturnDebt
    fields = ['amount']
    template_name = 'debts/return_debt_form.html'


    def form_valid(self, form):
        debt = get_object_or_404(Debt, pk=self.kwargs['pk'])
        payment = form.save(commit=False)
        payment.debt = debt
        if payment.payback():
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('debt_detail', kwargs={'pk': self.kwargs['pk']})

class HomeView(TemplateView):
    template_name = "home.html"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def send_sms_view(request, pk):
    debt = Debt.objects.get(id=pk)
    to_phone_number = '+992907708429'  
    message = f"The {debt.customer_name}, have to pay owe {debt.amount} for {debt.description}."
    if send_sms(to_phone_number, message):
        return HttpResponse("SMS sent successfully!")
    else:
        return HttpResponse("Failed to send SMS.")

