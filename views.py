from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from cyberbullying.cyberbullying import isBullyingPost
from cyberbullying.forms import RegistrationForm, LoginForm, CommentForm, LikeOrDisLikeForm, PostForm, \
    UpdateProfileForm, UpdatePICForm
from cyberbullying.models import RegistrationModel, CommentModel, LikeOrDisLikeModel, PostModel, ShareModel, FriendRequestModel
from cyberbullying.service import getAllPostsByUser, getAllPostsBySearch, getMyFriends


def registration(request):

    status = False

    if request.method == "POST":
        # Get the posted form
        registrationForm = RegistrationForm(request.POST,request.FILES)

        if registrationForm.is_valid():

            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.address = registrationForm.cleaned_data["address"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]
            regModel.pic=registrationForm.cleaned_data["pic"]
            regModel.status="yes"

            user = RegistrationModel.objects.filter(username=regModel.username).first()

            if user is not None:
                status = False
            else:
                try:
                    regModel.save()
                    status = True
                except:
                    status = False
    if status:
        return render(request, 'index.html', locals())
    else:
        response = render(request, 'registration.html', {"message": "User All Ready Exist"})

    return response

def login(request):

    uname = ""
    upass = ""

    if request.method == "GET":
        # Get the posted form
        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

        user = RegistrationModel.objects.filter(username=uname, password=upass).first()

        if user is not None:
            request.session['username'] = uname
            request.session['role'] = "user"
            return render(request, "wall.html", {"posts":getAllPostsByUser(request.session['username'])})
        else:
            response = render(request, 'index.html', {"message": "Invalid Credentials"})

    return response

'''
def activateAccount(request):

    status = False

    username = request.GET['username']
    status=request.GET['status']

    RegistrationModel.objects.filter(username=username).update(status=status)
    return render(request, 'adminhome.html', {"users": RegistrationModel.objects.all()})
'''

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})

def addPost(request):

    status = False
    postForm = PostForm(request.POST, request.FILES)

    print("before validating")

    if postForm.is_valid():
        print("form validated")
        title = postForm.cleaned_data['title']
        image = postForm.cleaned_data['image']

        if isBullyingPost(title) is False:

            dt=datetime.now()

            print("before creating")

            new_post = PostModel(username=request.session['username'],title=title,image=image,datetime=dt)

            try:
                print("before saving")
                new_post.save()
                print("after saving")
                status = True
            except:
                status = False

            if status:
                return render(request, "wall.html", {"message": "Posted Successfully","posts":getAllPostsByUser(request.session['username'])})
            else:
                return render(request, 'wall.html', {"message": "Post Upload Failed"})

        return render(request, "wall.html",{"message": "Your Post contains bullying words!", "posts": getAllPostsByUser(request.session['username'])})

    else:
        return render(request, 'wall.html', {"message": "invalid request"})

def getposts(request):
    return render(request, "wall.html", {"posts":getAllPostsByUser(request.session['username'])})

def search(request):
    return render(request, 'wall.html', {'posts': getAllPostsBySearch(request.GET["query"])})

def postComment(request):

    form = CommentForm(request.POST)

    if form.is_valid():

        comment = form.cleaned_data['comment']
        post_id = request.POST['post']
        dt = datetime.now()

        if isBullyingPost(comment) is False:

            CommentModel(comment=comment, username=request.session['username'], post=post_id,datetime=dt).save()

            return render(request, "wall.html", {"posts": getAllPostsByUser(request.session['username'])})

        else:
            return render(request, "wall.html", {"message":"Your comment is filtered","posts": getAllPostsByUser(request.session['username'])})
    else:
        return render(request, "wall.html", {"message": "invalid request", "posts": getAllPostsByUser(request.session['username'])})

def likeOrDisLike(request):

    form = LikeOrDisLikeForm(request.GET)

    if form.is_valid():

        ld = form.cleaned_data['likeOrDislike']
        post_id = form.cleaned_data['post']

        islikedOrDisLiked=LikeOrDisLikeModel.objects.filter(username=request.session['username'], post=post_id).count()

        print(islikedOrDisLiked," is Liked?")

        if islikedOrDisLiked==1 :
            LikeOrDisLikeModel.objects.filter(username=request.session['username'],
                                                                  post=post_id).update(status=ld)
        else:
            LikeOrDisLikeModel(status=ld, username=request.session['username'], post=post_id).save()

        return render(request, "wall.html", {"posts": getAllPostsByUser(request.session['username'])})

def deletepost(request):

    post_id = request.GET['post']

    PostModel.objects.filter(id=post_id).delete()
    CommentModel.objects.filter(post=post_id).delete()
    LikeOrDisLikeModel.objects.filter(post=post_id).delete()
    ShareModel.objects.filter(post=post_id).delete()

    return render(request, "wall.html", {"posts": getAllPostsByUser(request.session['username'])})

def sharePost(request):
    ShareModel(username=request.session['username'],post=request.GET['postid']).save()
    return render(request, "wall.html", {"posts":getAllPostsByUser(request.session['username'])})

def viewfriends(request):

    friends = getMyFriends(request.session['username'])

    print("my friends :", len(friends))

    requestedusers = FriendRequestModel.objects.filter(friendname=request.session['username'], status='no')

    print("no of db requests ", len(requestedusers))

    requests = []
    for requesteduser in requestedusers:
        user = RegistrationModel.objects.filter(username=requesteduser.username).first()
        user.pic = str(user.pic).split("/")[1]
        requests.append(user)

    print("no of requests ", len(requests))

    friendslist = []

    for friend in RegistrationModel.objects.filter(username__in=friends):
        friend.pic = str(friend.pic).split("/")[1]
        friendslist.append(friend)

    print("no of friends ", len(requests))

    return render(request, "friends.html", {"friends": friendslist, "requests": requests})

