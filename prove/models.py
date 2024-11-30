from django.db import models

# Create your models here.

class Person(models.Model):
    uid = models.CharField(max_length=12,primary_key=True)
    name = models.CharField(max_length=30, null=False)
    id_number = models.CharField(max_length=12,null=False)
    license_plate = models.CharField(max_length=15, null=False)
    date_joined = models.DateField(auto_now_add=True, null=False)
    activate = models.BooleanField(default=True, null=False)
    profile_image = models.ImageField(upload_to='profile_images/',
                                      default='profile_images/default.jpg')
    def __str__(self):
        return self.name
    
class History(models.Model):
    id = models.AutoField(primary_key=True)
    timeline = models.DateTimeField(auto_now_add=True, null=False)
    gate = models.BooleanField(null=False) # Đi vào : True  |  Đi ra : False
    person = models.ForeignKey(
        Person,
        related_name = 'histories',
        on_delete = models.CASCADE,
        null = False
    )
