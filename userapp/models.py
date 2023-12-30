import uuid
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _

# from product.models import RefferalLink

# Create your models here.

UPGRADATION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]


class UserManager(BaseUserManager):
    use_in_migration = True
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(email, password, **extra_fields)
    

class UserData(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self): 
        return self.name+","+str(self.id)


    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    #     related_name='user_data_groups',  # <-- Change this line
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     related_name='user_data_user_permissions',  # <-- Change this line
    # )

class RegionDataVillage(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sub_district = models.CharField(max_length=100)
    local_body = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.state} - {self.district} - {self.sub_district} - {self.local_body} - {self.village}"

    class Meta:
        verbose_name_plural = "Region Data"



class UserDetails(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='user_details')
    phone = models.CharField(max_length =15, null = True, blank = True)
    house_number=models.CharField(max_length=50,null = True, blank = True)
    land_mark = models.CharField(max_length=500,null = True, blank = True)
    # region_data = models.ForeignKey(RegionDataVillage, on_delete = models.CASCADE, null= True)
    state = models.CharField(max_length =500, null = True, blank = True)
    district =models.CharField(max_length =500, null = True, blank = True)
    sub_district =models.CharField(max_length =500, null = True, blank = True)
    local_body=models.CharField(max_length =500, null = True, blank = True)
    village =models.CharField(max_length =500, null = True, blank = True)
    profile_image = models.ImageField(null=True, blank = True)
    
    def __str__(self): 
        return self.user.name+","+str(self.user.id)

#To pay the commission amount 
class UserBankAccountDetails(models.Model):
    user = models.ForeignKey('product.RefferalLink', on_delete = models.CASCADE, null = True)
    account_holder_name = models.CharField(max_length =500, null = True, blank = True)
    account_number = models.CharField(max_length =500, null = True, blank = True)
    bank_name = models.CharField(max_length =500, null = True, blank = True)
    ifsc_code = models.CharField(max_length =500, null = True, blank = True)
    pan_number = models.CharField(max_length = 500, blank =True)
    branch_name = models.CharField(max_length = 500, blank =True)
    check_or_passbook_photo = models.ImageField(null=True, blank = True)
    pancard_photo = models.ImageField(null=True, blank = True)
    # current_primary_account = models.BooleanField()


class UserRequestingforUpgradingToOrganiser(models.Model):
    user = models.ForeignKey(UserData, on_delete = models.CASCADE)
    user_refferal_link = models.ForeignKey('product.RefferalLink', on_delete = models.CASCADE, default ='0')
    request_status = models.CharField(max_length= 50, choices=UPGRADATION_STATUS_CHOICES, default='Pending')
    description = models.CharField(max_length =700, null = True, blank = True)
    is_verified = models.BooleanField(default = False)#to outlist it from the admin dash from  a request
    approved_or_reject_by= models.ForeignKey(UserData,on_delete = models.CASCADE,related_name = 'upgradation_approved_by', null = True)

    def __str__(self): 
        return self.user.name+","+str(self.id)



class SupportingExcelData(models.Model):
    xlsx_file = models.FileField(upload_to='xlsx_files/')
    def __str__(self):
        return f"{str(self.id)}"