def searchUsers(request):

    keyword=request.GET['keyword']
    print("keyword",keyword)
    friends = getMyFriends(request.session['username'])
    users=RegistrationModel.objects.filter(Q(username__icontains=keyword) |
                               Q( name__icontains=keyword) | Q(email__icontains=keyword) | Q(mobile__icontains=keyword))
    results=[]
    print("db users",len(users))
    for user in users:
        if user.username not in request.session['username']:
            print("in for")
            isfriend=False
            for friend in friends:
                print("for 21 ",user.username," ",request.session['username'])
                print("for 22 ", user.username, " ", friend)
                if user.username in request.session['username'] or user.username in friend:
                    isfriend=True
                    print("friend is ",friend)

            print("is Friend ? ",isfriend)

            if isfriend is False:
                user.pic= str(user.pic).split("/")[1]
                results.append(user)

            print("size",len(results))

    return render(request,"wall.html",{"results":results,"posts":getAllPostsByUser(request.session['username'])})

def sendFriendRequest(request):

    dt = datetime.now()
    FriendRequestModel(username=request.session['username'],datetime=dt,friendname=request.GET['friendname'],status='no').save()

    friends = getMyFriends(request.session['username'])

    print("my friends :",len(friends))

    requestedusers = FriendRequestModel.objects.filter(friendname=request.session['username'], status='no')

    print("no of db requests ",len(requestedusers))

    requests = []
    for requesteduser in requestedusers:
        user = RegistrationModel.objects.filter(username=requesteduser.username).first()
        user.pic = str(user.pic).split("/")[1]
        requests.append(user)

    print("no of requests ",len(requests))

    friendslist = []

    for friend in RegistrationModel.objects.filter(username__in=friends):
        friend.pic = str(friend.pic).split("/")[1]
        friendslist.append(friend)

    print("no of friends ",len(requests))

    return render(request, "friends.html", {"friends": friendslist, "requests": requests})

def acceptFriendRequest(request):

    FriendRequestModel.objects.filter(username=request.GET['friendname'],friendname=request.session['username']).update(status='yes')

    friends = getMyFriends(request.session['username'])
    requestedusers = FriendRequestModel.objects.filter(friendname=request.session['username'], status='no')

    requests = []
    for requesteduser in requestedusers:
        user = RegistrationModel.objects.filter(username=requesteduser.username)
        user.pic = str(user.pic).split("/")[1]
        requests.append(user)

    friendslist = []

    for friend in RegistrationModel.objects.filter(username__in=friends):
        friend.pic = str(friend.pic).split("/")[1]
        friendslist.append(friend)

    return render(request, "friends.html", {"friends": friendslist, "requests": requests})

def unFriend(request):

    FriendRequestModel.objects.filter(username=request.GET['friendname'],friendname=request.session['username'],status='yes').delete()
    FriendRequestModel.objects.filter(username=request.session['username'], friendname=request.GET['friendname'],status='yes').delete()

    friends = getMyFriends(request.session['username'])
    requestedusers = FriendRequestModel.objects.filter(friendname=request.session['username'], status='no')

    requests = []
    for requesteduser in requestedusers:
        user=RegistrationModel.objects.filter(username=requesteduser.username)
        user.pic = str(user.pic).split("/")[1]
        requests.append(user)

    friendslist=[]

    for friend in RegistrationModel.objects.filter(username__in=friends):
        friend.pic = str(friend.pic).split("/")[1]
        friendslist.append(friend)

    return render(request, "friends.html", {"friends": friendslist, "requests": requests})

def viewprofile(request):
    user=RegistrationModel.objects.get(username=request.session['username'])
    user.pic = str(user.pic).split("/")[1]
    return render(request, 'viewprofile.html',
                  {"profile": user})

def updateprofile(request):

    if request.method == "POST":
        # Get the posted form
        updateProfileForm = UpdateProfileForm(request.POST)

        if updateProfileForm.is_valid():

            name = updateProfileForm.cleaned_data["name"]
            email = updateProfileForm.cleaned_data["email"]
            mobile = updateProfileForm.cleaned_data["mobile"]
            address = updateProfileForm.cleaned_data["address"]
            password = updateProfileForm.cleaned_data["password"]

            RegistrationModel.objects.filter(username=request.session['username']).update(name=name,email=email,mobile=mobile,address=address,password=password)

    user = RegistrationModel.objects.get(username=request.session['username'])
    user.pic = str(user.pic).split("/")[1]

    return render(request, 'viewprofile.html', {"profile":user})

def updatepic(request):

    if request.method == "POST":

        updatepicfrom = UpdatePICForm(request.POST,request.FILES)

        if updatepicfrom.is_valid():

            image="images/"+str(updatepicfrom.cleaned_data["pic"])
            print("image path",image)

            user = RegistrationModel.objects.filter(username=request.session['username']).first()

            regModel = RegistrationModel()
            regModel.name = user.name
            regModel.email =  user.email
            regModel.mobile =  user.mobile
            regModel.address = user.address
            regModel.username = user.username
            regModel.password = user.password
            regModel.pic = updatepicfrom.cleaned_data["pic"]
            regModel.status = user.status

            RegistrationModel.objects.filter(username=request.session['username']).delete()
            regModel.save()

        user = RegistrationModel.objects.get(username=request.session['username'])
        user.pic = str(user.pic).split("/")[1]
        return render(request, 'viewprofile.html', {"profile": user})
