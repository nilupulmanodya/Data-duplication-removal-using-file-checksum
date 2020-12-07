from django.shortcuts import render, redirect
from django.contrib.auth.models import User as A_U
from django.http import HttpResponse, Http404
from .forms import createUser, temUpload, fileShare
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import hashlib
import os
from django.conf import settings
from .filters import UploadFilter, ShareFilter, UsersFilter, BlockedUsersFilter
import mimetypes
from .decorators import unauthenticated_user, allowed_users,adminonly, useronly


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = createUser()
    if request.method == 'POST':
        form = createUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name="user")
            user.groups.add(group)

            create_user = User(name = username)
            create_user.save()

            messages.success(request, 'Account created Success for '+username)
            return redirect('login')
    context = {'form': form}
    return render(request,'ddp/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password incorrect")
    context = {}
    return render(request, 'ddp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    #return HttpResponse('sfsefse')
    return render(request, 'ddp/dashboard.html')

@useronly
@allowed_users(allowed_roles=['user','admin'])
@login_required(login_url='login')
def profileUser(request, pk):
    ur = request.user
    uploads = Uploads.objects.filter(uploaded_by=str(ur))

    myfilter = UploadFilter(request.GET, queryset=uploads)
    uploads = myfilter.qs

    shares = Shared.objects.filter(shared_to=str(ur))

    mysharefilter = ShareFilter(request.GET, queryset=shares)
    shares = mysharefilter.qs




    context = {'upload_filters': myfilter, 'shares':shares, 'uploaded_files':uploads, 'mysharefilter':mysharefilter,
               }
    return render(request, 'ddp/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def temupload(request, pk):
    t_title=''
    t_file=''

    UP_form = temUpload()
    if request.method == 'POST':
        print("POST")
        form = temUpload(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            form.save()

        tem_all = temUploads.objects.all()
        for v in tem_all:
            t_title = v.title
            t_file = os.path.join(settings.MEDIA_ROOT, str(v.tem_file))


        openedfile = open(t_file, 'rb')
        readfile = openedfile.read()

        md5hash = hashlib.md5(readfile)
        hash = md5hash.hexdigest()


        u_name = User.objects.get(name=pk)
        print(u_name)

        openedfile.close()

        all_files = Files.objects.all()
        for i in all_files:
            if str(i.hash)==hash:
                up_hash = Files.objects.get(hash=hash)
                os.remove(os.path.join(settings.MEDIA_ROOT, str(t_file)))
                print(up_hash)
                temUploads.objects.all().delete()
                venue1 = Uploads(uploaded_by=u_name, u_title=t_title, u_hash=up_hash)
                venue1.save()

                print("deleted hash : {} title is : {} temporary saved path : {}  and all tempory datas in database... "
                      "and created value for new module (Uploads)".format(i.hash, t_title, str(t_file)))

                return redirect('user', User.name)



        venue = Files(hash=hash, path=str(t_file))
        venue.save()

        up_hash = Files.objects.get(hash=hash)
        print(up_hash)

        venue1 = Uploads(uploaded_by=u_name, u_title=t_title, u_hash=up_hash)
        venue1.save()
        temUploads.objects.all().delete()

        print("it is uncommon file ,, Set path to new Files and deleter temporary dtata")

        return redirect('user', A_U.username)


    context = {'forms': UP_form}
    return render(request, 'ddp/uploadform.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
#@allowed_users(allowed_roles=['user'])
def sharefile(request,pk_title):

    shareform = fileShare()

    if request.method == 'POST':
        form = fileShare(request.POST)

        if form.is_valid():
            print("valid Shared")

            shared_to = form.cleaned_data.get('shared_to')
            s_id = Uploads.objects.get(u_title=pk_title)
            s_hash = s_id.u_hash
            s_name = User.objects.get(name=s_id)


            shared = Shared(shared_by=s_name, shared_to=shared_to, s_title=pk_title, s_hash=s_hash)
            shared.save()

            print("Shared succesfully... data stored to shared module shared by {} , file hash : {}".format(s_name, s_hash))

            return redirect('user', User.name)



    context = {'sharefile':shareform}
    return render(request, 'ddp/shareform.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def deletefile(request, pk_title):

    if request.method == 'POST':

        deleting_file = Uploads.objects.get(u_title=pk_title)
        d_f_hash = str(deleting_file.u_hash)

        # Deleting from Uploads module
        deleting_file.delete()


        all_files = Uploads.objects.all()
        for i in all_files:
            if str(i.u_hash) == d_f_hash:
                print("file deleted from upload module..there is another file from same hash....{}".format(d_f_hash))
                return redirect('user', User.name)

#Assigning values to Delete file
        d_file = Files.objects.get(hash=d_f_hash)
        d_file_path = d_file.path

#deleting from OS
        t_file = os.path.join(settings.MEDIA_ROOT, str(d_file_path))
        os.remove(os.path.join(settings.MEDIA_ROOT, str(t_file)))
#Deleting from Files module
        d_file.delete()


        print("file deleted from data base and os, file title was: {}".format(d_file_path))

        return redirect('user', User.name)


    context = {'title':pk_title}
    return render(request,'ddp/deletefile.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def deleteshare(request, pk_title):

    if request.method == 'POST':
#Deleting from Share model
        deleting_file = Shared.objects.get(id=pk_title)
        deleting_file.delete()
        return redirect('user', User.name)

    context ={'title':pk_title}
    return render(request, 'ddp/sharedelete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['user','admin'])
def downloads(request, title):
    path=''
    try :
        hash = str(Uploads.objects.get(u_title=title).u_hash)
        path = str(Files.objects.get(hash=hash).path)
        print(path)

    except:
        return HttpResponse("File was deleted by user")


    print("start")
    #path = "upload/._FL_insurance_sample.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, 'rb')as fh:
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline;title=' + os.path.basename(file_path)
            return response

    raise Http404


@login_required(login_url='login')
@adminonly
def adminprofile(request,pk):

    uploads = Uploads.objects.all()

    myfilter = UploadFilter(request.GET, queryset=uploads)
    uploads = myfilter.qs

    shares = Shared.objects.all()

    mysharefilter = ShareFilter(request.GET, queryset=shares)
    shares = mysharefilter.qs

    users = A_U.objects.filter(groups__name='user')
    myuserfilter = UsersFilter(request.GET, queryset=users)
    users = myuserfilter.qs

    blocked_users = A_U.objects.filter(groups__name='blocked user')
    #blockuserfilter = BlockedUsersFilter(request.GET, queryset=blocked_users)
    #blocked_users = blockuserfilter.qs

    context = {'upload_filters': myfilter, 'shares': shares, 'users':users, 'uploaded_files': uploads, 'mysharefilter': mysharefilter,
               'usersfilter' : myuserfilter,'blocked_users':blocked_users }

    return render(request,'ddp/adminprofile.html',context,)

@login_required(login_url='login')
def blockuser(request, uid):
    print(uid)
    users = A_U.objects.get(username=uid)
    if request.method == 'POST':
#add user(uid) to blocked group
        b_group = Group.objects.get(name="blocked user")
        users.groups.add(b_group)
#removing user (uid) from user group
        u_group = Group.objects.get(name="user")
        users.groups.remove(u_group)
        return redirect('admin', User.name)
    #return HttpResponse("page")
    context = {'users':users}
    return render(request, 'ddp/blockuser.html', context)



def activeuser(request, uid):

    print(uid)
    blockusers = A_U.objects.get(username=uid)
    if request.method == 'POST':
        # add user(uid) to blocked group
        u_group = Group.objects.get(name="user")
        blockusers.groups.add(u_group)
        # removing user (uid) from user group
        b_group = Group.objects.get(name="blocked user")
        blockusers.groups.remove(b_group)
        return redirect('admin', User.name)
    # return HttpResponse("page")
    context = {'users': blockusers}
    return render(request, 'ddp/activeuser.html', context)

