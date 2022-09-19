from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from emp_app.forms import LoginForm_
from emp_app.forms import EmployeeForm
from django.contrib import messages
from emp_app.models import Employee
from emp_app.forms import UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.

def home(request):
    return HttpResponse("hello")

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm_()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm_(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user= authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("emp-list")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"login.html",{"form":form})
        return render(request,"login.html",{"form":form})

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserRegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"your account has been created successfully")
            return redirect("sign-in") #sign-up is name from urls.py
        else:
            messages.error(request,"registration failed")
            return render(request,"signup.html",{"form":form})


def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            messages.error(request,"you must login")
            return redirect("sign-in")
    return wrapper

@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form= EmployeeForm()
        return render(request, "emp-add.html", {"form": form}) #custom templates
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"product has been added")
            return redirect("emp-add")
        else:
            messages.error(request,"product adding failed")
            return render(request, "emp-add.html", {"form": form}) #custom templates

@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs = Employee.objects.all()
        return render(request,"index.html",{"employees":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDetailsView(View):
    def get(self,request,*args,**kwargs):
        print(kwargs)
        qs = Employee.objects.get(eid=kwargs.get("emp_id"))
        return render(request,"emp-details.html",{"employee":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeEditView(View):
    def get(self,request,*args,**kwargs):
        eid=kwargs.get("emp_id")
        employee=Employee.objects.get(eid=eid)
        form=EmployeeForm(instance=employee)
        return render(request,"emp-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        eid = kwargs.get("emp_id")
        employee = Employee.objects.get(eid=eid)
        form= EmployeeForm(request.POST,instance=employee,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"employeee has updated")
            return render(request,"index.html",{"form":form})
        else:
            messages.error(request,"employee updation failed")
            return render(request,"index.html",{"form":form})


@signin_required
def remove_employee(request,*args,**kwargs):
    eid=kwargs.get("emp_id")
    employee=Employee.objects.get(eid=eid)
    employee.delete()
    messages.error(request,"employee hasbeeen removed")
    return redirect("emp-list")

@signin_required
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("sign-in")