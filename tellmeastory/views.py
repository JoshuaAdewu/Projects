import json
import uuid
from django.http import HttpRequest , HttpResponse , HttpResponseRedirect , HttpResponseForbidden , Http404
from django.shortcuts import get_object_or_404 , render
from hashlib import sha512
from .forms import LoginForm , AccountForm , AddImageForm , NodeCreationForm , RegisterForm , PostStoryForm , \
    ReportForm , PostForm
from managetags.models import Tag
from typing import Any , Dict
from .models import User , Report , Ban , Node
from .constants import *
from django.shortcuts import render , redirect
from django.core.exceptions import PermissionDenied
import uuid

API_TOKEN = APIKEY
COOKIE_NAME: str = "StoryUserLoggedIn"


# temp, obviously
def index(req: HttpRequest) -> HttpResponse:
    # if the user has a cookie, they've already logged in
    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    return render(req , "tellmeastory/index.html" , {
        "logged_in_username": logged_user
    })


# account stub for now
def account(req: HttpRequest , username) -> HttpResponse:
    # check if the person logged in has been banned already
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # get the current user object from the database
    user: User = get_object_or_404(User , username=username)

    form: AccountForm = None
    form_msg: str = ""

    # 0 = No message
    # 1 = Success
    # -1 = Error
    msg_type = 0;

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    if req.COOKIES.get(COOKIE_NAME) == username:
        if req.method == "POST":
            form = AccountForm(req.POST)

            # update the User model and check if the new
            # display name is valid
            old_dname: str = user.display_name

            if form["edit_blurb"].value() != user.user_blurb and form["edit_blurb"].value() != None:
                user.user_blurb = form["edit_blurb"].value().strip()
                user.save()
                msg_type = 1
                form_msg = form_msg + "Successfully changed user blurb."

            if form["new_display_name"].value() != user.display_name and form["new_display_name"].value() != None:
                old_dname: str = user.display_name
                user.display_name = form["new_display_name"].value().strip()

                if user.is_valid_display_name():
                    user.save()
                    msg_type = 1;
                    form_msg = form_msg + "Successfully changed display name."
                else:
                    user.display_name = old_dname
                    msg_type = -1;
                    form_msg = form_msg + "Failed to change display name."

        else:
            # just display the form if the cookie is present and
            # we aren't trying to post data
            form = AccountForm()

    return render(req , "tellmeastory/account.html" , {
        "user": user ,
        "form": form ,
        "change_message": form_msg ,
        "message_type": msg_type ,
        "logged_in_username": logged_user
    })


# https://docs.djangoproject.com/en/4.0/topics/forms/
def login(req: HttpRequest) -> HttpResponse:
    form: LoginForm = None
    err_msg: str = None

    if req.method == "POST":
        form: LoginForm = LoginForm(req.POST)

        if form.is_valid():
            username: str = form["username"].value().strip()

            # im just now realizing this means we're sending a password in the clear...
            # too bad!
            # (just kidding... I'll fix this...)
            password: str = sha512(form["password"].value().encode("utf-8")).hexdigest()
            form = LoginForm()

            user: User = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                err_msg = "No account with that username."

            # only validate password iff user account was found
            if not err_msg:
                if user.password == password:
                    # using a cookie here...
                    # super spoofable. Too bad!
                    # cookie will be valid until the browser is closed (i.e. max_age=None)
                    res: HttpResponse = HttpResponseRedirect(f"/story/account/{username}")
                    res.set_cookie(
                        COOKIE_NAME ,
                        username
                    )

                    return res
                else:
                    err_msg = "Incorrect password."

    else:
        form: LoginForm = LoginForm()

    return render(req , "tellmeastory/login.html" , {
        "form": form ,
        "error_message": err_msg
    })


