from django.shortcuts import render, redirect
from vine_app.models import Wine, Shelf
from django.contrib import messages
from .forms import UserRegisterForm, WineForm, FileUploadForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin

from docx import Document

def parse_docx(filename):
    doc = Document(filename)
    data_dict = {}
    table = doc.tables[0]
    for row in table.rows:
        data = [cell.text for cell in row.cells]
        data_dict[f"{data[0]}"] = data[1]
    print(data_dict)
    return data_dict

def create_wine(request):
    if request.method == 'POST':
        if 'submit_form' in request.POST:
            print(request.POST)
            form = WineForm(data=request.POST)
            if form.is_valid():
                wine = form.save(commit=True)
                return redirect(f'/wine/{wine.wine_id}', {'wine': wine})
            return redirect('/profile/')
        if 'upload_file' in request.POST:
            form = FileUploadForm(request.POST, request.FILES)
            data = parse_docx(request.FILES["file"])
            form = WineForm(data=data)
            form_uf = FileUploadForm()
            return render(request, 'wine_create.html',  {'form': form, 'form_uf': form_uf})
    else:
        form = WineForm()
        form_uf = FileUploadForm()
    return render(request, 'wine_create.html', {'form': form, 'form_uf': form_uf})

@method_decorator(login_required, name='dispatch')
class WineDeleteView(SuccessMessageMixin, DeleteView):
    model = Wine
    pk_url_kwarg = 'wine_id'
    template_name = 'wine_delete.html'
    success_message = "Карточка удалена!"
    success_url = reverse_lazy('profile')

@method_decorator(login_required, name='dispatch')
class WineUpdateView(SuccessMessageMixin, UpdateView):
    model = Wine
    pk_url_kwarg = 'wine_id'
    template_name = 'wine_edit.html'
    fields = ('winery', 'crop_year', 'region', 'fragrance', 'taste', 'fun_facts', 'wine_image')
    success_message = "Карточка изменена!"
    
    def get_success_url(self):
           pk = self.kwargs["wine_id"]
           return reverse("show_wine", kwargs={"wine_id": pk})


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
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'profile.html')

def homepage(request):
    shelfs = Shelf.objects.all()
    return render(request, "homepage.html", {"shelfs": shelfs})

def show_wine(request, wine_id):
    wine = Wine.objects.get(wine_id=wine_id)
    wine_fun_facts = [item for item in wine.fun_facts.split("\n")]
    return render(request, "wine_page.html", {"wine": wine, "wine_fun_facts": wine_fun_facts})

def show_shelf(request, shelf_id):
    wines = Wine.objects.filter(shelf_id=shelf_id)
    shelf = Shelf.objects.get(shelf_id=shelf_id)
    return render(request, "show_shelf.html", {"wines": wines, "shelf": shelf})
