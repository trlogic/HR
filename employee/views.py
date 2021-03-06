from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render, redirect
from supplier.models import Service
from company.models import Benefit, Employe, Company_Service, Company
from .forms import ProfileEditForm, CreditTransferForm, ServiceUseForm, ServiceLeaveForm
from usermanage.models import User


def index(request):
    if not request.user.user_type == 'Employe':
        return HttpResponseForbidden('Nope U\'re not Employee!')
    employe = Employe.objects.get(user_id=request.user.id)
    company = Company.objects.get(id=employe.company_id)
    servis = Company_Service.objects.filter(company_id=company.id).all()
    services = Service.objects.filter(id__in=servis.values("service_id"))
    bnf = Benefit.objects.filter(employe_id=employe.id).all()
    used_services = Service.objects.filter(id__in=bnf.values("service_id")).all()
    return render(request, 'employee/index.html', locals(), RequestContext(request))


def services(request):
    if not request.user.user_type == 'Employe':
        return HttpResponseForbidden('Nope U\'re not Employee!')
    employe = Employe.objects.get(user_id=request.user.id)
    bnf = Benefit.objects.filter(employe_id=employe.id).all()
    services = Service.objects.filter(id__in=bnf.values("service_id")).all()
    return render(request, 'employee/services.html', locals(), RequestContext(request))


def profile(request):
    employe = Employe.objects.get(user_id=request.user.id)
    form = ProfileEditForm(instance=employe)
    if request.method == 'POST':
        if request.user.id:
            form = ProfileEditForm(request.POST, request.FILES, instance=employe)
        else:
            form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/employee', locals())
    return render(request, 'employee/profile.html', locals(), RequestContext(request))


def credit_transfer(request):
    employe = Employe.objects.get(user_id=request.user.id)
    form = CreditTransferForm()
    if request.method == 'POST':
        if request.user.id:
            form = CreditTransferForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                value = form.cleaned_data['credit']
                user = User.objects.get(username=username)
                t_employe = Employe.objects.get(user_id=user)
                t_employe.credit += value
                t_employe.save()
                employe.credit -= value
                employe.save()
                return redirect('/employee', locals())
        else:
            form = CreditTransferForm(request.POST)
    return render(request, 'employee/profile.html', locals(), RequestContext(request))


def service_choose(request, pk):
    employe = Employe.objects.get(user_id=request.user.id)
    service = Service.objects.get(id=pk)
    form = ServiceUseForm(instance=employe)
    if request.method == 'POST':
        if request.user.id:
            form =ServiceUseForm(request.POST)
        else:
            form = ServiceUseForm(request.POST)
        if form.is_valid():
            usage = form.cleaned_data.get('usage')
            form.save(employe=employe,usage=usage,service=service)
            return redirect('/employee', locals())
    return render(request, 'employee/service_add.html', locals(), RequestContext(request))


def service_leave(request, pk):
    employe = Employe.objects.get(user_id=request.user.id)
    service = Service.objects.get(id=pk)
    form = ServiceUseForm()
    if Benefit.objects.filter(employe_id=employe.id , service_id = pk).exists():
        benefit = Benefit.objects.get(employe_id=employe.id , service_id = pk)
        if benefit.usage==1:
            benefit.delete()
            return redirect('/employee/services', locals())
        else:
            if request.method == 'POST':
                if request.user.id:
                    form = ServiceLeaveForm(request.POST)
                else:
                    form = ServiceLeaveForm(request.POST)
                if form.is_valid():
                    usage = form.cleaned_data.get('usage')
                    form.save(employe=employe, usage=usage, service=service)
                    return redirect('/employee/services', locals())
    return render(request, 'employee/service_leave.html', locals(), RequestContext(request))



def service_info(request, pk):
    employe = Employe.objects.get(user_id=request.user.id)
    service = Service.objects.get(id=pk)
    bnf = Benefit.objects.filter(employe_id=employe.id).all()
    used_services = Service.objects.filter(id__in=bnf.values("service_id")).all()
    return render(request, 'employee/service_info.html', locals(), RequestContext(request))
