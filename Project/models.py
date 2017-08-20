from django.db import models

# Create your models here.
class Customer(models.Model):

   cid = models.AutoField(primary_key=True)
   name = models.CharField(max_length = 50,null=False)
   email = models.EmailField(max_length = 50,null=False)
   password = models.CharField(max_length = 50,null=False)
   balance = models.FloatField(default='0')
   phonenumber = models.IntegerField(max_length = 10,null=False)

class shares(models.Model):
	sid = models.AutoField(primary_key=True)
	stock_name = models.CharField(max_length = 50,null=False)
	stock_branch = models.CharField(max_length = 50,null=False)


class Transaction(models.Model):

	t_id = models.AutoField(primary_key=True)
	c_id = models.ForeignKey(Customer)
	quantity = models.IntegerField(null=False)
	s_id = models.ForeignKey(shares)
	impact = models.FloatField(null=False)
	buyrate = models.FloatField(null=True)
	sellrate = models.FloatField(null=True)



class historical_data(models.Model):
	sid = models.ForeignKey(shares)
	open_price = models.FloatField(null=False)
	close_price = models.FloatField(null=False)
	highest_p = models.FloatField(null=False)
	lowest_p =  models.FloatField(null=False)
	date = models.DateField(null=False)

