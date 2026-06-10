from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .serializers import *

def search_product(request):
    if request.method == "GET":
        query_name = request.GET.get('q')
        sort_by = request.GET.get('sort', 'relevant')
        if query_name:
            results = Product.objects.filter(product_title__icontains=query_name)
            if sort_by == 'price_low':
                results = results.order_by('price')
            elif sort_by == 'price_high':
                results = results.order_by('-price')
            elif sort_by == 'newest':
                results = results.order_by('-created_datetime')
            # else relevant, no order
            context = {
                "products": results,
                'query': query_name,
                'total_results': results.count(),
                'sort_by': sort_by
            }
            return render(request, 'search_results.html', context)
        else:
            context = {
                "products": [],
                'query': '',
                'total_results': 0,
                'sort_by': sort_by
            }
            return render(request, 'search_results.html', context)

    return render(request, 'search_results.html')

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

        if not email.lower().endswith("@student.jlu.edu.in"):
            messages.info(request, "Only JLU student email is allowed.")
            return redirect("signup")

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
        return redirect('profile')

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('profile')

    # ensure only owner edits
    if product.user.user_id != user_id:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('profile')

    categories = Category.objects.all()
    profile = User.objects.get(user_id=user_id)

    if request.method == 'POST':
        post = request.POST
        product.product_title = post.get('product_title', product.product_title)
        product.product_description = post.get('product_description', product.product_description)
        price = post.get('price')
        if price:
            product.price = price
        category_id = post.get('category')
        if category_id:
            try:
                product.category = Category.objects.get(category_id=category_id)
            except Category.DoesNotExist:
                pass
        image = request.FILES.get('product_image_url')
        if image:
            product.product_image_url = image
        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('profile')

    return render(request, 'editproduct.html', {'product': product, 'categories': categories, 'profile': profile})

def negotation(request, product_id):
        user_id =request.session.get('user_id')
        if not user_id:
            return redirect('login')
        listedproducts = Product.objects.get(product_id=product_id)
        profile = User.objects.get(user_id=user_id)
        context = {
            'listedproducts': listedproducts,
            'profile':profile,
        }
        return render(request, 'negotation.html', context)



def productlist(request):
    profile = None
    user_id = request.session.get('user_id')
    categories = Category.objects.all()
    query = request.GET.get('q', '').strip()
    category_ids = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '')

    products = Product.objects.all()
    if query:
        products = products.filter(product_title__icontains=query)
    if category_ids:
        try:
            ids = [int(c) for c in category_ids]
            products = products.filter(category_id__in=ids)
        except Exception:
            pass

    try:
        if min_price:
            products = products.filter(price__gte=float(min_price))
        if max_price:
            products = products.filter(price__lte=float(max_price))
    except Exception:
        pass

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_datetime')

    if user_id:
        profile = User.objects.get(user_id=user_id)

    selected_cats = []
    for c in category_ids:
        try:
            selected_cats.append(int(c))
        except:
            pass

    context = {
        'categories': categories,
        'product': products,
        'profile': profile,
        'query': query,
        'selected_categories': selected_cats,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'sort_by': sort_by,
    }

    return render(request, 'productlisting.html', context)


def suggest_products(request):
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        matches = Product.objects.filter(product_title__icontains=q).values_list('product_title', flat=True).distinct()[:10]
        suggestions = list(matches)
    return JsonResponse({'suggestions': suggestions})


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
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        profile_image = request.FILES.get('user_image_url')

        if username:
            profile.user_name = username
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

