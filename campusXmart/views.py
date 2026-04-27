from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .serializers import *
# from myorg.imagekit import imagekit

# # def upload_image(file):
# #     take_image = imagekit.upload_file(
# #         file=file,
# #         file_name=file.name
# #     )
# #     return take_image.response_metadata['url']

# def upload_profileImage(request):
#     if request.method == "POST":
#         file =request.Files.get('user_image_url')
#         print(file)
#     return redirect("profile")

def homepage(request):
    recent_products = Product.objects.order_by('-created_datetime')[:8]
    user_id =request.session.get('user_id')
    profile = None
    if user_id:
        profile = User.objects.get(user_id=user_id)
    context = {
         'recent_products' : recent_products,
         'profile' : profile,
    }
    return render(request, 'home.html', context)

# login part
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                 email_id=email)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("login")
        
        if user.password == password:
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name
            messages.success(request, "You have been successfully logged in.")
            return redirect("homepage") 
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, "login.html")
    
def logout_view(request):
        request.session.flush()
        return redirect('login')
 
def signup(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        email = request.POST.get('email_id')
        password = request.POST.get('password')

        if User.objects.filter(user_name=username).exists():
            messages.info(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email_id=email).exists():
            messages.info(request, "Email already exists.")
            return redirect("signup")

        user = User.objects.create(
            user_name=username,
            email_id=email,
            password=password,
        )

        messages.info(request, "Your account has been successfully created.")
        return redirect("login")
    
    return render(request, "signup.html")

def sellproduct(request):
    sell_product = None
    product_title = ''
    product_description = ''
    price = 0
    product_image = None
    category = None
    category_id=0
    categories = Category.objects.all() 
    user_id =request.session.get('user_id')
    profile = User.objects.get(user_id=user_id)
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        data = request.POST
        product_title = data.get('product_title')
        product_description = data.get('product_description')
        price = data.get('price')
        category_id = data.get('category')
        product_image = request.FILES.get('product_image_url')
        category = Category.objects.get(category_id=category_id)

        sell_product = Product.objects.create(
            product_title=product_title,
            product_description=product_description,
            price=price,
            category=category,
            user=profile,
            product_image_url=product_image,
        )
        messages.success(request, "Your item is now listed!")
        return redirect('sellproduct')

    context = {
        'categories':categories,
        'sell_product':sell_product,
        'profile': profile,
    }
    return render(request, 'sellproduct.html', context)

def delete_product(request, product_id):
    product= Product.objects.get(product_id=product_id)
    product.delete()
    return redirect("profile")

def edit_product(request, product_id):
    product= Product.objects.get(product_id=product_id)
    return render(request,'editproduct.html')

def negotation(request, product_id):
        user_id =request.session.get('user_id')
        listedproducts = Product.objects.get(product_id=product_id)
        profile = User.objects.get(user_id=user_id)
        context = {
            'listedproducts': listedproducts,
            'profile':profile,
        }
        return render(request, 'negotation.html', context)



def productlist(request):
    profile = None
    user_id =request.session.get('user_id')
    categories = Category.objects.all()
    product = Product.objects.all()
    if user_id:
        profile = User.objects.get(user_id=user_id)

    Context ={
            'categories' : categories,
            'product' : product,
            'profile':profile,
        }

    return render(request, 'productlisting.html',Context)


def productdetails(request , product_id):
        user_id =request.session.get('user_id')
        listedproducts = Product.objects.get(product_id=product_id)
        profile = None
        if user_id:
            profile = User.objects.get(user_id=user_id)
        context = {
            'listedproducts': listedproducts,
            'profile':profile,
        }
        return render(request, 'product details.html', context)

def profile(request):
    user_id =request.session.get('user_id')
    if not user_id:
        return redirect('login')
    listedproducts = Product.objects.filter(user_id=user_id)
    if user_id:
        profile = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        profile_image = request.FILES.get('user_image_url')

        if email:
            profile.email_id = email
        if contact:
            profile.contact_no = contact
        if password:
            profile.password = password
        if profile_image:
            profile.user_image_url = profile_image

        profile.save()
        return redirect('profile')
    
    context = {
        'listedproducts': listedproducts,
        'profile':profile
        }
    return render(request, 'profile.html', context)

def reportfraud(request):
    user_id =request.session.get('user_id')
    profile = None
    if user_id:
        profile = User.objects.get(user_id=user_id)


    context = {
    'profile':profile
    }   

    return render(request, 'reportingpage.html')

