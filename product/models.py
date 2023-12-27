from django.db import models
import uuid

from userapp.models import UserData, UserDetails

LINK_HOLEDR_ROLE_CHOICE = {
    ('influencer' ,'influencer'),
    ('organiser' ,'organiser'),
    ('admin', 'admin')
}

class Product(models.Model):
    name = models.CharField(max_length =250)
    description = models.TextField(blank=True, null=True)
    subcription_fee = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    created_by = models.ForeignKey(UserData, on_delete = models.CASCADE,default = '1')
    unique_id = models.CharField(max_length = 15,null = True, blank= True, unique= True)
    product_link = models.URLField(blank=True, null=True)  # Use URLField for storing links
    inclusive_GST = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    influencer_commission_percentage = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    organiser_commission_percentage = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    full_fillment_link = models.URLField(null = True)
    clicks = models.IntegerField(default=0)


class RegionData(models.Model):
    user = models.ForeignKey(UserData, on_delete= models.CASCADE)


class RefferalLink(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserData, on_delete = models.CASCADE, related_name = 'link_generator')# the link generator ie the perosn got is registering
    direct_referred_link_owner = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='direct_referred_links', null=True)#ie influner
    indirect_referred_link_owner = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='indirect_referred_links', null=True)#ie organiser
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    link_holder_role_at_link_generation = models.CharField(max_length=50, choices=LINK_HOLEDR_ROLE_CHOICE, default='admin')
    link_holder_current_role =models.CharField(max_length=50, choices=LINK_HOLEDR_ROLE_CHOICE, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    user_refferal_link = models.URLField(null = True)#The refferal linkgenerated  once the user got regitered
    user_details =  models.ForeignKey(UserDetails, on_delete = models.CASCADE, related_name = 'user_details_parameters', null= True)
    # commission_amount= models.DecimalField(max_digits=25, decimal_places=2, default=0)
 

class UserCommissions(models.Model):
    user = models.ForeignKey(RefferalLink, on_delete = models.CASCADE) #the user who got commission
    commission_amount= models.DecimalField(max_digits=25, decimal_places=2, default=0)
    paid_user = models.ForeignKey(RefferalLink, on_delete = models.CASCADE, related_name = 'paid_user') #the user who subcribe the product that time
    product = models.ForeignKey(Product , on_delete = models.CASCADE) #the product subcribed at the time
    commissioned_user_role = models.CharField(max_length = 200 , null= True, blank = True)#The role of the user at time he got commission 
    paid_user_role = models.CharField(max_length = 200 , null= True, blank = True)#The role of the user at the time they suscribed the product 
    commission_credited_on = models.DateField(auto_now_add=True,)

class PaymentRquest(models.Model):
    user_link = models.ForeignKey(RefferalLink, on_delete = models.CASCADE, null = True)
    pay_request_order_id = models.CharField(max_length = 200 , null= True, blank = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    total_amount = models.IntegerField(default=0)

#After the sucessfull payment completion
class UserPaymentDetailsOfProduct(models.Model):
    user_link = models.ForeignKey(RefferalLink, on_delete = models.CASCADE,default = '1')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    payment_status = models.BooleanField(default = False)
    payment_done_at = models.DateField(auto_now_add= True, null = True)
    payment_total_amount_paid = models.IntegerField(default=0)
    payment_status_of_gateway = models.CharField(max_length=25 ,default= 'failed')
    payment_order_id = models.CharField(max_length=100,default= '0')
    payment_signature =models.CharField(max_length=100,default= '0')
    payment_id = models.CharField(max_length = 200 , null= True, blank = True)



