from django.urls import path, reverse_lazy
from django.conf import settings 
from django.conf.urls.static import static 
from . import views
from django.views.generic import TemplateView

app_name='createexp'
urlpatterns = [
    path('add/', views.post, name='add'),
    path('exps/', views.ListView, name='Exp_list'),
    path('exps/<int:id>', views.DetailView, name='Exp_detail'),
    path('exps/<int:id>/update', views.UpdateView, name='Exp_update'),
    path('exps/<int:id>/delete', views.DeleteView, name='Exp_delete'),
    path('exps/<int:id>/comment',views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',views.CommentDeleteView.as_view(), name='comment_delete'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #path('', views.CreateexpCreateView.as_view()),
    #path('createexp', views.CreateexpCreateView.as_view(), name='all'),]