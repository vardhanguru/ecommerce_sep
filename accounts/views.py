from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import User
from products.models import Products, Category

# Create your views here.

def register_user(request):

    if request.method == 'POST':
        print(request)
        print(request.body)
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print("hereee")

        print(username, email, password)
        if password != confirm_password:
            return render(request, 'register.html', {'error':'password is not matching'})
        elif not all([first_name, last_name, phone_number, address]):
            return render(request, 'register.html', {'error':'Please complete all profile and account fields.'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error':'user is existed'})
        else:
            print('heree inside the else block')
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
            )
            return redirect('login')



    return render(request, 'register.html')

def login_view(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        if '@' in username:
            
            # fetch username based on the email
            print(username)
            user = User.objects.filter(email=username)
            print(user)

            if user is not None:
                user = user[0]
                print('here ')
                user = authenticate(request, username=user.username, password = password)


            
        else:
            user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            return redirect('storefront_home')
        else:
            return render(request, 'login.html', {'errors':'not existed/incorrect password'})



    return render(request, 'login.html')

def home_view(request):
    featured_products = Products.objects.filter(is_available=True).order_by('-created_at')[:12]

    categories = Category.objects.all()
    
    return render(request, 'home.html', {'featured_products': featured_products, 'categories': categories})

def logout_view(request):
    logout(request)

    return redirect('login')

def set_session(request):
    request.session['name'] = 'vardhan'
    request.session['age'] = 28
    request.session['city'] = 'Hyderabad'
    request.session.set_

    return JsonResponse({'message':'session data created.'})


def get_session(request):
    name = request.session.get('name')
    age = request.session.get('age')
    city = request.session.get('city')

    return JsonResponse({'name':name, 'age':age,'city':city})

def delete_session(request):

    # del request.session['age']
    # request.session.clear()
    # complete flush
    request.session.flush()  # very stronger than clear method
    return JsonResponse({"message": "deleted"})

def profile_view(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.phone_number = request.POST.get('phone_number', '').strip()
        user.address = request.POST.get('address', '').strip()
        user.save()
        return redirect('profile')
    return render(request, 'profile.html', {'user': user})