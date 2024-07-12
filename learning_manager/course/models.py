from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(max_length=100, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'

    LESSON_STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    ARTICLE = 'article'
    QUIZ = 'quiz'

    LESSON_TYPE = (
        (ARTICLE, 'Article'),
        (QUIZ, 'Quiz')
    )

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(max_length=100, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    lesson_status = models.CharField(max_length=20, choices=LESSON_STATUS, default=DRAFT)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE, default=ARTICLE)

    def __str__(self):
        return self.title