from django.db import models
from django.contrib.auth.models import Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone
# Create your models here.

class World(models.Model):
    world_id = models.CharField(max_length = 30, primary_key = True)
    curr = models.BooleanField(max_length = 30, default = True)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #is_prime = models.BooleanField(default=False)
    world = models.ForeignKey(World, max_length=30, on_delete = models.CASCADE)

class Truck(models.Model):
    truck_id = models.AutoField(primary_key = True)
    STATUS = (
        ('i', 'IDLE'),
        ('t', 'TRAVELING'),
        ('l', 'LOADING'),
        ('d', 'DELIVERING'))
    cur_status = models.CharField(max_length=30, choices=STATUS)
    pos_x = models.CharField(max_length=30)
    pos_y = models.CharField(max_length=30)
    world = models.ForeignKey(World, max_length=30, on_delete = models.CASCADE)

class Package(models.Model):
    package_id = models.CharField(max_length=30, primary_key = True)
    user = models.ForeignKey(Account, max_length=30, null = True, on_delete = models.CASCADE)
    truck = models.ForeignKey(Truck, max_length=30, null = True, on_delete = models.CASCADE)
    wh_id = models.CharField(max_length=30)
    wh_addr_x = models.CharField(max_length=30)
    wh_addr_y = models.CharField(max_length=30)
    dest_x = models.CharField(max_length=30)
    dest_y = models.CharField(max_length=30)
    STATUS = (
        ('p', 'wait for pick up'),
        ('o', 'out for delivery'), # should keep this one
        ('d', 'delivered'))
    cur_status = models.CharField(max_length=30, choices=STATUS)
    ready_for_pickup_time = models.CharField(max_length=30)
    load_time = models.CharField(max_length=30, null=True, blank=True)
    delivered_time = models.CharField(max_length=30, null=True)
    world = models.ForeignKey(World, max_length=30, on_delete = models.CASCADE)