from django.shortcuts import get_object_or_404, redirect, render
from .models import  Status, NewOrder, Payment, Profile
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
import xlwt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
import string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
      
@login_required
def search_orders(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        # Filter orders for the current user
        user_orders = NewOrder.objects.filter(owner=request.user)
        
        # Apply search filters on user's orders
        orders = user_orders.filter(
            Q(name__icontains=search_str) |
            Q(contact__istartswith=search_str) |
            Q(location__icontains=search_str) |
            Q(date_ordered__istartswith=search_str) |
            Q(status__icontains=search_str) |
            Q(amount__icontains=search_str) |
            Q(id__istartswith=search_str)
        )
        
        data = orders.values()
        return JsonResponse(list(data), safe=False)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)



def home(request):
    


    return render(request, "index.html")

def sos(request,exception):


    return render(request, "404.html")    

def account(request):

    return render(request, "account.html")

def wallet(request):

    return render(request, "wall.html")





def user_login(request):
    if request.method == 'POST':
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            messages.error(request, 'Email is required')
            context['has_error'] = True

        if not password:
            messages.error(request, 'Password is required')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'login.html', status=400, context=context)

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is None:
            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'No account found with this email address')
            return render(request, 'login.html', status=401, context=context)

        login(request, user)
        return redirect('home')

    return render(request, "login.html")


def notifications(request):

    return render(request, "notifications.html")

def user_logout(request):
    logout(request)
    return redirect('user_login') 


def orders(request):
    if request.user.is_authenticated:

        order = NewOrder.objects.filter(owner=request.user).order_by('-date_ordered')    
        statusy = Status.objects.all()
        payment  = Payment.objects.all()

        

        #Paginators ALL section
        paginator = Paginator(order, 10)
        page_number = request.GET.get('page')
        try:
            page_object = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_object = paginator.page(1)
        #page_object = Paginator.get_page(paginator,page_number)
        #mandevu = NewOrder.objects.filter(owner=request.user)
        context = {
            'order' : order,
            'statusy': statusy,
            'page_object': page_object,
            'payment': payment
        }
    else:
        messages.error(request, "You need to be logged in to view orders.")
        return redirect('home')  # Redirect to your login page    

    
    

    return render(request, "orders.html",context)

def reset(request):

    return render(request, "reset-password.html")

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return redirect('signup')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        otp = generate_otp()
        request.session['otp'] = otp
        request.session['user_data'] = {
            'username': username,
            'email': email,
            'password': password
        }

        # Send OTP via email
        try:
            send_mail(
                'Your OTP for Registration',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            messages.error(request, 'Error sending OTP email. Please try again.')
            return redirect('signup')

        return redirect('verify_otp')

    return render(request, 'signup.html')


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        user_data = request.session.get('user_data')

        if user_otp == stored_otp:
            # Check if the user already exists (due to a previous failed attempt)
            if User.objects.filter(username=user_data['username']).exists():
                messages.error(request, 'This username has already been registered.')
                return redirect('signup')

            if User.objects.filter(email=user_data['email']).exists():
                messages.error(request, 'This email has already been registered.')
                return redirect('signup')

            # Try creating the user
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                user.is_active = True
                user.save()
            except IntegrityError:
                messages.error(request, 'An error occurred during registration. Please try again.')
                return redirect('signup')

            # Clear session data after successful registration
            del request.session['otp']
            del request.session['user_data']

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')

def new_edit(request,id):

    order = get_object_or_404(NewOrder, pk=id, owner=request.user)
    
    statusy = Status.objects.all()
    payment = Payment.objects.all()

    context = {
        'order': order,
        'Values': order,
        'statusy': statusy,
        'payment': payment   
    }
    if request.method == "GET":

       return render(request, "new_edit.html", context)
    

    if request.method == "POST":
        name = request.POST['name']
        if not name:
            messages.error(request, 'name is required')
            return render(request, "new_edit.html", context)
        

        contact = request.POST['contact']
        if not contact:
            messages.error(request, 'contact is required')
            return render(request, "new_edit.html", context)
        

        location = request.POST['location']
        if not location:
            messages.error(request, 'location is required')
            return render(request, "new_edit.html", context)
        
        
        quantity = request.POST['quantity']
        if not quantity:
            messages.error(request, 'quantity is required')
            return render(request, "new_edit.html", context)
        
        date_ordered = request.POST['date_ordered']
        if not date_ordered:
            messages.error(request, 'date_ordered is required')
            return render(request, "new_edit.html", context)
        
        date_due = request.POST['date_due']
        if not date_due:
            messages.error(request, 'date_due is required')
            return render(request, "new_edit.html", context)
        
        status = request.POST['status']
        if not status:
            messages.error(request, 'status is required')
            return render(request, "new_edit.html", context)
        
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, "new_edit.html", context)
        
        pay_form = request.POST['pay_form']
        if not pay_form:
            messages.error(request, 'pay_form is required')
            return render(request, "new_edit.html", context)
        
        order.name=name
        order.contact=contact
        order.location=location
        order.quantity=quantity
        order.date_ordered=date_ordered
        order.date_due=date_due
        order.status=status
        order.amount=amount
        order.pay_form=pay_form


        order.save()
        messages.success(request, "order successfully edited")
        return redirect('orders')
    return render(request, "new_edit.html", context)
      

 

