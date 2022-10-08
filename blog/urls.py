from django.urls import path
from . import views


urlpatterns = [
    #path('fbv-index', views.indexView, name='fbv-index'),
    #path('cbv-index', TemplateView.as_view(template_name='index.html', extra_context={"name": "ALI"})),

    #path('cbv-index', views.IndexView.as_view(), name ='cbv-index'),
    path('go-to-maktabkhoone', views.RedirectToMaktab.as_view(), name='go-to-maktabkhoone'),
    path('post/', views.PostList.as_view(), name='post-view'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete')
]