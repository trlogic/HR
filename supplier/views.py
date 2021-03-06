from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import ProfileEditForm, ServiceUseForm
from .models import Supplier, Service
from company.models import Benefit, Employe, Company
import psycopg2


def index(request):
    supplier = Supplier.objects.get(user_id=request.user.id)
    services = Service.objects.filter(supplier_id=supplier.id).all()
    benefits = Benefit.objects.filter(service_id__in=services).all()
    customer = Employe.objects.filter(id__in=benefits.values("employe_id")).all()
    return render(request, 'supplier/index.html', locals(), RequestContext(request))


def customers(request):
    supplier = Supplier.objects.get(user_id=request.user.id)
    sp_id = supplier.id
    try:
        conn = psycopg2.connect("dbname='deneme2' user='postgres' host='localhost' password='123'")
    except:
        print "I am unable to connect to the database"
    cur = conn.cursor()
    cur.execute(
        "SELECT company_employe.id, company_employe.name, company_employe.surname, company_employe.phone_number, company_employe.credit , company_employe.image, supplier_service.name, company_company.name "
        "FROM public.company_employe, public.supplier_service, public.company_company, public.company_benefit WHERE company_benefit.employe_id = company_employe.id "
        "AND company_benefit.service_id = supplier_service.id AND supplier_service.supplier_id = %s "
        "AND company_employe.company_id = company_company.id;", str(sp_id))
    data = cur.fetchall()
    if request.GET:
        search_value = request.GET.get('q')
        cur.execute(
            "SELECT company_employe.id, company_employe.name, company_employe.surname, company_employe.phone_number, company_employe.credit , company_employe.image, supplier_service.name, company_company.name "
            "FROM public.company_employe, public.supplier_service, public.company_company, public.company_benefit WHERE company_benefit.employe_id = company_employe.id "
            "AND company_benefit.service_id = supplier_service.id AND supplier_service.supplier_id = %s "
            "AND company_employe.company_id = company_company.id AND"
            " to_tsvector(company_employe.name || ' ' || company_employe.surname || ' ' || company_employe.phone_number) @@ to_tsquery (%s);",
            (str(sp_id), str(search_value)))
        data = cur.fetchall()
        return render(request, 'supplier/customers.html', locals(), RequestContext(request))
    return render(request, 'supplier/customers.html', locals(), RequestContext(request))


def profile(request):
    supplier = Supplier.objects.get(user_id=request.user.id)
    form = ProfileEditForm(instance=supplier)
    form.helper = form.helper
    if request.method == 'POST':
        if request.user.id:
            form = ProfileEditForm(request.POST, request.FILES, instance=supplier)
        else:
            form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/supplier', locals())
    return render(request, 'supplier/profile.html', locals(), RequestContext(request))


def services(request):
    supplier = Supplier.objects.get(user_id=request.user.id)
    data = Service.objects.filter(supplier_id=supplier.id).all()
    return render(request, 'supplier/services.html', locals())


def service_info(request, pk):
    supplier = Supplier.objects.get(user_id=request.user.id)
    service = Service.objects.get(id=pk)
    benefits = Benefit.objects.filter(service_id=service.id).all()
    employes = Employe.objects.filter(id__in=benefits.values("employe_id")).all()
    companys = Company.objects.filter(id__in=employes.values("company_id")).all()
    return render(request, 'supplier/service_info.html', locals(), RequestContext(request))


def employe_info(request, pk):
    supplier = Supplier.objects.get(user_id=request.user.id)
    employe = Employe.objects.get(id=pk)
    return render(request, 'supplier/employe_info.html', locals(), RequestContext(request))


def service_use(request, pk):
    employe = Employe.objects.get(user_id=request.user.id)
    service = Service.objects.get(id=pk)
    form = ServiceUseForm()
    if request.method == 'POST':
        form = ServiceUseForm(request.POST, request.FILES)
        if form.is_valid():
            usage = form.cleaned_data.get('usage')
            form.save(employe_id=employe.id, usage=usage, service=service, employe=employe)
            return redirect('/supplier', locals())
    return render(request, 'supplier/employe_info.html', locals(), RequestContext(request))
