from django.urls import path
from emp_app import views
urlpatterns=[
    path('home/', views.home, name='home'),
    path("accounts/signup", views.SignUpView.as_view(), name="sign-up"),
    path("accounts/signin", views.LoginView.as_view(), name="sign-in"),
    path('profile/add', views.EmployeeCreateView.as_view(), name="emp-add"),
    path('all/',views.EmployeeListView.as_view(),name="emp-list"),
    path('all/', views.EmployeeListView.as_view(), name="emp-list"),
    path('details/<str:emp_id>',views.EmployeeDetailsView.as_view(),name="emp-detail"),
    path("change/<str:emp_id>",views.EmployeeEditView.as_view(),name="emp-edit"),
    path("remove/<str:emp_id>",views.remove_employee,name="emp-remove"),
    path("accounts/signout",views.sign_out,name="sign-out"),
    ]