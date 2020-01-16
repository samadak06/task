from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User



class userProfile(models.Model):
    STATUSES = [
        ('IS_BOOK', 'BOOK STATUS'),
        ('IS_POST', 'POST STATUS')
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    username = models.CharField( max_length=128)
    password = models.CharField( max_length=128)
    email = models.EmailField(max_length=128)
    user_type = models.CharField(choices=STATUSES, max_length=128,default='IS_BOOK')
    maximum_booking = models.IntegerField(default=5)

    class Meta:
        db_table = 'users'
        verbose_name = _('usertab')
        verbose_name_plural = _('users info')

    def __str__(self):
        return self.user.username


class LuggageType(models.Model):

    STATUSES = [
        ('FULL','FULL'),
        ('AVAILABALE','AVAILABALE')
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price =  models.IntegerField()
    status = models.CharField(choices=STATUSES,max_length=128,default='AVAILABALE')


    class Meta:
        db_table = 'Luggage'
        verbose_name = _('LuggageType')
        verbose_name_plural = _('Luggage Types')

    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(LuggageType, related_name='items', blank=True)
    booked_by = models.ForeignKey("auth.User",related_name="booked_%(class)s_objects",on_delete=models.PROTECT)
    total_price = models.IntegerField(blank=True,null=True)

    class Meta:
        db_table = 'Book'
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def Items(self):
        items = []
        for p in self.items.all():
            items.append(p.name)
        return items


#signal


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)