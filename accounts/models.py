from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,phone,password=None,**extra_fields):

        if not phone:
            raise ValidationError('Phone number is required')
        
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits')

        if not len(phone) == 11:
            raise ValidationError('Phone number must be exactly 11 digits')
        
        participant = extra_fields.get("participant")
        organizer = extra_fields.get("organizer")

        if participant is None or organizer is None:
            raise ValidationError('Role selection is required')
        
        if participant == organizer:
            raise ValidationError('One of the roles must be True and the other False')
        
        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone,password=None,**extra_fields):
        
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        # superuser ---> organizer
        extra_fields.setdefault("participant",False)
        extra_fields.setdefault("organizer",True)

        return self.create_user(phone, password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):

    phone = models.CharField(max_length=11,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    participant = models.BooleanField(default=False)
    organizer = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created_date']

    def clean(self):
        
        if not self.phone:
            raise ValidationError('Phone number is required')
        
        if not self.phone.isdigit():
            raise ValidationError({'phone': 'Phone number must contain only digits'})

        if len(self.phone) != 11:
            raise ValidationError({'phone': 'Phone number must be exactly 11 digits'})
        
        if self.participant is None or self.organizer is None:
            raise ValidationError('Role selection is required')
        
        if self.participant == self.organizer:
            raise ValidationError('One of the roles must be True and the other False')
        
    def save(self,*args,**kwargs):

        self.full_clean()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.phone