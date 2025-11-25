from django.shortcuts import render
from django.http import HttpResponse
import pymongo
from .models import *
from django.conf import settings
from bson.objectid import ObjectId
import os
from datetime import datetime

# Create your views here.
my_client = pymongo.MongoClient(settings.DB_NAME)
dbname = my_client['Smart_City']
collection_name = dbname["User_Registration"]
service_collection=dbname['Service_Registration']
service_provide_collection=dbname['Service_Provider']
shop_details=dbname['Shop_Details']


def get_unique_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S%f")
        new_filename = f"{base}_{unique_suffix}{ext}"
    return new_filename

#Home page
def home(request):
   return render(request, 'index.html') 

#About page
def about(request):
    return render(request, 'about.html')

#User registration page
def register(request):
    return render(request, 'register.html')

#Admin and User login page
def login(request):
    return render(request, 'login.html')

#Register User
def save_user(request):
    error=False
    message=""
    if request.method == "POST":
        full_name=request.POST['full_name']
        emailid=request.POST['emailid']
        phoneno=request.POST['phoneno']
        address=request.POST['address']
        password=request.POST['password']
        birthdate=request.POST['birthdate']
        myquery = {'phoneno':phoneno}

        mydoc=collection_name.find(myquery)

        if collection_name.count_documents({'phoneno':phoneno}):
            message="Data already exists"
            d={'message':message}
            return render(request, 'register.html', d)
        else:
            staff_1 = {
                "name": full_name,
                "emailid" : emailid,
                "phoneno" : phoneno,
                "birthdate" : birthdate,
                "address": address,
                "password":password
            }
            collection_name.insert_one(staff_1)
            error=True
            message = "Data saved successfully"
            d={'message':message}
    return render(request, 'register.html',d)

#Admin and User login
def login_user(request):
    error=False
    if request.method == "POST":
        staffid=request.POST['emailid']
        password=request.POST['password']
        if staffid=="admin@gmail.com" and password=="admin":
            count_services=service_collection.count_documents({})
            count_service_provider=service_provide_collection.count_documents({})
            count_users=collection_name.count_documents({})
            users_list=collection_name.find().limit(5)
            service_provider=service_provide_collection.find().limit(5)
            services=service_collection.find().limit(5)
            context={'services':services,'service_provider':service_provider,'users':users_list,'user_count':count_users,'service_count':count_services,'provider_count':count_service_provider}
            return render(request,'admin_page.html',context)
        else:
            myquery={'emailid':staffid,'password':password}
            if collection_name.count_documents(myquery):
                services=service_collection.find()
                context={'services':services}
                return render(request, 'userpage.html',context)
            else:
                error=True
                message="Invalid credentials"
                d={'message':message,'error':error}
                return render(request,'login.html',d)

#Add and View services
def services(request):
    services_data=[]
    services=service_collection.find()
    for sr in services:
        sr['service_id']=str(sr['_id'])
        services_data.append(sr)
    d={'services':services_data}
    return render(request,'service.html',d)

#Add services
def add_services(request):
    error=False
    services_data=[]
    services=service_collection.find()
    for sr in services:
        sr['service_id']=str(sr['_id'])
        services_data.append(sr)
    if request.method=='POST':
        service_name=request.POST['service_name']  
        service_1 = {
                "service_name": service_name
            }
        service_collection.insert_one(service_1)
        error=True
        message = "Data saved successfully"
        d={'services':services_data,'message':message, 'error':error}
        return render(request, 'service.html',d)
    else:
        message = "Data not saved"
        d={'services':services,'message':message, 'error':error}
        return render(request, 'service.html',d)
    
#Service provider registration page
def service_provider(request):
    return render(request, 'serviceprovider.html')

#Save service provider
def save_service_provider(request):
    error=False
    if request.method == "POST":
        full_name=request.POST['full_name']
        emailid=request.POST['emailid']
        phoneno=request.POST['phoneno']
        address=request.POST['address']
        password=request.POST['password']
        birthdate=request.POST['birthdate']
        myquery = {'phoneno':phoneno}

        mydoc=service_provide_collection.find(myquery)

        if service_provide_collection.count_documents({'phoneno':phoneno}):
            error=True
            message="Data already exists"
            d={'message':message,'error':error}
            return render(request, 'serviceprovider.html', d)
        else:
            staff_1 = {
                "name": full_name,
                "emailid" : emailid,
                "phoneno" : phoneno,
                "birthdate" : birthdate,
                "address": address,
                "password":password
            }
            service_provide_collection.insert_one(staff_1)
            error=True
            message = "Data saved successfully"
            d={'message':message,'error':error}
            return render(request, 'serviceprovider.html',d)
        
#Login page for service provider
def login_service(request):
    return render(request, 'login_service.html')

#Check service provider login details
def login_service_provider(request):
    error=False
    if request.method == "POST":
        staffid=request.POST['emailid']
        password=request.POST['password']
        myquery={'emailid':staffid,'password':password}
        request.session['service_emailid']=staffid
        
        if service_provide_collection.count_documents(myquery):
            services=service_collection.find()
            context={'services':services}
            return render(request, 'add_shops.html',context)
        else:
            error=True
            message="Invalid credentials"
            d={'message':message,'error':error}
            return render(request,'login_service.html',d)
        
