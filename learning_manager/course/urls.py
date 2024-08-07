from django.urls import path
from course import views

urlpatterns = [
    path('', views.get_courses),
    path('get_categories/', views.get_categories),
    path('get_author_courses/<int:user_id>/', views.get_author_courses),
    path('homepage_courses/', views.homepage_courses),
    path('create_course/', views.create_course),
    path('<slug:slug>/', views.get_course),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.add_comment),
    path('<slug:course_slug>/<slug:lesson_slug>/comments/', views.get_comments),
    path('<slug:course_slug>/<slug:lesson_slug>/quizzes/', views.get_quiz),
]