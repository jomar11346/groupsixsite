from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db.models import Q  # <-- Add this import
from django.core.paginator import Paginator
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from .utils import login_required_custom
from django.views.decorators.cache import never_cache
from django.contrib import messages



@never_cache
def log_in(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                # Set session variable to mark user as logged in
                request.session['user_id'] = user.pk
                return redirect('/user/list')
            else:
                messages.error(request, 'Invalid password')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username')

    return render(request, 'layout/login.html')

@login_required_custom
@never_cache
def gender_list(request):
    try:
        genders= Genders.objects.all()

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')
@login_required_custom
@never_cache
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
          return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')
@login_required_custom
@never_cache
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')
             
            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')

            data = {
            'gender': genderObj
         }
            
            return render(request, 'gender/EditGender.html', data)
        else:
         genderObj = Genders.objects.get(pk=genderId)

         data = {
            'gender': genderObj
         }

         return render(request, 'gender/EditGender.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error Occurred during edit gender: {e}')
@login_required_custom
@never_cache  
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
         genderObj = Genders.objects.get(pk=genderId)

         data = {
            'gender': genderObj
         }

         return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error Occurred during delete gender: {e}')
@login_required_custom
@never_cache  
def user_list(request):
    try:
        users = Users.objects.select_related('gender')
        search_query = request.GET.get('search', '')

        # Apply search filter if query exists
        if search_query:
            users = users.filter(
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(username__icontains=search_query)
            )

        # Pagination: limit to 10 users per page
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pass the paginated object as 'users'
        return render(request, 'user/UsersList.html', {
            'users': page_obj,  # <-- This is the key change
            'search_query': search_query,
            'genders': Genders.objects.all()
        })

    except Exception as e:
        messages.error(request, f'Error loading users: {e}')
        return redirect('/user/list')
    
@login_required_custom
def add_user(request):
    is_public = request.GET.get('public') == '1'
    template = 'user/AddUserPublic.html' if is_public else 'user/AddUser.html'
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get("username")
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                if is_public:
                    return redirect('/user/add?public=1')
                return redirect('/user/add')
            if password != confirmPassword:
                messages.error(request, 'Password and Confirm Password do not match!')
                # Redirect with the public flag if public
                if is_public:
                    return redirect('/user/add?public=1')
                return redirect('/user/add')
            

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)
            ).save()

            messages.success(request, 'User added successfully!')
            # Redirect to login if public registration, else stay on add user
            if is_public:
                return redirect('/login/')
            return redirect('/user/add')

        else:
            genderObj = Genders.objects.all()

        data = {
            'genders': genderObj
        }
        return render(request, template, data)
    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')
    
@login_required_custom
@never_cache      
# ...existing code...
@login_required_custom
@never_cache      
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')

            # Check if username exists for another user
            if Users.objects.filter(username=username).exclude(pk=userId).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                genderObj = Genders.objects.all()
                data = {
                    'user': userObj,
                    'genders': genderObj
                }
                return render(request, 'user/EditUser.html', data)

            userObj.full_name = fullName
            userObj.gender = Genders.objects.get(pk=gender)
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username
            userObj.save()

            messages.success(request, 'User updated successfully!')

        genderObj = Genders.objects.all()
        data = {
            'user': userObj,
            'genders': genderObj
        }
        return render(request, 'user/EditUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')

    
@login_required_custom
@never_cache   
def delete_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        if request.method == 'POST':
            userObj.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')
        else:
            data = {
                'user': userObj
            }
            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')
    
@login_required_custom
def password(request, userId=None):
    if not userId:
        messages.error(request, 'User ID is required to change the password.')
        return redirect('/user/list/')

    user = get_object_or_404(Users, pk=userId)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect(f'/user/password/{userId}/')

            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('/user/list')
        else:
            messages.error(request, 'Password fields cannot be empty!')

    return render(request, 'user/ChangePassword.html', {'user': user})


        
def log_out(request):
    request.session.flush()  # Clears all session data
    return redirect('login/')  # Change to your login UR
