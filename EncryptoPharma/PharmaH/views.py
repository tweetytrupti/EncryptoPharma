from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from .models import Manager, Employee,Component,Administrator,Details,Medicine
from .forms import ComponentForm
from django.contrib import messages
from . import paillier
from django.http import QueryDict
import pickle
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .password_generator import  generate_password

def serialize_private_key(private_key):
    return pickle.dumps(private_key)

def deserialize_private_key(serialized_key):
    return pickle.loads(serialized_key)

def home(request):
    return render(request, 'home/home.html')

@login_required
def ComponentEntry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'medicine_id' in data and 'component_name' in data:
            medicine_id = data['medicine_id']
            component_name = data['component_name']
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                manager = medicine.manager_id
                new_manager=Manager.objects.get(id=manager)
                Details.objects.create(medicine_id=medicine_id, name=component_name, manager=new_manager,cost=0,quantity=0)
                return JsonResponse({'success': True})
            except Medicine.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Medicine not found'})
        return JsonResponse({'success': False, 'error': 'Invalid data'})

    medicines = Medicine.objects.all()  # Fetch all the medicines from the database

    if 'medicine_id' in request.GET:
        medicine_id = request.GET['medicine_id']
        components = Details.objects.filter(medicine_id=medicine_id).values_list('name', flat=True)
        return JsonResponse(list(components), safe=False)

    return render(request, 'ComponentEntry/ComponentEntry.html', {'medicines': medicines})

@login_required
def get_medicines(request):
    medicines = Medicine.objects.all()
    medicines_data = []
    for medicine in medicines:
        components = medicine.components.values_list('name', flat=True)
        medicines_data.append({
            'name': medicine.name,
            'components': list(components),
        })
    return JsonResponse(medicines_data, safe=False)

@login_required
def managersignup(request):
    if request.method == 'POST':
        username = request.POST.get('signupusername')
        first_name = request.POST.get('signupfirstname')
        last_name = request.POST.get('signuplastname')
        email = request.POST.get('signupemail')
        medicine= request.POST.get('signupmedicine')
        employee_id = request.POST.get('signupemployeeid')
        password=  generate_password()

        
        #print("this is input from form: ",username, first_name, last_name, email, employee_id, password)

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            print('Username already exists.')
            return redirect('managersignup')
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists.')
        #     print('Email already exists.')
        #     return redirect('managersignup')
        #print('passed checking successfully.')
        
        priv,pub_key = paillier.generate_keypair(int(256))
        # Serialize the private key
        # priv_key = serialize_private_key(priv)
        #print("Private key ->", priv_key)
        #print("Public key ->", pub_key)
        
        a = priv.get_list()
        priv1 = a[0]
        priv2 = a[1]
        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        #print('User created successfully.')
        # Create the manager profile
        Manager.objects.create(username=username,user=user, employee_id=employee_id,priv_key=priv1,priv_key_2=priv2,pub_key=pub_key )
        messages.success(request, 'Manager created successfully.')
        print('Manager created successfully.')
        
        manager = Manager.objects.get(username=username)
        Medicine.objects.create(
            manager_id=manager.id,  # this uses the newly created manager instance
            medicine_name=medicine
        )
        print('Medicine created successfully.')
        #from here we send mail
        # Define the subject and message for the email to be sent to the new employee
        subject = "Important Notfication"
        message = 'Following is your username and password to login in EncryptoPharma ' \
                  'Username: ' + username + ' Password: '+ password

        # Get the email settings from the Django settings
        from_email = settings.EMAIL_HOST_USER
        print("This is sender's email :", from_email)

        # Define the list of recipients for the email
        to_list = [email,from_email]
        print(to_list)

        # Send the email using Django's send_mail function
        send_mail(subject=subject,from_email=from_email,message=message,recipient_list=to_list,fail_silently=True)
        print("Mail sent successfully!!!")
    
    return render(request, 'Signup/ManagerSignup.html')

