from django.shortcuts import render


from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from demo.models import GENERIC_CLASSES

# Create your views here.

def get_navigation_links():
    return [ {'name': cl.NAME, 'url': cl.__name__.lower()+'-list'} for cl in GENERIC_CLASSES]

def index(request):
    return render(request,'home.html', {'NAV_LINKS':get_navigation_links()} )


class GenericCreate(PermissionRequiredMixin,CreateView):
    
    template_name = "generic_form.html"
   
    def dispatch(self, *args, **kwargs):
        self.model = self.kwargs.get('model','')
        self.model_name = self.model.__name__.lower()
        self.form_class = self.kwargs.get('form_class','')
        self.permission_required = 'stock.add_'+self.model_name
        self.success_url = reverse_lazy(self.model_name+"-list")

        return super(GenericCreate, self).dispatch(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        data = super(GenericCreate, self).get_context_data(**kwargs)
        data['NAME']=self.model.NAME
        data['LISTURL']=self.model_name+"-list"
        data['NAV_LINKS'] = get_navigation_links()
        return data


class GenericList(PermissionRequiredMixin,ListView):
    
    template_name = "generic_list.html"
   
    def dispatch(self, *args, **kwargs):
        self.model = self.kwargs.get('model','')
        self.model_name = self.model.__name__.lower()
        self.form_class = self.kwargs.get('form_class','')
        self.permission_required = 'stock.view_'+self.model_name
        self.success_url = reverse_lazy(self.model_name+"-list")

        return super(GenericList, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super(GenericList, self).get_context_data(**kwargs)
        data['NAME']=self.model.NAME
        data['AddURL']=self.model_name+"-add"
        data['UpdateURL']=self.model_name+"-update"
        data['DeleteURL']=self.model_name+"-delete"
        if hasattr(self.model, 'HAS_VIEW_URL') and self.model.HAS_VIEW_URL:
            data['ViewURL']=self.model_name+"-view"
        else:
            data['ViewURL']=False
        data['CanAdd']=self.request.user.has_perm('stock.add_'+self.model_name)
        data['CanEdit']=self.request.user.has_perm('stock.change_'+self.model_name)
        data['CanDelete']=self.request.user.has_perm('stock.delete_'+self.model_name)

        data['NAV_LINKS'] = get_navigation_links()
        return data


class GenericUpdate(PermissionRequiredMixin,UpdateView):
    
    template_name = "generic_form.html"
   
    def dispatch(self, *args, **kwargs):
        self.model = self.kwargs.get('model','')
        self.model_name = self.model.__name__.lower()
        self.form_class = self.kwargs.get('form_class','')
        self.permission_required = 'stock.change_'+self.model_name
        self.success_url = reverse_lazy(self.model_name+"-list")

        return super(GenericUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(GenericUpdate, self).get_context_data(**kwargs)
        data['NAME']=self.model.NAME
        data['LISTURL']=self.model_name+"-list"

        data['NAV_LINKS'] = get_navigation_links()
        return data
    

class GenericDelete(PermissionRequiredMixin,DeleteView):
    
    template_name = "generic_confirm_delete.html"
   
    def dispatch(self, *args, **kwargs):
        self.model = self.kwargs.get('model','')
        self.model_name = self.model.__name__.lower()
        self.permission_required = 'stock.delete_'+self.model_name
        self.success_url = reverse_lazy(self.model_name+"-list")

        return super(GenericDelete, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super(GenericDelete, self).get_context_data(**kwargs)
        data['NAME']=self.model.NAME
        data['LISTURL']=self.model_name+"-list"

        data['NAV_LINKS'] = get_navigation_links()
        return data
    

class GenericView(PermissionRequiredMixin,DetailView):
    
    template_name = "generic_view.html"
   
    def dispatch(self, *args, **kwargs):
        self.model = self.kwargs.get('model','')
        self.model_name = self.model.__name__.lower()
        self.form_class = self.kwargs.get('form_class','')
        self.permission_required = 'stock.view_'+self.model_name
        self.success_url = reverse_lazy(self.model_name+"-list")

        return super(GenericView, self).dispatch(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        data = super(GenericView, self).get_context_data(**kwargs)
        data['NAME']=self.model.NAME
        data['LISTURL']=self.model_name+"-list"

        data['OBJ']= self.form_class(data=model_to_dict(self.object))
        data['NAV_LINKS'] = get_navigation_links()
        return data