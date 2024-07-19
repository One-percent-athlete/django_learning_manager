from django.shortcuts import render
from random import randint
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import CourseListSerializer, CourseDetailSerializer, LessonListSerializer, CommentSerializer, CategorySerializer, QuizSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Course, Lesson, Comment, Category

@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    quiz = lesson.quizzes.first()
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def homepage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED).order_by('-created_at')[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED).order_by('-created_at')

    category_id = request.GET.get('category_id', '')
    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def get_course(request, slug):
    course = Course.objects.filter(status=Course.PUBLISHED).get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer =LessonListSerializer(course.lessons.all(), many=True)

    if request.user.is_authenticated:
        course_data = course_serializer.data
    else:
        course_data = []
        
    data = {
        'course': course_data,
        'lessons': lesson_serializer.data
    }

    return Response(data) 

@api_view(['POST'])
def create_course(request):
    course = Course.objects.create(
        title=request.data.get('title'),
        slug=slugify(request.data.get('title')),
        short_description=request.data.get('short_description'),
        long_description=request.data.get('long_description'),
        status=request.data.get('status'),
        created_by=request.user
    )

    for id in request.data.get('categories'):
        course.categories.add(id)

    course.save()

    for lesson in request.data.get('lessons'):
        tmp_lesson = Lesson.objects.create(
            course=course,
            title=lesson.get('title'),
            slug='%s-%s' % (slugify(lesson.get('title')), randint(1000, 10000)),
            short_description=lesson.get('short_description'),
            long_description=lesson.get('long_description'),
            lesson_status=Lesson.DRAFT,
        )

    return Response({'course_id': course.id})

@api_view(['GET'])
def get_comments(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    title = data.get('title')
    content = data.get('content')

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    comment = Comment.objects.create(course=course, lesson=lesson, title=title, content=content, created_by=request.user)
    comment.save()

    serializer = CommentSerializer(comment)

    return Response(serializer.data)


@api_view(['GET'])
def get_author_courses(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
        'courses': courses_serializer.data,
        'created_by': user_serializer.data
    })