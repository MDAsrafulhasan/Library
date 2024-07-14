
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage , name = 'home'),
    path('category/<slug:category_slug>/', views.homepage, name='category_wise_post'),
    path('account/',include('account.urls')),
    path('book/',include('book.urls')),
    path('transaction/',include('transaction.urls')),
    path('category/',include('category.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)