@login_required
def form(request):

    statusy = Status.objects.all()
    payment  = Payment.objects.all()

    context = {
        'statusy': statusy,
        'values': request.POST,
        'payment': payment
    }

    if request.method == 'POST':

        name = request.POST['name']
        if not name:
            messages.error(request, 'name is required')
            return render(request, "form.html", context)
        

        contact = request.POST['contact']
        if not contact:
            messages.error(request, 'contact is required')
            return render(request, "form.html", context)
        

        location = request.POST['location']
        if not location:
            messages.error(request, 'location is required')
            return render(request, "form.html", context)
        
        
        quantity = request.POST['quantity']
        if not quantity:
            messages.error(request, 'quantity is required')
            return render(request, "form.html", context)
        
        date_ordered_str = request.POST['date_ordered']
        if not date_ordered_str:
            messages.error(request, 'date_ordered is required')
            return render(request, "form.html", context)
        

         # Parse date_ordered string into datetime object
        date_ordered = datetime.strptime(date_ordered_str, '%Y-%m-%d')
        
        date_due_str = request.POST['date_due']
        if not date_due_str:
            messages.error(request, 'date_due is required')
            return render(request, "form.html", context)
        

         # Parse date_due string into datetime object
        date_due = datetime.strptime(date_due_str, '%Y-%m-%d')
        


         # Ensure date_due is one month later than date_ordered
        if date_due <= date_ordered + timedelta(days=30):
            messages.info(request, 'Date due should be at least one month later than Date ordered')  
            return render(request, "form.html", context)
        


        status = request.POST['status']
        if not status:
            messages.error(request, 'status is required')
            return render(request, "form.html", context)
        
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, "form.html", context)
        
        pay_form = request.POST['pay_form']
        if not pay_form:
            messages.error(request, 'pay_form is required')
            return render(request, "form.html", context)
        
        NewOrder.objects.create(name=name,
                                contact=contact, 
                                location=location,
                                quantity=quantity,
                                date_ordered=date_ordered,
                                date_due=date_due,
                                status=status,
                                pay_form=pay_form,
                                amount=amount,
                                owner=request.user  # This line associates the order with the current user

                                )
        messages.success(request, "order successfully added")
        return redirect('orders')
    return render(request, "form.html", context)    



def export_excel(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] ='attachment; filename=Orders' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook( encoding='utf-8')
    ws = wb.add_sheet('Orders')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True


    columns = ['Name', 'Contact', 'Location','Quantity', 'Date_ordered','Date_due','Status','Payment_Form', 'Amount']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = NewOrder.objects.filter().values_list('name','contact','location', 'quantity', 'date_ordered', 'date_due','status','pay_form','amount')  

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]), font_style) 

    wb.save(response) 

    return response        