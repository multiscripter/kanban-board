"""kbboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from kbboard.controllers import KanbanBoard
from kbboard.controllers import SwaggerSchemaView

urlpatterns = [
    path('openapi/', SwaggerSchemaView.as_view()),
    path('tasks/<str:id>/', KanbanBoard.as_view()),
    path('tasks/', KanbanBoard.as_view()),
    path('admin/', admin.site.urls),
    # Инструкция на случай если favicon.ico не прописан в тэге head страницы
    # и не настроена отдача favicon.ico в Nginx.
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
