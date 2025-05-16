from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_required(request, user)
            return redirect('/user/list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'layout/login.html')

def gender_list(request):
    try:
        genders= Genders.objects.all()

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during load genders: {e}')

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
    
def user_list(request):
    try:
        userObj = Users.objects.select_related('gender')

        data = {
            'users': userObj
        }

        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during Load users: {e}')
def add_user(request):
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
            
            if password != confirmPassword:
                messages.error(request, 'Password and Confirm Password do not match!')
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
            return redirect('/user/add')

        else:
         genderObj = Genders.objects.all()

        data = {
            'genders': genderObj
        }
        return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')
        
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