# https://docs.djangoproject.com/en/4.0/topics/forms/
def register(req: HttpRequest) -> HttpResponse:
    form: RegisterForm = None
    err_msg: str = None

    if req.method == "POST":
        form = RegisterForm(req.POST)

        if form.is_valid():

            # display_name is optional--
            # if one isn't specified, default the username
            display_name: str = form["display_name"].value()
            if display_name is None or not len(display_name):
                display_name = form["username"].value()

            # email needed
            mail_e: str = form.cleaned_data["email"]

            # check if the username was banned
            checkBan = Ban.objects.filter(bannedUser=str(form["username"].value()))

            # hash the user's password for at least a bit of security
            hashed_pw: str = sha512(form["password"].value().encode("utf-8")).hexdigest()




            #check if the user is above 18, then assign the boolean value

            #if this was realistic then we'd check for id's etc

            mature = True

            if (int(form["maturity"].value()) < 18):
                mature = False




            new_user: User = User(
                username=form["username"].value(),
                password=hashed_pw,
                display_name=display_name,
                email=mail_e,
                mature=mature
            )

            form = RegisterForm()
            # TODO: Make these more informative?
            if not new_user.is_valid_username():
                err_msg = "Invalid username."
            elif not new_user.is_unique_username():
                err_msg = "Username is already taken."
            elif not new_user.is_valid_display_name():
                err_msg = "Invalid display name."
            elif len(mail_e) < 5:
                err_msg = "Email must be at least 5 char long."
            elif not new_user.unique_email():
                err_msg = "Email is already taken."
            elif checkBan.exists():
                err_msg = "That username is banned."
            else:
                new_user.save()
                return HttpResponseRedirect("/story/login/")

    else:
        form = RegisterForm()

    return render(req , "tellmeastory/register.html" , {
        "form": form ,
        "error_message": err_msg
    })


# may need location data as args, not sure
def create_node(req: HttpRequest) -> HttpResponse:
    form: NodeCreationForm = None
    logged_in: bool = False
    err_message: str = None

    # the cookie stores the username.
    # grab the stored username, then follow the generic steps
    alleged_username: str = req.COOKIES.get(COOKIE_NAME)
    if alleged_username:
        user: User = None
        try:
            user = User.objects.get(username=alleged_username)
            logged_in = True
        except User.DoesNotExist:
            err_message = "We could not find your account..."

        if req.method == "POST":
            form: NodeCreationForm = NodeCreationForm(req.POST)

            if form.is_valid():
                # gather all of the form data and make the node
                # ISSUE: I have no idea why, but I get kwarg issues
                #   on longitude and latitude...

                # create a post id
                create_post_id = uuid.uuid1()
                checkID = Node.objects.filter(post_id=create_post_id)
                while (checkID.count() != 0):
                    create_post_id = uuid.uuid1()
                    checkID = Node.objects.filter(post_id=create_post_id)

                node_args: Dict[str , Any] = {
                    "image": None ,
                    "node_title": form["node_title"].value().strip() ,
                    "node_content": form["node_content"].value().strip() ,
                    # "longitude": 0,
                    # "latitude": 0,
                    "node_author": user ,
                    "post_id": create_post_id
                }

                new_node: Node = Node(**node_args)
                # validate the new node
                # TODO: make these more informative?
                if not new_node.is_valid_title():
                    err_message = "Invalid title."
                elif not new_node.is_valid_content():
                    err_message = "The content must be less than 10,000 characters!"
                else:
                    new_node.save()
                    if form["mature_node"].value():
                        new_node.attach_mature_tag()

                    # this should redirect to VIEWING the node
                    # for now, I'll just go to the index
                    return HttpResponseRedirect("/story/")
        else:
            form = NodeCreationForm()

    return render(req , "tellmeastory/make_node.html" , {
        "form": form ,
        "logged_in": logged_in ,
        "error_message": err_message
    })


# need some node id
"""def view_node(req: HttpRequest, node_id: int) -> HttpResponse:
    # get id or 404, display node
    return"""


def map(req: HttpRequest) -> HttpResponse:
    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    # check if the current user logged in has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")


    # retrieve all of the nodes in [(long, lat), title] table format
    # this is passed to our map file
    data = [(
        (float(node.longitude) , float(node.latitude)) ,
        node.node_title
    ) for node in Node.objects.all()]


    # Converts our data to JSON format
    CONVERT_JSON = json.dumps(data)
    return render(req , "tellmeastory/map.html" , {
        "mapbox_token": API_TOKEN ,
        "map_data": CONVERT_JSON ,
        "logged_in_username": logged_user ,
    })