#Add shop
def add_shop(request):
    services=service_collection.find()
    d={'services':services}
    return render(request, 'add_shops.html',d)


#Save Shop
def save_shop(request):
    services = service_collection.find()
    error = False
    message = ""

    if request.method == "POST":
        emailid = request.session.get('service_emailid')
        shop_category = request.POST['shop-category']
        city_name = request.POST['city-name']
        area = request.POST['Area']
        address = request.POST['Address']
        pservices=request.POST['services']
        shop_name = request.POST['shop-name']
        owner_name = request.POST['owner-name']
        contact_number = request.POST['contact-number']
        openclose = request.POST['openclose']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        shop_photo = request.FILES.get('shop-photo')
        other_photos = request.FILES.getlist('other-photos')
        owner_photo = request.FILES.get('owner-photo')

        # Define subfolders for storing images
        shop_photo_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_photo')
        owner_photo_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_owner')
        other_photos_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_others')

        # Ensure that the subfolders exist
        os.makedirs(shop_photo_subfolder, exist_ok=True)
        os.makedirs(owner_photo_subfolder, exist_ok=True)
        os.makedirs(other_photos_subfolder, exist_ok=True)

        # Generate custom file names if photos are provided
        custom_shop_photo = None
        custom_owner_photo = None
        custom_other_photos = []

        if shop_photo:
            filename = f"{emailid}_shop{os.path.splitext(shop_photo.name)[1]}"
            unique_filename = get_unique_filename(shop_photo_subfolder, filename)
            custom_shop_photo = unique_filename
            shop_photo_path = os.path.join(shop_photo_subfolder, custom_shop_photo)
            with open(shop_photo_path, 'wb+') as destination:
                for chunk in shop_photo.chunks():
                    destination.write(chunk)


        if other_photos:
            for idx, image in enumerate(other_photos, start=1):
                filename = f"{emailid}_other_{idx}{os.path.splitext(image.name)[1]}"
                unique_filename = get_unique_filename(other_photos_subfolder, filename)
                custom_other_photos.append(unique_filename)
                other_photo_path = os.path.join(other_photos_subfolder, unique_filename)
                with open(other_photo_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)


        if owner_photo:
            filename = f"{emailid}_owner{os.path.splitext(owner_photo.name)[1]}"
            unique_filename = get_unique_filename(owner_photo_subfolder, filename)
            custom_owner_photo = unique_filename
            owner_photo_path = os.path.join(owner_photo_subfolder, unique_filename)
            with open(owner_photo_path, 'wb+') as destination:
                for chunk in owner_photo.chunks():
                    destination.write(chunk)

        # Check if the shop already exists by using find_one
        existing_shop = shop_details.find_one({'emailid': emailid, 'latitude': latitude, 'longitude': longitude})

        if existing_shop:
            error = True
            message = "Shop with these details already exists"
        else:
            # Create the shop entry
            shop = {
                "shop_category": shop_category,
                "city_name": city_name,
                "shop_name": shop_name,
                "owner_name": owner_name,
                "contact_number": contact_number,
                "services": pservices,
                "shop_photo": custom_shop_photo,
                "other_photos": custom_other_photos,
                "owner_photo": custom_owner_photo,
                "openclose": openclose,
                "latitude": latitude,
                "longitude": longitude,
                "area": area,
                "emailid": emailid,
                "address":address
            }

            # Insert the new shop record into the database
            shop_details.insert_one(shop)
            message = "Shop saved successfully"
            error=True

    # Render the template with the necessary context
    context = {'services': services, 'message': message, 'error': error}
    return render(request, 'add_shops.html', context)

#View shops
def view_shops(request):
    shops_data=[]
    shops = shop_details.find() 
    for sp in shops:
        sp['shop_id']=str(sp['_id'])
        shops_data.append(sp)
    d={'shops':shops_data, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request,"view_shops.html",d)

#View service provider shops
def view_shops_provider(request):
    shops_data=[]
    emailid = request.session.get('service_emailid')  # Assuming you're getting the emailid from the session
    shops = shop_details.find({'emailid': emailid})
    for sp in shops:
        sp['shop_id']=str(sp['_id'])
        shops_data.append(sp)
    context={'shops':shops_data}
    return render(request,'view_shops_provider.html',context)


# Fetch default recommendations (before user types anything)
def get_default_recommendations(request):
    recommendations = service_collection.objects.all()[:5]  # Fetch top 10 recommendations
    data = list(recommendations.values('name'))
    return JsonResponse(data, safe=False)

# Fetch matching recommendations based on user input
def get_filtered_recommendations(request):
    query = request.GET.get('query', '')
    recommendations = service_collection.objects.filter(name__icontains=query)
    data = list(recommendations.values('name'))
    return JsonResponse(data, safe=False)

