from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.decorators import method_decorator
from django.utils.html import format_html

from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.widgets import FileInput, Textarea
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from docx import *

from .models import Wine, Shelf, Cabinet
from .forms import UserRegisterForm, WineForm, FileUploadForm

def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parse_docx(filename):
    doc = Document(filename)
    data_dict = []
    for table in doc.tables:
        table_dict = {}
        for row in table.rows:
            data = [cell.text for cell in row.cells]
            table_dict[f"{data[0]}"] = data[1]
        data_dict.append(table_dict)
    print(data_dict)
    return data_dict



class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'auth/login.html'
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f"Добро пожаловать, сомелье!")
        if self.request.POST.get('next'):
            valuenext = self.request.POST.get('next')
        else:
            valuenext = reverse("home")
        context = {"form": form, 'valuenext': valuenext}
        super().form_valid(form)
        return redirect(valuenext)
    
    def form_invalid(self, form):
        messages.error(self.request, "Логин или пароль неверны")
        return self.render_to_response(self.get_context_data(form=form))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('home')
        else:
            form = UserRegisterForm()
            messages.info(request, "Пароли не совпадают! Проверить правильность введения")
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли из аккаунта")
        return super().dispatch(request, *args, **kwargs)

def relogin(request):
    logout(request)
    return redirect("login")



def create_wine(request):
    if request.method == 'POST':
        if 'submit_form' in request.POST:
            form = WineForm(data=request.POST)
            if form.is_valid():
                wine = form.save(commit=True)
                return redirect(f'/wine/{wine.wine_id}', {'wine': wine})
            if request.POST.get('next'):
                valuenext = request.POST.get('next')
            else:
                valuenext = reverse("profile")
            return redirect(valuenext)
        if 'upload_file' in request.POST:
            form = FileUploadForm(request.POST, request.FILES)
            data = parse_docx(request.FILES["file"])
            for item in data:
                new_wine = Wine.objects.create(shelf_id=Shelf.objects.get(id=8))
                for k, v in item.items():
                    setattr(new_wine, k, v)
                new_wine.save()
            form = WineForm()
            form_uf = FileUploadForm()
            messages.info(request, format_html("Загруженные карточки добавлены в \"Карточки для редакции\". <a href=\"\"> Перейти </a>"))
            return render(request, 'wine/wine_create.html',  {'form': form, 'form_uf': form_uf})
    else:
        form = WineForm()
        form_uf = FileUploadForm()
    return render(request, 'wine/wine_create.html', {'form': form, 'form_uf': form_uf})

@method_decorator(login_required, name='dispatch')
class WineDeleteView(SuccessMessageMixin, DeleteView):
    model = Wine

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Wine, wine_id=self.kwargs.get('wine_id'))
        messages.success(request, 'Карточка удалена!')
        obj.delete()
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class WineUpdateView(SuccessMessageMixin, UpdateView):
    model = Wine
    pk_url_kwarg = 'wine_id'
    template_name = 'wine/wine_edit.html'
    fields = ('shelf_id','winery', 'wine_name', 'amount', 'crop_year', 'region', 'fragrance', 'grape', 'taste', 'fun_facts', 'wine_image')
    success_message = "Карточка изменена!"

    def get_form(self, form_class=None):
        form = super(WineUpdateView, self).get_form(form_class)
        form.fields['wine_image'].widget = FileInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wine'] = Wine.objects.get(wine_id=self.kwargs["wine_id"])
        return context
    
    def get_success_url(self):
        pk = self.kwargs["wine_id"]
        return reverse("show_wine", kwargs={"wine_id": pk})

def show_wine(request, wine_id):
    wine = Wine.objects.get(wine_id=wine_id)
    wine_fun_facts = [item for item in wine.fun_facts.replace("\r", "").split("\n") if item]
    return render(request, "wine/wine_show.html", {"wine": wine, "wine_fun_facts": wine_fun_facts, "item": "wine"})



def show_shelf(request, id):
    shelf = Shelf.objects.get(id=id)
    wines = list(Wine.objects.filter(shelf_id=shelf))
    wines = list(partition(wines, 3))
    p = Paginator(wines, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "shelf/shelf_show.html", {"shelf": shelf, 'page_obj': page_obj})

@method_decorator(login_required, name='dispatch')
class ShelfCreateView(SuccessMessageMixin, CreateView):
    model = Shelf
    fields =  ('title', 'cabinet', 'description')
    success_message = "Полка создана успешно!"
    
    def get_success_url(self):
        return reverse("home")
    
    def get_form(self, form_class=None):
        form = super(ShelfCreateView, self).get_form(form_class)
        form.fields['description'].widget = Textarea()
        form.fields['cabinet'].empty_label = "Не выбрано"
        return form

