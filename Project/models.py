from django.db import models

# Create your models here.
class customer(models.Model):
   cid = models.AutoField(primary_key=True)
   name = models.CharField(max_length = 50,null=False)
   email = models.EmailField(max_length = 50,null=False)
   password = models.CharField(max_length = 100,null=False)
   balance = models.FloatField(default='0')
   phonenumber = models.BigIntegerField(null=False)

class shares(models.Model):
	sid = models.AutoField(primary_key=True)
	stock_code = models.CharField(max_length=50,null=False, default='')
	stock_name = models.CharField(max_length = 100,null=False)
	ceo_name = models.CharField(max_length = 100,null=False,default='')
	comp_desc = models.TextField(null=False,default='')

class buy_transaction(models.Model):
	b_tid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(customer)
	quantity = models.IntegerField(null=False)
	sid = models.ForeignKey(shares)
	impact = models.FloatField(null=False)
	buyrate = models.FloatField(null=True)

class sell_transaction(models.Model):
	s_tid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(customer)
	quantity = models.IntegerField(null=False)
	sid = models.ForeignKey(shares)
	impact = models.FloatField(null=False)
	sellrate = models.FloatField(null=True)

class historical_data(models.Model):
	sid = models.ForeignKey(shares)
	open_price = models.FloatField(null=False)
	close_price = models.FloatField(null=False)
	highest_p = models.FloatField(null=False)
	lowest_p =  models.FloatField(null=False)
	date = models.DateField(null=False)

