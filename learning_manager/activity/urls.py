from django.urls import path

from . import views

urlpatterns = [
    path('get_active_courses/', views.get_active_courses),
    path('track_progress/<slug:course_slug>/<slug:lesson_slug>/', views.track_progress),
    path('track_done/<slug:course_slug>/<slug:lesson_slug>/', views.track_done),

]