@login_required
def employeesignup(request):
    if request.method == 'POST':
        username = request.POST.get('signupusername')
        first_name = request.POST.get('signupfirstname')
        last_name = request.POST.get('signuplastname')
        email = request.POST.get('signupemail')
        employee_id = request.POST.get('signupemployeeid')
        password = generate_password()
        manager = request.POST.get('signupmanagername')
        
        #print("this is input from form: ",username, first_name, last_name, email, employee_id, password, manager)

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            print('Username already exists.')
            return redirect('employeesignup')
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists.')
        #     print('Email already exists.')
        #     return redirect('employeesignup')
        #print('passed checking successfully.')
        
        try:
            # Look up the manager by name
            manager = Manager.objects.get(username=manager)
            print("manager is here:",manager)
        except Manager.DoesNotExist:
            messages.error(request, 'Manager not found.')
            print('Manager not found.')
            return redirect('employeesignup')
        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        #print('User created successfully.')
        # Create the manager profile
        Employee.objects.create(username=username, user=user, employee_id=employee_id,email=email, manager=manager)

        messages.success(request, 'Employee created successfully.')
        print('employee created successfully.')
        
        #from here we send mail
        # Define the subject and message for the email to be sent to the new employee
        subject = "Important Notfication"
        message = 'Following is your username and password to login in EncryptoPharma ' \
                  'Username: ' + username + ' Password: '+ password

        # Get the email settings from the Django settings
        from_email = settings.EMAIL_HOST_USER
        print("This is sender's email :", from_email)

        # Define the list of recipients for the email
        to_list = [email,from_email]
        print(to_list)

        # Send the email using Django's send_mail function
        send_mail(subject=subject,from_email=from_email,message=message,recipient_list=to_list,fail_silently=True)
        print("Mail sent successfully!!!")
        
    return render(request, 'Signup/EmployeeSignup.html')

@login_required
def administrator(request):
    return render(request, 'Admin/admin.html')

