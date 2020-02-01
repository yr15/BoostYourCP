from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm,CreatePostForm
from django.contrib.auth.decorators import login_required
from .models import CodechefContest,Profile,CodeforceContest,Post,Announcements
import datetime
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC

import requests,json
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
import datetime

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
#from urllib import urlopen
# Create your views here.



def home(request):
    return render(request,'profiles/home.html')


def contests(request):
    con = CodeforceContest.objects.all()
    cdate = con[:].start

    return render(request,'profiles/contest.html',{'codechef':CodechefContest.objects.all(),
                                                    'codeforces':CodeforceContest.objects.all()})




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
        	form.save()
        	username = form.cleaned_data.get('username')
        	messages.success(request, f'Account created for {username}! ')
        	return redirect('user_profile')
    else:
    	form = UserRegisterForm()

    return render(request,'profiles/register.html',{'form': form} )




@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated successfully! ')
            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request,'profiles/user_profile.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully posted ! ')
            return redirect('user_profile')
        else :
            return redirect('logout')
    else:
        form = CreatePostForm(instance=request.user)

    return render(request,'profiles/user_post.html',{'form': form,'posts':Post.objects.all()})

@login_required
def announcements(request):
    return render(request,'profiles/Announcements.html',{'Announcements':Announcements.objects.all()})

def codechef(request):
    #columns=contents
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    urle = 'https://codechef.com/contests'

    content = session.get(urle, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    containers=soup.findAll("tr")
    containers=containers[0:20]

    now = datetime.datetime.now()

    y=int(now.strftime("%Y"))
    m=int(now.strftime("%m"))
    d=int(now.strftime("%d"))
    print(y,m,d)
    Dict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    for container in containers: 
        new_contest=codechefContest()
        name=container.findAll("td")
        if(len(name)>3):
            l=name[2].text.strip()
            lis=l[0:11].split()
            if    len(lis)!=3 or  Dict.get(lis[1] ,0)==0:
                continue
            lis_m=int(Dict[lis[1]])
            lis_d=int(lis[0])
            lis_y=int(lis[2])
            if(lis_y>=y ):
                if(lis_y>y):
                    #print(str(name[0].text.strip()),str(name[1].text.strip()))
                    new_contest.title=str(name[0].text.strip())
                    new_contest.name=str(name[1].text.strip())
                    new_contest.start=str(name[2].text.strip())
                    new_contest.end=str(name[3].text.strip())
                    new_contest.save()
                else:
                    if(lis_m>=m):
                        if(lis_m>m):
                            #print(str(name[0].text.strip()),str(name[1].text.strip()))
                            new_contest.title=str(name[0].text.strip())
                            new_contest.name=str(name[1].text.strip())
                            new_contest.start=str(name[2].text.strip())
                            new_contest.end=str(name[3].text.strip())
                            new_contest.save()
                        else:
                            if(lis_d>=d):
                                #print(str(name[0].text.strip()),str(name[1].text.strip()))
                                new_contest.title=str(name[0].text.strip())
                                new_contest.name=str(name[1].text.strip())
                                new_contest.start=str(name[2].text.strip())
                                new_contest.end=str(name[3].text.strip())
                                new_contest.save()
    return redirect('register') 



def codeforce(request):
    r=requests.get(url='https://codeforces.com/api/contest.list?gym=false')
    data=r.json()
    data=data['result']
    for x in data:
        if x['phase']=='BEFORE':
            c=codeforceContest()
            c.title=x['id']
            c.name=x['name']
            c.start=x['startTimeSeconds']
            c.end=x['durationSeconds']+x['startTimeSeconds']
            c.save()
    return redirect('register')

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    subject='check mail'
    message='checking mailing'
    from_email='yash028raghuwanshi@gmail.com'
    
    c=CodechefContest.objects.all()
    for contest in c:
        datetime_object = datetime.datetime.strptime(contest.start, '%d %b %Y %X')
        con_date = datetime_object.timestamp()
        datetime2_object = datetime.datetime.strptime(contest.end, '%d %b %Y %X')
        end_date = datetime_object.timestamp()
        cur_date = datetime.datetime.now().strftime("%s")
        if(int(con_date) - int(cur_date)<86400):

            cal = Calendar()
            cal.add('prodid', '-//My calendar product//mxm.dk//')
            cal.add('version', '2.0')

            event = Event()
            event.add('summary', 'codechef: '+ contest.name)
            event.add('dtstart', datetime_object)
            event.add('dtend',datetime2_object )
            event['uid'] = '20050115T101010/27346262376@mxm.dk'
            event.add('priority', 5)

            cal.add_component(event)
            myfile = contest.title+ '.ics'

            f = open(myfile, 'wb')
            f.write(cal.to_ical())
            f.close()
            p = Profile.objects.all()
            for Prof in p:
                if(Prof.MailChoice=="codechef" or Prof.MailChoice=="both"):
                    subject = "Codechef contest "+ contest.name 
                    message = ""
                    msg=EmailMessage(subject, message, from_email, [Prof.user.email])
                    msg.attach_file(myfile)
                    msg.send()

    
    c=CodeforceContest.objects.all()
    for contest in c:
        con_date = contest.start
        start = datetime.datetime.fromtimestamp(int(con_date))
        end = datetime.datetime.fromtimestamp(int(contest.end))
        cur_date = datetime.datetime.now().strftime("%s")
        if(int(con_date) - int(cur_date)<86400):

            cal = Calendar()
            cal.add('prodid', '-//My calendar product//mxm.dk//')
            cal.add('version', '2.0')

            event = Event()
            event.add('summary', 'Codeforces: '+ contest.name)
            event.add('dtstart', start)
            event.add('dtend',end)
            event['uid'] = '20050115T101010/27346262376@mxm.dk'
            event.add('priority', 5)

            cal.add_component(event)
            myfile = contest.title+ '.ics'

            f = open(myfile, 'wb')
            f.write(cal.to_ical())
            f.close()

            p = Profile.objects.all()
            for Prof in p:
                if(Prof.MailChoice=="Codeforces" or Prof.MailChoice=="both"):
                    subject = "Codeforces contest "+ contest.name 
                    message = ""
                    msg=EmailMessage(subject, message, from_email, [Prof.user.email])
                    msg.attach_file(myfile)
                    msg.send()

    return redirect('user_profile')




                