@method_decorator(login_required, name='dispatch')
class ShelfUpdateView(SuccessMessageMixin, UpdateView):
    model = Shelf
    pk_url_kwarg = 'id'
    fields =  ('title', 'cabinet', 'description')
    template_name = "shelf/shelf_edit.html"
    success_message = "Полка изменена!"

    def get_form(self, form_class=None):
        form = super(ShelfUpdateView, self).get_form(form_class)
        form.fields['description'].widget = Textarea()
        form.fields['cabinet'].empty_label = "Не выбрано"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelf'] = Shelf.objects.get(id=self.kwargs["id"])
        return context
    
    def get_success_url(self):
        pk = self.kwargs["id"]
        return reverse("show_shelf", kwargs={"id": pk})

@method_decorator(login_required, name='dispatch')
class ShelfDeleteView(SuccessMessageMixin, DeleteView):
    model = Shelf

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Shelf, id=self.kwargs.get('id'))
        messages.success(request, 'Полка удалена!')
        obj.delete()
        return redirect('home')



@method_decorator(login_required, name='dispatch')
class CabinetCreateView(SuccessMessageMixin, CreateView):
    model = Cabinet
    fields =  "__all__"
    success_message = "Шкаф создан успешно!"
    
    def get_success_url(self):
        return reverse("home")
    
    def get_form(self, form_class=None):
        form = super(CabinetCreateView, self).get_form(form_class)
        return form

@method_decorator(login_required, name='dispatch')
class CabinetUpdateView(SuccessMessageMixin, UpdateView):
    model = Cabinet
    pk_url_kwarg = 'id'
    fields =  ('title', 'description')
    template_name = "cabinet/cabinet_edit.html"
    success_message = "Шкаф изменен!"

    def get_form(self, form_class=None):
        form = super(CabinetUpdateView, self).get_form(form_class)
        form.fields['description'].widget = Textarea()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cabinet'] = Cabinet.objects.get(id=self.kwargs["id"])
        return context
    
    def get_success_url(self):
        pk = self.kwargs["id"]
        return reverse("cabinet_show", kwargs={"id": pk})

def show_cabinet(request, id):
    cabinet = Cabinet.objects.get(id=id)
    shelfs = Shelf.objects.filter(cabinet=cabinet.id)
    shelfs = list(partition(shelfs, 3))
    return render(request, "cabinet/cabinet_show.html", {"shelfs": shelfs, "cabinet": cabinet})

@method_decorator(login_required, name='dispatch')
class CabinetDeleteView(SuccessMessageMixin, DeleteView):
    model = Cabinet

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Cabinet, id=self.kwargs.get('id'))
        messages.success(request, 'Шкаф удален!')
        obj.delete()
        return redirect('home')


@login_required
def profile(request):
    wines = Wine.objects.all()
    shelfs = Shelf.objects.all()
    cabinets = Cabinet.objects.all()
    wines_redacted = Wine.objects.filter(shelf_id=Shelf.objects.get(id=8))
    context = {"wines": wines, 
               "shelfs": shelfs,
               "cabinets": cabinets,
               "wines_redacted": wines_redacted}
    
    return render(request, 'profile.html', context=context)

def homepage(request):
    cabinets = list(Cabinet.objects.all())
    cabinets = list(partition(cabinets, 3))
    return render(request, "homepage.html", {'cabinets': cabinets})

@login_required
def download_file(request):
    import os
    filename = "Example.docx"
    filepath = os.getcwd() + "\\vine_app\\media\\test.docx"
    
    fl = open(filepath, 'rb')
    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    mime_type="pain/text"

    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response

@login_required
def wine_list(request):
    wines = list(Wine.objects.exclude(shelf_id=Shelf.objects.get(id=8)))
    wines = list(partition(wines, 3))
    p = Paginator(wines, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "wine/wine_list.html", {'page_obj': page_obj, 'title': "Все вина"})

@login_required
def editable_wine_list(request):
    wines = list(Wine.objects.filter(shelf_id=8))
    wines = list(partition(wines, 3))
    p = Paginator(wines, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "wine/wine_list.html", {'page_obj': page_obj, 'title': "Все вина для редакции"})

@login_required
def search(request):
    wines = ""
    if request.method == "GET":
        query = request.GET.get('search', None)
        if not query:
            return redirect("wine_list")
        else:
            wines = Wine.objects.filter(Q(wine_name__icontains=query))
        wines = list(partition(wines, 3))
        p = Paginator(wines, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        return render(request, "wine/wine_list.html", {'page_obj': page_obj, 'title': f"Результаты поиска \"{query}\""})


@login_required
def shelf_list(request):
    shelfs = list(Shelf.objects.exclude(id=8))
    shelfs = list(partition(shelfs, 3))
    p = Paginator(shelfs, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "shelf/shelf_list.html", {'page_obj': page_obj})

@login_required
def cabinet_list(request):
    cabinets = list(Cabinet.objects.exclude())
    cabinets = list(partition(cabinets, 3))
    p = Paginator(cabinets, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "cabinet/cabinet_list.html", {'page_obj': page_obj})