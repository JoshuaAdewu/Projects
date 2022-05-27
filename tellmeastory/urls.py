from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin

app_name = "tellmeastory"
urlpatterns = [
    path("", views.register, name="register"),
    path("index/", views.index, name="index"),
    path("account/<str:username>/", views.account, name="account_page"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout , name="logout") ,
    path("register/", views.register, name="register"),
    path("map/" , views.map , name="map") ,
    path("addtags/", include("managetags.urls")),


    #edit post page
    path('modify/<post_id>', views.editPost, name="editPost"),

    #delete post page (just deletes and redirects not an actual page)
    path('delete/<post_id>', views.deletePost, name="deletePost"),

    #all post page
    path('allPosts/', views.viewPost, name="viewPosts"),

    #delete post page (just deletes and redirects not an actual page)
    path('report/<post_id>', views.reportPost, name="reportPost"),

    #admin report page
    path('adminReportList/', views.adminReportPage, name="adminReportPage"),

    #delete post page (just deletes and redirects not an actual page)
    path('adminReport/<report_id>', views.adminReportPost, name="adminReportPost"),

    #banned page
    path('banned/', views.banned, name="bannedPage"),

    #standard django admin path
    path('admin/', admin.site.urls),
  

    path("profile/<str:username>/", views.profile, name="profile"),
    path("addtags/", include("managetags.urls")),

    path("addnodeimage/", views.add_image, name="add_node_image"),
    path("create-story/", views.create_node, name="create_story"),

    path("author-story/<str:username>/", views.author_story, name="author_story"),
    path("author-story/<str:username>/<str:longitude>/<str:latitude>/", views.author_story, name="author_storyll"),
    path("search/<str:username>/", views.search_results, name="search_results"),

    path('post/<post_id>/' , views.post , name="post") ,

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

