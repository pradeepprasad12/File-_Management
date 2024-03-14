from django.urls import path
from .views import upload_file, file_list, download_file,signup_view, login_view, logout_view,home_view,update_file_entry,delete_file_entry



urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('files/update/<int:file_id>/', update_file_entry, name='update_file_entry'),
    path('files/delete/<int:file_id>/', delete_file_entry, name='delete_file_entry'),

    

]
