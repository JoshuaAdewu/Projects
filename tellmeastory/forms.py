from django.forms import CharField, Form, EmailField, BooleanField, IntegerField, CharField, ImageField, ModelForm,FloatField
from .models import Node, User, Report


class LoginForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)


class RegisterForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)
    email: EmailField = EmailField(max_length=254)
    # default to the username if not specified
    display_name: CharField = CharField(max_length=200, required=False)

    maturity: CharField = CharField(max_length=3,label="Age", required=True)

class AccountForm(Form):
    # this may not need to be required?
    new_display_name: CharField = CharField(max_length=200, required=True)
    edit_blurb: CharField = CharField(max_length=1000, required=True)

#Create Post form
class PostForm(ModelForm):
    class Meta:
        #get the current Post database
        model = Node

        #controls what fields appear, MUST BE NAMED AFTER THE FIELDS IN THE DATABASE
        fields = ('node_title','node_content','image')

#Create Report form
class ReportForm(ModelForm):
    class Meta:
        #get the current Post database
        model = Report

        #controls what fields appear, MUST BE NAMED AFTER THE FIELDS IN THE DATABASE
        fields = ('report_reason',)

class NodeCreationForm(Form):
    node_title: CharField = CharField(max_length=200, required=True)
    node_content: CharField = CharField(max_length=10_000, required=True)
    mature_node: BooleanField = BooleanField(label="Is this story mature?", required=False)

class AddImageForm(Form):
    # If no image is given, then no image is added.
    image_file: ImageField = ImageField(required=False)
    image_url: CharField = CharField(max_length=200, required=False)
    node_id: IntegerField = IntegerField(required=True)


class PostStoryForm(Form):
    # If no image is given, then no image is added.
    node_title: CharField = CharField(max_length=200, required=True)
    node_content: CharField = CharField(max_length=10_000, required=True)
    image_file: ImageField = ImageField(required=False)
    image_url: CharField = CharField(max_length=200, required=False)
    main_tag_id: IntegerField = IntegerField(required=True)
    mature_node: BooleanField = BooleanField(label="Is this story mature?", required=False)
    latitude: FloatField = FloatField(required=True)
    longitude: FloatField = FloatField(required=True)

