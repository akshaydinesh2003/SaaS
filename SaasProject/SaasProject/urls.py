#from django.contrib import admin
#from django.urls import path, include

#urlpatterns = [
#   path('admin/', admin.site.urls),
#    path('register/', include('registration.urls')),  # Correct the app name here
#]




from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userlogin.urls')),  # For login and signup pages
    path('tasks/', include('taskmanager.urls')),  # Add this line to include taskmanager URLs
]