# Remove a post then redirect to all the posts of the current user (needs a confirm prompt)
def deletePost(req: HttpRequest , post_id) -> HttpResponse:
    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    # if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # get the current post
    post = Node.objects.filter(post_id=post_id)

    # if the post does not exists raise a 404 error for now
    if post.exists() == False:
        raise Http404

    post = Node.objects.get(post_id=post_id)

    # if another user is trying to edit someone else's post
    current_post_user = str(post.node_author)
    if (current_post_user != username):
        return HttpResponseRedirect("/profile/{0}/".format(current_post_user))

    get_user = str(post.node_author)

    # delete current post
    post.delete()

    # redirect to the users page
    return redirect("/profile/{0}/".format(get_user))


# Editing a post chosen by the current user redirect to all the posts of the current user (includes input validation based off the model)
def editPost(req: HttpRequest , post_id) -> HttpResponse:
    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)


    user = User.objects.get(username=username)
    # if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # get current post
    post = Node.objects.filter(post_id=post_id)

    # if the post does not exists raise a 404 error for now
    if post.exists() == False:
        raise Http404

    post = Node.objects.get(post_id=post_id)

    # if another user is trying to edit someone else's post
    current_post_user = str(post.node_author)
    if (current_post_user != username):
        return HttpResponseRedirect("/profile/{0}/".format(current_post_user))

    form= PostForm(instance=post)

    get_user = str(post.node_author)
    if req.method == "POST":
        # get the form for posting
        form = PostForm(data=req.POST, files=req.FILES, instance=post)
        # if the fields are valid, save and redirect
        if form.is_valid():
            form.save()
            return redirect("/profile/{0}/".format(get_user))

    # form is a form specified by forms.py, post becomes the Post object specified by the post_id

    return render(req, 'tellmeastory/editPost.html',
                    {
                       'form': form,
                       'post': post,
                       'logged_in_username': username,
                       'user': user
                    })


# Viewing all the post's in the database
def viewPost(req: HttpRequest) -> HttpResponse:
    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    # if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # posts are all the posts in the database
    posts = Node.objects.all()

    # pass all the objects to the html page
    return render(req , 'tellmeastory/viewAllPosts.html' ,
                  {
                      'posts': posts ,
                      'username': str(username) ,
                  })


def reportPost(req: HttpRequest , post_id) -> HttpResponse:
    # get the current user
    currentUser = req.COOKIES.get(COOKIE_NAME)

    # check if the current user is banned first
    checkBan = Ban.objects.filter(bannedUser=currentUser)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # get the current post and the form we need
    post = Node.objects.get(post_id=post_id)
    form = ReportForm(req.POST or None , instance=post)

    # get the current user
    getUser = User.objects.get(username=currentUser)

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    # if the fields are valid, save and redirect
    if form.is_valid():

        # get a report id
        taken_id = True

        # get a random id
        getId = None
        while (taken_id == True):
            getId = str(uuid.uuid4())
            try:
                Report.objects.get(id_for_report=getId)
            except Report.DoesNotExist:
                taken_id = False

        # get a report object

        new_report = Report(reporting_username=getUser, reported_user=post.node_author,
                            report_reason=form.cleaned_data.get('report_reason'), id_for_report=getId,
                            post=Node.objects.get(post_id=post_id))

        # save the new report to the database and redirect to all the posts
        Report.save(new_report)
        return redirect("tellmeastory/map.html")

    # form is a form specified by forms.py, post becomes the Post object specified by the post_id

    return render(req, 'tellmeastory/reportPost.html',
                  {'form': form,
                   'post': post,
                   'node_author': str(post.node_author),
                    'logged_in_username': logged_user
                   })


# Admin view for viewing reports
def adminReportPage(req: HttpRequest) -> HttpResponse:
    # get current user
    username = req.COOKIES.get(COOKIE_NAME)

    # check if the current user is banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # posts are all the posts in the database
    reports = Report.objects.all()

    # get the current user to check privileges
    user = User.objects.get(username=username)

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    # if the user is not an admin, deny permission to view the website
    if (user.admin == False):
        raise PermissionDenied
    else:
        # pass all the objects to the html page
        return render(req , 'tellmeastory/adminReportPage.html' ,
                      {
                          'reports': reports,
                          'user': user,
                          'logged_in_username': logged_user
                      })


