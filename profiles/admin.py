from django.contrib import admin
from .models import Profile,CodechefContest,CodeforceContest,Post,Announcements
# Register your models here.
admin.site.register(Profile)
admin.site.register(CodechefContest)
admin.site.register(CodeforceContest)
admin.site.register(Post)
admin.site.register(Announcements)