@login_required
def Managerdashboard(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    print("manager:",manager.id)
    managerid=manager.id
    # Retrieve all employees under this manager
    employees = Employee.objects.filter(manager=manager)
    medicines=Medicine.objects.filter(manager_id=managerid)
    # print("medicines:",medicines)
    # print("employee: ", employees)
    components = Component.objects.filter(employee__in=employees)
    # print("components: ",components)
    for medicine in medicines:
        medicine= medicine.medicine_name
        print("Medicine name:",medicine)
    # Decrypt cost and quantity for each component
    decrypted_components = []
    priv_key = int(manager.priv_key)  # Ensure the private key is securely retrieved
    priv_key_2 = int(manager.priv_key_2)
    pub_key = int(manager.pub_key)
    
    for component in components:
        if component.cost ==0 and component.quantity == 0:
            decrypted_cost = component.cost
            decrypted_quantity =component.quantity
        else:
            decrypted_cost = paillier.decrypt(priv_key, priv_key_2, pub_key, int(component.cost))
            decrypted_quantity = paillier.decrypt(priv_key, priv_key_2, pub_key, int(component.quantity))
                
                # Get the employee name for this component
        employee_name = Employee.objects.get(id=component.employee_id).username
                
        decrypted_components.append({
            'name': getattr(component, 'name'),
            'employee_name': employee_name,
            'decrypted_cost': decrypted_cost,
            'decrypted_quantity': decrypted_quantity,
            'timestamp': component.timestamp,
            })
    print("Medicine name:",medicine)
    employe = []
    for employee in employees:
        decrypted_employee = {
            'Id':employee.employee_id,  # Changed from employee.employee_id to employee.id
            'name': employee.username,  # Assuming 'username' is the field for employee name
            'email': employee.email,  # Assuming 'email' is the field for employee email
            'Medicine': medicine,
            # Add other decrypted fields as needed
        }
        employe.append(decrypted_employee)
        # print("Decrypted Employee: ", decrypted_employee)
    
    # print("Decrypted Employees List: ", employe)
    
    details = Details.objects.filter(manager=manager)
    det = []
    for Detail in details:
        if Detail.cost == '0' and Detail.quantity == '0':
            decrypted_cost = Detail.cost
            decrypted_quantity = Detail.quantity
        else:
            decrypted_cost = paillier.decrypt(priv_key, priv_key_2, pub_key, int(Detail.cost))
            decrypted_quantity = paillier.decrypt(priv_key, priv_key_2, pub_key, int(Detail.quantity))
            
        decrypted_details = {
            'Id':Detail.id,  # Changed from employee.employee_id to employee.id
            'name': Detail.name,  # Assuming 'username' is the field for employee name
            'quantity': decrypted_quantity ,  # Assuming 'email' is the field for employee email
            'cost': decrypted_cost,
            # Add other decrypted fields as needed
        }
        det.append(decrypted_details)
        # print("Decrypted Details: ", decrypted_details)
    
    
    # Pass the manager and employees to the template
    context = {
        'manager': manager,
        'employees': employe,
        'components': decrypted_components,
        'Details':det,
    }
    
    # print("Context: ", context)

    return render(request, 'Manager/ManagerDashboard.html', context)


def Employeedashboard(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    manager_id = employee.manager_id

    # Filter components based on manager_id
    components = Details.objects.filter(manager_id=manager_id)
    context = {
        'employee': employee,
        'components': components,
    }
    return render(request, 'Employee/EmployeeDashboard.html', context)

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        print("this is username:",loginusername,"this is password:",loginpassword)
        # Authenticate user with provided username and password
        user = authenticate(username=loginusername, password=loginpassword)
        print("this is user:",user)
        if user is not None:
            print("i am inside this....")
            # Login successful, redirect based on user type
            if Manager.objects.filter(user=user).exists():
                login(request, user)
                return redirect('Managerdashboard')
            elif Employee.objects.filter(user=user).exists():
                login(request, user)
                return redirect('Employeedashboard')
            elif Administrator.objects.filter(user=user).exists():
                login(request, user)
                return redirect('Administrator')
            else:
                # Redirect to home page if user is not a Manager or Employee
                print("i am not getting any position")
                return redirect('home')
        else:
            # Redirect to home page if authentication fails
            return redirect('home')

    return render(request, 'Login/login.html')


def add_component(request):
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        
        if form.is_valid():
            component_name = form.cleaned_data['name']
            
            employee = request.user.employee
            print("employee:",employee)
            manager = employee.manager
            print("manager:",manager)
            public_key = manager.pub_key  # Assuming the public key is stored in manager's profile
            
            cost = form.cleaned_data['cost']
            quantity = form.cleaned_data['quantity']
            
            encrypted_cost = paillier.encrypt(int(public_key), int(cost))
            encrypted_quantity =paillier.encrypt(int(public_key), int(quantity))

            component = form.save(commit=False)
            component.cost = encrypted_cost
            component.quantity = encrypted_quantity
            component.employee = employee
            component.save()
            
            if Details.objects.filter(name=component_name).exists():
                detail = Details.objects.get(name=component_name)
                if int(detail.cost) != 0 or int(detail.quantity) != 0:
                    encrypted_detail_cost = int(detail.cost)
                    encrypted_detail_quantity = int(detail.quantity)
                    detail.quantity = paillier.e_add(int(public_key), encrypted_detail_quantity, encrypted_quantity)
                    detail.cost = paillier.e_add(int(public_key), encrypted_detail_cost, encrypted_cost)
                else:
                    detail.quantity = encrypted_quantity
                    detail.cost = encrypted_cost
                detail.save()
            else:
                print("Component is not present")
                return redirect('Employeedashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = ComponentForm()
    
    user = request.user
    employee = Employee.objects.get(user=user)
    manager_id = employee.manager_id
    components = Details.objects.filter(manager_id=manager_id)  
    context = {
        'form': form,
        'employee': employee,
        'components': components,
    }
    
    return render(request, 'Employee/EmployeeDashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')