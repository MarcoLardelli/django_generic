from django.urls import path
from . import views

from demo.forms import GENERIC_CLASSES_AND_FORMS

urlpatterns = [path('', views.index, name='index')]

for cl in GENERIC_CLASSES_AND_FORMS:
    class_name_lc = cl[0].__name__.lower()
    urlpatterns.append(
        path(class_name_lc+'/add', views.GenericCreate.as_view(),  {
            'model': cl[0],
            'form_class': cl[1],
        }, 
        name=class_name_lc+'-add')
    )
    urlpatterns.append(
        path(class_name_lc+'/', views.GenericList.as_view(),  {
            'model': cl[0]
        }, 
        name=class_name_lc+'-list')
    )
    urlpatterns.append(
        path(class_name_lc+'/<int:pk>', views.GenericUpdate.as_view(),  {
            'model': cl[0],
            'form_class': cl[1],
        }, 
        name=class_name_lc+'-update')
    )
    urlpatterns.append(
        path(class_name_lc+'/<int:pk>/delete', views.GenericDelete.as_view(),  {
            'model': cl[0]
        }, 
        name=class_name_lc+'-delete')
    )
    if  (not (hasattr(cl[0], 'HAS_CUSTOM_VIEW_URL') and cl[0].HAS_CUSTOM_VIEW_URL)) and (hasattr(cl[0], 'HAS_VIEW_URL') and cl[0].HAS_VIEW_URL):
        urlpatterns.append(
            path(class_name_lc+'/<int:pk>/view', views.GenericView.as_view(),  {
                'model': cl[0],
                'form_class': cl[1],
            }, 
            name=class_name_lc+'-view')
    )