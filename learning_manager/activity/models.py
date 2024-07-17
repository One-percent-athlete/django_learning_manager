from django.db import models
from django.contrib.auth.models import User

from course.models import Course, Lesson

class Activity(models.Model):
    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='activities', on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    INPROGRESS = 'inprogress'
    DONE = 'done'

    STATUS_CHOICES = (
        (INPROGRESS, 'In Progress'),
        (DONE, 'Done')
    )

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=INPROGRESS)

    class Meta:
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.course} - {self.lesson} - {self.status}"