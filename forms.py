from django.forms import Form, CharField, PasswordInput, FileField

class RegistrationForm(Form):
    username = CharField(max_length=50)
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=50)
    pic = FileField()

class UpdateProfileForm(Form):
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=50)

class UpdatePICForm(Form):
    pic = FileField()

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class PostForm(Form):
    title = CharField(max_length=30000)
    image = FileField()

class CommentForm(Form):
    post = CharField(max_length=60)
    comment = CharField(max_length=3000)

class LikeOrDisLikeForm(Form):
    post = CharField(max_length=60)
    likeOrDislike = CharField(max_length=100)

class ServiceForm(Form):
    service = CharField(max_length=100)
    description = CharField(max_length=10000)

class ServiceRatingForm(Form):
    service = CharField(max_length=60)
    rating = CharField(max_length=100)
