from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    role = models.CharField(max_length=1, choices=[
        ('S', 'Student'),
        ('A', 'Admin')
    ], default='S')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)


class Reference(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    stud = models.IntegerField()
    status = models.CharField(max_length=2, choices=[
        ('Rd', 'Received'),
        ('IP', 'In process'),
        ('Fd', 'Finished'),
        ('RR', 'Ready for receive')
    ], default='Rd')
    edu_form = models.CharField(max_length=1, choices=[
        ('F', 'Full-time'),
        ('P', 'Part-time'),
        ('D', 'Distance')
    ])
    location = models.CharField(max_length=40)
    department = models.CharField(max_length=100)
    pickup_method = models.CharField(max_length=1, choices=[
        ('S', 'Self'),
        ('D', 'PostDelivery')
    ])
    organization_for = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='stud_num_is_valid',
                check=models.Q(stud__range=(100000, 999999))
            )
        ]


class Article(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'media/post_images')
    header = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True)