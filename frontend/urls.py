from django.urls import path, re_path
from .views import Home, Assets
from django.views.generic import TemplateView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # re_path(r'^(?P<filename>[\w\.]+)$', Assets.as_view(), name='assets'),
    # re_path(r'^(?P<filename>[\w\.]+)$', Assets.as_view(content_type='text/javascript'), name='assets'),
    re_path(r'^(?P<filename>[\w\.]+)$', TemplateView.as_view(template_name='bundle.js', content_type='text/javascript'), name='assets'),
    # re_path(r'^(?P<filename>[\w\.]+)$', TemplateView.as_view(content_type='text/javascript'), name='assets'),
    # re_path(r'^.*', TemplateView.as_view(
    #     template_name='index.html',
    #     content_type='text/html'))
]