# Fetch service providers for user on login
def fetch_providers_list(request):
    shops_data=[]
    if request.method == "POST":
        services = request.POST['service']
        area = request.POST['area']
        city = request.POST['city']

        print("Service:", services)
        print("Area:", area)
        print("City:", city)

        shops_cursor = shop_details.find({
            'shop_category': services,
            'area': area,
            'city_name': city
        })
        for sp in shops_cursor:
            sp['shop_id']=str(sp['_id'])
            shops_data.append(sp)
            print(sp['_id'])
        
        flag = True
        context = {'flag': flag,'shops':shops_data,'MEDIA_URL': settings.MEDIA_URL}
        return render(request, 'userpage.html', context)
    
def view_individual_shop(request, shopid, service, area, city):
    try:
        shop_obj_id = ObjectId(shopid)
    except Exception:
        return render(request, 'error.html', {'message': 'Invalid shop ID'})

    shops = shop_details.find({
        'shop_category': service,
        'area': area,
        'city_name': city,
        '_id': shop_obj_id
    })

    context = {
        'shops': shops,
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request, 'individual_shops.html', context)

def delete_shop(request):
    error=False
    shop_photo_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_photo')
    owner_photo_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_owner')
    other_photos_subfolder = os.path.join(settings.MEDIA_ROOT, 'shop_others')
    emailid = request.session.get('service_emailid')  # Assuming you're getting the emailid from the session
    if request.method=='POST':
        emailid = request.session.get('service_emailid')
        shop_id=request.POST['id']
        print("Shop ID is:",shop_id)
        shop_individual=shop_details.find_one({'_id':ObjectId(shop_id)})
        if shop_individual:
            shop_photo=shop_individual.get("shop_photo")
            other_photos=shop_individual.get("other_photos")
            owner_photo=shop_individual.get("owner_photo")
            if shop_photo:
                shop_photo_path = os.path.join(shop_photo_subfolder, shop_photo)
                if os.path.exists(shop_photo_path):
                    os.remove(shop_photo_path)
                    print(f"Image Deleted:{shop_photo}")
                else:
                    print(f"Image not deleted:{shop_photo}")
            if owner_photo:
                owner_photo_path=os.path.join(owner_photo_subfolder,owner_photo)
                if os.path.exists(owner_photo_path):
                    os.remove(owner_photo_path)
                    print(f"Image deleted:{owner_photo_path}")
                else:
                    print(f"Image not deleted:{owner_photo_path}")
            if other_photos and isinstance(other_photos,list):
                for op in other_photos:
                    op_path=os.path.join(other_photos_subfolder,op)
                    if os.path.exists(op_path):
                        os.remove(op_path)
                        print(f"Image deleted:{op_path}")
                    else:
                        print(f"Image not deleted:{op_path}")
            #Correct delete operation here
            shop_details.delete_one({'_id': ObjectId(shop_id)})
            message = "Deleted Successfully"
            error = True
            # Refresh the shop list
            shops_data = []
            shops = shop_details.find({'emailid': emailid})
            for sp in shops:
                sp['shop_id'] = str(sp['_id'])
                shops_data.append(sp)
        context = {'shops': shops_data, 'error': error, 'message': message}
    return render(request,'view_shops_provider.html',context)

def delete_service(request):
    error=False
    if request.method=='POST':
        service_id=ObjectId(request.POST['id'])
        service_collection.delete_one({'_id':service_id})
        error=True
        message='Service Deleted'
        services_data=[]
        services=service_collection.find()
        for sr in services:
            sr['service_id']=str(sr['_id'])
            services_data.append(sr)
        context={'services':services_data,'error':error,'message':message}
    return render(request,'service.html',context)


def users_list(request):
    users_list=collection_name.find()
    context={'users':users_list}
    error=False
    message=""
    if request.method=='POST':
        phoneno=request.POST['phoneno']
        collection_name.delete_one({'phoneno':phoneno})
        error=True
        message="User deleted"
        users_list=collection_name.find()
        context={'users':users_list,'error':error,'message':message}
    return render(request,"users_list.html",context)


def service_provider_list(request):
    service_provider=service_provide_collection.find()
    context={'service_provider':service_provider}
    error=False
    message=""
    if request.method=='POST':
        phoneno=request.POST['phoneno']
        service_provide_collection.delete_one({'phoneno':phoneno})
        error=True
        message="Service provider deleted"
        service_provider=service_provide_collection.find()
        context={'service_provider':service_provider,'error':error,'message':message}
    return render(request,"service_provider_list.html",context)

def admin_page(request):
    count_services=service_collection.count_documents({})
    count_service_provider=service_provide_collection.count_documents({})
    count_users=collection_name.count_documents({})
    users_list=collection_name.find().limit(5)
    service_provider=service_provide_collection.find().limit(5)
    services=service_collection.find().limit(5)
    context={'services':services,'service_provider':service_provider,'users':users_list,'user_count':count_users,'service_count':count_services,'provider_count':count_service_provider}
    return render(request,'admin_page.html',context)

def show_directions(request):
    return render(request, 'directions.html')