def adminReportPost(req: HttpRequest , report_id) -> HttpResponse:
    username = req.COOKIES.get(COOKIE_NAME)

    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    # get the current user to check privileges
    user = User.objects.get(username=username)

    # get the report from the database
    report = Report.objects.get(id_for_report=report_id)

    reported_username = str(report.reporting_username)

    # if the user is not an admin, deny permission to view the website
    if (user.admin == False):
        raise PermissionDenied
    else:
        # if a dropdown option is saved
        if req.method == "POST":

            # get the dropdown option (Ban or Delete)
            getChoice = req.POST["choice"]

            # Ban the offender
            if (getChoice) == "Ban":
                reportedUser = str(report.reported_user)
                Ban.save(Ban(bannedUser=str(reportedUser)))
                User.objects.get(username=reportedUser).delete()
            # Delete the report
            else:
                Report.delete(report)

            # redirect to a list of the reports
            return HttpResponseRedirect("/adminReportList/")
        else:
            # pass all the objects to the html page
            return render(req , 'tellmeastory/adminReportPost.html' ,
                          {
                              'report': report,
                              'reported_username': reported_username,
                              'logged_in_username': username,
                              'user': user
                          })


# Ban page
def banned(req: HttpRequest) -> HttpResponse:
    return render(req , 'tellmeastory/ban.html')


# Takes an existing node to add an image onto it
def add_image(req: HttpRequest) -> HttpResponse:
    err_msg: str = "Please enter only one image field and an id from an existing Node."
    all_nodes = Node.objects.filter()
    # Verify a valid POST request
    if req.method == "POST":
        form = AddImageForm(req.POST)
        if form.is_valid():
            # Check if Node object is given, otherwise prompt
            # with undefined node error.
            # TODO: Redirect to view all Nodes page
            #  once Node page is created for an account.
            node = form["node_id"].value()
            if Node.objects.filter(id=node).exists():
                node = Node.objects.get(id=node)
            else:
                node = None
            if node is None:
                err_msg = "Undefined Node. Image cannot be attached to this node. Please try another node."
            # Otherwise, try to attach new image given
            else:
                # Null image if empty
                try:
                    image_file = req.FILES.get('image_file' , None)
                except:
                    # Image_file should be none if no files given.
                    # Failsafe if get throws an exception instead
                    # of setting image_file to None for no files.
                    image_file = None
                image_url: str = form["image_url"].value()
                # Null url if blank
                if image_url == "":
                    image_url = None
                # If Node receives an image from an image file
                if image_file is not None and image_url is None:
                    # Only save if new image is valid
                    if node.add_image(newFile=image_file):
                        node.save()
                        err_msg = "Thank you! Your node has been updated for Node id: " + str(node.id)
                    else:
                        err_msg = "Undefined Image. Please try again."
                # If Node receives an image from an url
                elif image_url is not None and image_file is None:
                    # Only save if new image is valid
                    if node.add_image(newURL=image_url):
                        node.save()
                        err_msg = "Thank you! Your node has been updated for Node id: " + str(node.id)
                    else:
                        err_msg = "Invalid Image URL. Please try again."
                # If Node receives no image or two images (retains features)
                elif image_url is not None and image_file is not None:
                    err_msg = "Try again. Please enter only one one field."
                # If no images are given (retains features)
                else:
                    err_msg = "Try again. No image given."
        # Reprompt for another change with applied new changes
        # Provide an error message if relevant. Otherwise,
        # provide a success message.
        return render(req , "tellmeastory/addnodeimage.html" , {
            "form": form ,
            "err_msg": err_msg ,
            "image_file": None ,
            "image_url": None ,
            "id": None ,
            "nodes": all_nodes
        })
    # Otherwise, prompt for image source info to add to node
    else:
        return render(req , "tellmeastory/addnodeimage.html" , {
            "form": AddImageForm ,
            "err_msg": err_msg ,
            "image_file": None ,
            "image_url": None ,
            "id": None ,
            "nodes": all_nodes
        })


def profile(req: HttpRequest , username: str) -> HttpResponse:
    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")
    user: User = None

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return render(req , "tellmeastory/profileNotFound.html" , {
            "logged_in_username": logged_user ,
        })

    storiesFromUser = Node.objects.filter(node_author=user)
    storyCount = storiesFromUser.count()

    return render(req , "tellmeastory/profile.html" , {
        "user": user ,
        "logged_in_username": logged_user ,
        "stories": storiesFromUser ,
        "story_count": storyCount ,
    })


