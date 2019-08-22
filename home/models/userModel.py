"""
:synopsis: Used to define the `home.models.userModel` models
"""
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.db import models
from django.db import transaction

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)
    
class AppUserManager(models.Manager):
    """
    AppUser objects manager.
    """
    @transaction.atomic
    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        
        # set user group
        user_group = None
        if(kwargs['user_level'] == AppUser.SUBSCRIBER):
            user_group = Group.objects.get(name='Subscribers')
        elif(kwargs['user_level'] == AppUser.AUTHOR):
            user_group = Group.objects.get(name='Authors')
        elif(kwargs['user_level'] == AppUser.PUBLISHER):
            user_group = Group.objects.get(name='Publishers')
        elif(kwargs['user_level'] == AppUser.ADMIN):
            new_user.is_staff = True
            user_group = Group.objects.get(name='Administrators')
        elif(kwargs['user_level'] == AppUser.SUPER_USER):
            new_user.is_superuser = True
            user_group = Group.objects.get(name='Super_users')

        kwargs['user'].groups.set([user_group])
        kwargs['user'].save()
        
        return obj

class AppUser(models.Model):
    """
    Virtual object for the app user. 
    Has one to one relationship with django auth user.
    
    It is inherited by the models:
    
    * home.models.userModel.Admin
    * home.models.userModel.Author
    * home.models.userModel.Subscriber
    * home.models.userModel.Publisher
    """
    #: The user model which belongs to the AppUser.
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=False)
    #: The user's telephone number.
    telephone = models.CharField(max_length=100, null = True, blank=True)
    #: The user's physical address.
    address = models.CharField(max_length=100, null = True, blank=True)
    #: The user's profile picture.
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

    ADMIN = 'ADM'       #: Admin user level.
    AUTHOR = 'AUT'      #: Author user level.
    PUBLISHER = 'PUB'   #: publisher user level.
    SUBSCRIBER = 'SUB'  #: subscriber user level.
    SUPER_USER = 'SU'   #: `'super user'` user level.
    
    #: AppUser user levels
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Administrator'),
        (SUBSCRIBER, 'Subscriber'),
        (SUPER_USER, 'Super_user'),
    )
    
    user_level = models.CharField(
        max_length=3,
        choices=USER_LEVEL,
    )

    #: AppUser objects manager.
    objects = AppUserManager()

    #: The available user groups and their permissions.
    user_groups = {
        'Super_users': [],
        'Subscribers': [
            'view_article',
        ],
        'Authors': [
            'add_article',
            'change_article',
            'delete_article',
            'view_article',
        ],
        'Administrators': [
            'add_user',
            'view_user',
            'delete_user',
            'add_publisher',
            'delete_publisher',
            'view_publisher',
            'view_admin',
            'view_author',
            'delete_author',
            'view_article',
        ],
        'Publishers': [
            'add_article',
            'change_article',
            'delete_article',
            'publish_article',
            'view_article',
            'add_topic',
            'change_topic',
            'delete_topic',
            'view_topic',
        ],
    }

    def set_user_permmisions(self, user):
        """
        Set the user group permissions.
        
        :param user: Django user object to be set permission
        :type user: django.contrib.auth.models.User
        """
        try:
            user.admin
            user.groups.set([Group.objects.get(name='Subscribers')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass
            
        try:
            user.author
            user.groups.set([Group.objects.get(name='Authors')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            user.groups.set([Group.objects.get(name='Publishers')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            user.groups.set([Group.objects.get(name='Administrators')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass

    def create_user_groups(self):
        """
        Create and store the available user groups.
        """
        user_group = None
        for group_name, perm_list in self.user_groups.items():
            user_group = Group.objects.create(name=group_name)
            permission_list = []
            for perm_codename in perm_list:
                permision = Permission.objects.get(codename=perm_codename)
                permission_list.append(permision)
            user_group.permissions.set(permission_list)
            user_group.save()
        for user in User.objects.all():
            self.set_user_permmisions(user)

    def test_user_groups(self):
        """
        Verify if the user groups are available in the database.
        """
        user_group = None
        try:
            for group_name, perm_list in self.user_groups.items():
                user_group = Group.objects.get(name=group_name)
                for perm_codename in perm_list:
                    user_group.permissions.get(codename=perm_codename)
        except ObjectDoesNotExist as e:
            if(len(Group.objects.all()) > 0):
                Group.objects.all().delete()
            self.create_user_groups()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initial user_level
        self.__user_level = self.user_level
        try:
            self.test_user_groups()
        except Error as e:
            print('>Database Error: ', e)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        """
        Delete the app user as well as django user model instances.
        
        calls ``super().delete(*args, **kwargs)``
        """
        super().delete(*args, **kwargs)
        User.objects.get(username=self.user.username).delete()

    def save(self, *args, **kwargs):
        """
        Prevents changing user levels.
        
        calls ``super().save(*args, **kwargs)``
        """
        # reset user_level to original
        if self.id and self.user_level != self.__user_level:
            self.user_level = self.__user_level
        
        # save and return
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class Subscriber(AppUser):
    """
    Inherits the app user.
    Should have a user level 'SUB'
    """    
    FREE = 'FREE'     #: Free subscription type.
    PAID = 'PAID'     #: Paid subscription type.
    
    #: Subscriber subscription types.
    SUBCRIPTIONS = (  
        (FREE, FREE),
        (PAID,PAID),
    )
    
    #: The subscription types.
    subscription_type = models.CharField(
        max_length=4, 
        choices=SUBCRIPTIONS,
        default=FREE,
    )

class Author(AppUser):
    """
    Inherits the app user.
    Should have a user level 'AUT'
    """
    FREE = 'FREE'     #: Free subscription type.
    PAID = 'PAID'     #: Paid subscription type.
    PREMIUM = 'PREMIUM'     #: Premium subscription type.
    
    #: Author subscription types.
    AUTHOR_LEVELS = (  
        (FREE, FREE),
        (PAID,PAID),
        (PREMIUM,PREMIUM)
    )
    
    #: The author types.
    author_type = models.CharField(
        max_length=10, 
        choices=AUTHOR_LEVELS,
        default=FREE,
    )

class Publisher(AppUser):
    """
    Inherits the app user.
    Should have a user level 'PUB'
    """
    pass

class Admin(AppUser):
    """
    Inherits the app user.
    Should have a user level 'ADM'
    """
    class Meta:
        verbose_name = "administrator"

