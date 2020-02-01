from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user=models.OneToOneField(User, on_delete = models.CASCADE)
	collegeName = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	codechefId = models.CharField(max_length=50)
	codeforceId = models.CharField(max_length=50)
	hackerrankId = models.CharField(max_length=50)
	codechef ="codechef"
	codeforce ="codeforce"
	both  ="both"
	non   ="non"

	mailChoiceOptions = (
        (codechef, 'Codechef'),
        (codeforce, 'Codeforce'),
        (both, 'Codeforce and Codechef both'),
        (non,'non')
        
    )
	MailChoice= models.CharField(
        max_length=20,
        choices=mailChoiceOptions,
        default=both,
    )
	

	def __str__(self):
		return f'{self.user.username} Profile'

class Post(models.Model):
	title = models.CharField(max_length=1000)
	post_data = models.CharField(max_length=50000)


	def __str__ (self):
		return f'{self.title}' 


class CodechefContest(models.Model):
	title = models.CharField(max_length=50,primary_key=True)
	name = models.CharField(max_length=50)
	start = models.CharField(max_length=50)
	end = models.CharField(max_length=50)

	def __str__ (self):
		return f'{self.title}'



class CodeforceContest(models.Model):
	title = models.CharField(max_length=50,primary_key=True)
	name = models.CharField(max_length=50)
	start = models.CharField(max_length=50)
	end = models.CharField(max_length=50)

	def __str__ (self):
		return f'{self.title}'



class Announcements(models.Model):
	title = models.CharField(max_length=1000)
	post_data = models.CharField(max_length=50000)


	def __str__ (self):
		return f'{self.title}' 