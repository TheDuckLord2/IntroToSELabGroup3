from django.db import models

class UserCreation(models.Model):
    #primary_key makes it start at that field, avoids unreal fields
    username = models.CharField(max_length=25,primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'created_users'