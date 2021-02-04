from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('testing_user.urls')),
    path('api/runner/', include('testing_runner.urls')),
]