def author_story(
        req: HttpRequest ,
        username: str ,
        longitude: str = "0.0" ,
        latitude: str = "0.0"
) -> HttpResponse:
    user: User = get_object_or_404(User , username=username)
    err_msg = None
    all_nodes = Node.objects.filter()
    my_nodes = []
    all_tags = Tag.objects.filter()

    # set default display values for form data
    init_dict = {
        "node_title": "" ,
        "node_content": "" ,
        "image_file": "" ,
        "image_url": "" ,
        "main_tag_id": "" ,
        "mature_node": "" ,
        "longitude": float(longitude) ,
        "latitude": float(latitude) ,
    }
    form = PostStoryForm(None , initial=init_dict)

    logged_user: str = req.COOKIES.get(COOKIE_NAME)

    # Find all of a user's stories
    if logged_user == username:
        # User account should exist, otherwise they have no nodes
        try:
            user = User.objects.get(username=username)
            for curNode in all_nodes:
                if curNode.node_author == user:
                    my_nodes.append(curNode)
        except User.DoesNotExist:
            my_nodes = []

    # If POST, then process new node authored by user, else
    # send to node creation page.
    if req.method == "POST":
        # Check for a valid POST request and that
        # the given username is what their cookie
        # shows.
        form: PostStoryForm() = PostStoryForm(req.POST)
        if form.is_valid():
            if logged_user == username:
                # User account should exist, otherwise send them
                # to the login page.
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    err_msg = "Account does not exist."
                    form: LoginForm = LoginForm()
                    return render(req , "tellmeastory/login.html" , {
                        "form": form ,
                        "error_message": err_msg
                    })
                # CREATE STORY NODE FROM PROVIDED INFORMATION
                # Null image if empty
                try:
                    image_file = req.FILES.get('image_file' , None)
                except:
                    # Image_file should be none if no files given.
                    # Failsafe if get throws an exception instead
                    # of setting image_file to None for no files.
                    image_file = None
                image_url = form["image_url"].value()
                # Null url if blank
                if image_url == "":
                    image_url = None
                err_msg = user.post_node({
                    "node_title": form["node_title"].value().strip() ,
                    "node_content": form["node_content"].value().strip() ,
                    "image_file": image_file ,
                    "image_url": image_url ,
                    "main_tag_id": form["main_tag_id"].value() ,
                    "mature_node": form["mature_node"].value() ,
                    "latitude": float(form["latitude"].value()) ,
                    "longitude": float(form["longitude"].value())
                })
                # Present error if any exists, update my nodes and present
                # blank form.
                form = PostStoryForm()
                return render(req , "tellmeastory/author_a_node.html" , {
                    "user": user ,
                    "form": form ,
                    "error_message": err_msg ,
                    "nodes": my_nodes ,
                    "tags": all_tags ,
                    "logged_in_username": logged_user
                })
            # If cookie does not match username, send to
            # login page.
            else:
                form: LoginForm = LoginForm()
                err_msg = "Account not found. Try adding a story later."
                return render(req , "tellmeastory/login.html" , {
                    "form": form ,
                    "error_message": err_msg
                })
        else:
            # Reprompt when invalid form is submitted
            form = PostStoryForm(req.POST)
            err_msg = "Invalid Story. All fields are required except the image. Only one image is allowed."
            return render(req , "tellmeastory/author_a_node.html" , {
                "user": user ,
                "form": form ,
                "error_message": err_msg ,
                "nodes": my_nodes ,
                "tags": all_tags ,
                "logged_in_username": logged_user
            })
    # Prompt with node creation page.
    else:
        # Render the page with node creation form and
        # all nodes of current user.
        return render(req , "tellmeastory/author_a_node.html" , {
            "user": user ,
            "form": form ,
            "error_message": err_msg ,
            "nodes": my_nodes ,
            "tags": all_tags ,
            "logged_in_username": logged_user
        })


def search_results(req: HttpRequest , username: str) -> HttpResponse:
    err_msg = None
    all_nodes = Node.objects.filter()
    all_tags = Tag.objects.filter()
    logged_user: str = req.COOKIES.get(COOKIE_NAME)
    found_stories = []  # all stories matching query
    search_query = req.GET['search_query']
    # If POST, then proceed to search using given search,
    # else send to login.
    if req.method == "GET":
        # Check for a valid POST request and that
        # the given username is what their cookie
        # shows.
        if logged_user == username:
            # User account should exist, otherwise send them
            # to the login page.
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                err_msg = "Account does not exist. Only users who sign in can search."
                form: LoginForm = LoginForm()
                return render(req , "tellmeastory/login.html" , {
                    "form": form ,
                    "error_message": err_msg
                })
            # Find all matching stories from request
            # ACTUAL RESULTS ARE SEARCHED FOR HERE
            # If user is signed up without being mature,
            # account for the that in the search results.
            if user.mature:
                for node in all_nodes:
                    # Search for partial matching author names
                    if str(search_query).lower() in str(node.node_author).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for partial matching content
                    if str(search_query).lower() in str(node.node_content).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for exact matching tags
                    for tag in node.other_tags.all():
                        if str(tag.name_text) == search_query:
                            # Skip duplicate stories
                            if node not in found_stories:
                                found_stories.append(node)
                            break
                    # Search for partial matching titles
                    if str(search_query).lower() in str(node.node_title).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for partial matching urls
                    if str(search_query).lower() in str(node.image_url).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
            # Immature users receive results that do not
            # include mature content.
            else:
                for node in all_nodes:
                    # Skip mature nodes
                    isMature = False
                    for tag in node.other_tags.all():
                        if "Mature" == tag.name_text:
                            isMature = True
                    if isMature:
                        continue
                    # Search for partial matching author names
                    if str(search_query).lower() in str(node.node_author).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for partial matching content
                    if str(search_query).lower() in str(node.node_content).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for exact matching tags
                    for tag in node.other_tags.all():
                        if str(tag.name_text) == search_query:
                            # Skip duplicate stories
                            if node not in found_stories:
                                found_stories.append(node)
                            break
                    # Search for partial matching titles
                    if str(search_query).lower() in str(node.node_title).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
                    # Search for partial matching urls
                    if str(search_query).lower() in str(node.image_url).lower():
                        # Skip duplicate stories
                        if node not in found_stories:
                            found_stories.append(node)
            return render(req , "tellmeastory/searchResults.html" , {
                "logged_in_username": user ,
                "error_message": err_msg ,
                "isResult": True ,
                "nodes": found_stories ,
                "search_query": search_query
            })
        # If cookie does not match username, send to
        # login page.
        else:
            form: LoginForm = LoginForm()
            err_msg = "Account not found. Try searching later."
            return render(req , "tellmeastory/login.html" , {
                "form": form ,
                "error_message": err_msg
            })
    # No search content was given from a valid search request.
    # The search page cannot be reached unless the user uses
    # the search bar.
    else:
        err_msg = "Please search using the search bar while logged into an account."
        form: LoginForm = LoginForm()
        return render(req , "tellmeastory/login.html" , {
            "form": form ,
            "error_message": err_msg
        })

def post(req: HttpRequest , post_id: str) -> HttpResponse:
     logged_user: str = req.COOKIES.get("StoryUserLoggedIn")
     postStr: Node = None;
     post = Node.objects.filter(post_id=post_id)

     # if the post does not exists raise a 404 error for now
     if post.exists() == False:
         return render(
             req , "tellmeastory/storyNotFound.html"
         )
     postStr = Node.objects.get(post_id=post_id)

     postAuthor = User.objects.get(id=postStr.node_author_id)

     reactions = [];
     UserLogged = None;

     if logged_user:
         UserLogged = User.objects.get(username=logged_user)


     if req.method == "POST":
         data = req.POST
         action = data.get("react")
         if postStr.is_user_reacted_with_emoji(action , UserLogged) == False and UserLogged != None:
             postStr.add_reaction(action , UserLogged)

     reactions.append(postStr.num_reactions_of_emoji("heart"))
     reactions.append(postStr.num_reactions_of_emoji("laugh"))
     reactions.append(postStr.num_reactions_of_emoji("thumbsup"))
     reactions.append(postStr.num_reactions_of_emoji("thumbsdown"))
     reactions.append(postStr.num_reactions_of_emoji("angry"))

     return render(req , "tellmeastory/post.html" , {
         "reactions": reactions ,
         "ismature": postStr.is_mature(),
         "post": postStr ,
         "logged_in_username": logged_user ,
     })
    
def logout(req: HttpRequest) -> HttpResponse:
    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    if logged_user:
        res: HttpResponse = HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))
        res.delete_cookie(
            COOKIE_NAME
        )
        return res;
