from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files import File
from .models import Document,Request_send,Shared,Friends,Details,PrivacyDetails,PrivacyFriend,PrivacyDocs,Document_mongo
from .forms import SignUpForm,ContactForm,DocumentForm,RequestSendForm,FriendForm,SaveForm,SaveDetailsForm,PrivacyDetailsForm,PrivacyFriendForm,PrivacyDocumentForm
from django.db import connection
from project.settings import MEDIA_ROOT
from django.db.models import Q
#from registration.signals import user_registered
from django.contrib.auth.signals import user_logged_in
#Label Creation
from ifc.rwlabel import RWFM,LabelManager
from rwlabel.views import MakeRWLabel,MakeForkLabel
from datetime import datetime
# Create your views here.
def home(request):
    # if request.user.is_authenticated:
    #     print "in home:user_authenticated"
    #     print request.get_full_path
    cursor=connection.cursor()
    friend_list=Request_send.objects.filter(friend_req=request.user.username).exclude(user_name=request.user.username).filter(document_name='00000')
    shared_list = Request_send.objects.filter(friend_req=request.user.username).exclude(user_name=request.user.username).exclude(document_name='00000')
    test = PrivacyFriend.objects.filter(user_name=request.user.username)
###########################################################################Navigation Bar########################################################
    profile_privacy = PrivacyDetails.objects.filter(user_name=request.user.username)
    n_privacy='0'
    a_privacy = '0'
    l_privacy='0'
    p_privacy='0'
    e_privacy ='0'
    if profile_privacy:
        n_privacy =profile_privacy[0].name
        a_privacy = profile_privacy[0].age
        l_privacy = profile_privacy[0].location
        p_privacy = profile_privacy[0].phnumber
        e_privacy = profile_privacy[0].email


###########################################################################Profile Privacy########################################################
    find_friend=[]
    form1=SaveForm(request.POST or None)
    if request.method=="POST":
        form = DocumentForm(request.POST,request.FILES)
        var=request.POST.get("SearchBox","")
        print var
        if(var):
            sql= User.objects.filter(username=var)
            # sql ='Select distinct user_name from documents where user_name ="%s"' %(var)
            # cursor.execute(sql)
            # q= cursor.fetchall()
            for f in sql:
                find_friend.append(f.username)
            print find_friend
#################################################################################SearchBox##########################################################

        username=request.user.username
        privacy_friend = request.POST.get("privacy_friend","")
        if(test):
            print "updating privacy settings"+str(privacy_friend)
            sql=PrivacyFriend.objects.get(user_name=request.user.username)
            sql.privacy=str(privacy_friend)
            sql.save()
        else:
            form_privacy_friend = PrivacyFriendForm(request.POST or None)
            if form_privacy_friend.is_valid():

                print "form_privacy_friend is valid"
                instance=form_privacy_friend.save(commit=False)
                instance.user_name= request.user.username
                #instance.privacy = privacy_friend
                instance.save()
                 # Redirect to the document list after POST
                return HttpResponseRedirect('/')
            else:
                print "not_valid_friend_privacy_form"
################################################################################FreindPrivacy######################################################
    else:
        form = DocumentForm()
    mydocs = Document.objects.filter(user_name=request.user.username).filter(grantor='00000')
    sql = PrivacyDocs.objects.filter(user_name=request.user.username)
    docs_privacy=''
    i=0
    for m in sql:
        i+=1
        docs_privacy+=(str(m.privacy))
    print 'docs_privacy'+str(docs_privacy)
    #docs_privacy=array('i',docs)
        #####################################################docs Privacy###########################################################
    #print docs_privacy
    shared_docs = Document.objects.filter(user_name=request.user.username).exclude(grantor='00000')
    q   = Friends.objects.filter(user_name=request.user.username)
    r   = Friends.objects.filter(friend_name=request.user.username)
    det=Details.objects.filter(user_name=request.user.username)
    name=''
    age=''
    location=''
    phnumber=''
    email=''
    if(det):
        name=det[0].name
        age=det[0].age
        location=det[0].location
        phnumber=det[0].phnumber
        email=det[0].email

    #print docs_privacy.

    test = PrivacyFriend.objects.filter(user_name=request.user.username)
    for t in test:
        print t.privacy
    return render_to_response(
            'home.html',
            {'request':request,'friends': q,'reversed_friends':r,'mydocs': mydocs,'shared_docs':shared_docs,'find_friend':find_friend,'txt':form1,'form':form,
             'friend_list':friend_list,'name':name,'age':age,
             'location':location,'phnumber':phnumber,'email':email,'shared_list':shared_list,'num_docs':i,
             'n_privacy':n_privacy,'a_privacy':a_privacy,'l_privacy':l_privacy,'p_privacy':p_privacy,'e_privacy':e_privacy,
             'docs_privacy':docs_privacy,
             # 'friend_privacy':test[0].privacy
             },
            context_instance=RequestContext(request)
        )
def login_rwlabel(sender,user,request,**kwargs):
        readers = User.objects.all()
        r = []
        for x in readers:
            r.append(x.id)
        print r
        temp = { "session_id" : request.session.session_key,"owner" :[request.user.id],"readers": r,"writers":[request.user.id]}
        request.session['rwlabel'] = temp
         ##storing labels into session cookie
        print temp



user_logged_in.connect(login_rwlabel)




def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        email= form.cleaned_data.get("email")
        print email
        
    context = {
    "form" : form
    }
        
    return render(request,"contact.html",context)

#def upload_file(request):
    #if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            #return HttpResponseRedirect('project.view.list')
    #else:
        #form = UploadFileForm()
    #return render_to_response('list.html', {'form': form})
def list1(request):
    # Handle file upload
    form1=SaveForm(request.POST or None)
    if request.method == 'POST':
        #print request.FILES['file'].filename
        form = DocumentForm(request.POST,request.FILES)
        print "checking form validation"
        if form1.is_valid():
            message= form1.cleaned_data.get("message")
            print message
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user_name= request.user
            instance.read = True
            instance.write = True
            instance.owner = True
            instance.save()
            sql = Document.objects.latest('id')
            if(sql):
                #print sql.docfile
                file =sql.docfile
            sql=PrivacyDocs(user_name=request.user.username,docfile=file,privacy=0)
            sql.save()
            # Object Label Creation()
            doc_rwlabel(request)

            return HttpResponseRedirect('/')
    else:
        print "in form_valid"
        form = DocumentForm() # A empty, unbound form
    #print "in form_invalid"
    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'document': documents,'form':form,'txt':form1},
        context_instance=RequestContext(request)
    )



def find_friend(request):
    user=request.GET.get('q','')
    #print "inside find_friend"
    form1=SaveForm(request.POST or None)
    if request.method=="POST":
        form = RequestSendForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_name= request.user.username
            instance.friend_req = request.POST.get("frnd_name","")
            instance.save()
            return HttpResponseRedirect('/')
    else:
        form = DocumentForm()

    mydocs = Document.objects.filter(user_name=user).filter(grantor='00000')
    docs=list(mydocs)
    for d in docs:
        logged_user=request.user.username
        #print d.docfile.url[7:]
        if logged_user not in show_privacy(PrivacyDocs,user,request,'privacy',d.docfile.url[7:],1):
            docs.remove(d)
    # for d in docs:
    #     print d.docfile.url[7:]
    shared_docs = Document.objects.filter(user_name=user).exclude(grantor='00000')
    q=''
    r=''
    logged_user=request.user.username
    if (logged_user in show_privacy(PrivacyFriend,user,request,'privacy','null',0)):
        q= Friends.objects.filter(user_name=user)
        r= Friends.objects.filter(friend_name=user)
    details=[]
    det=Details.objects.filter(user_name=user)
    name=''
    age=''
    location=''
    phnumber=''
    email=''
    #print show_privacy(PrivacyDetails,user,request,1)
    #print show_privacy("profile_privacy",user,request,4)
    if(det):
        logged_user=request.user.username
        #print "hello"+show_privacy(PrivacyDetails,user,request,1)
        if(logged_user in show_privacy(PrivacyDetails,user,request,'name','null',0)):
            #print "inside privacy_"
            name=det[0].name
        if(logged_user in show_privacy(PrivacyDetails,user,request,'age','null',0)):
            # print show_privacy(PrivacyDetails,user,request,2)
            age=det[0].age
        if(logged_user in show_privacy(PrivacyDetails,user,request,'location','null',0)):
            location=det[0].location
        if(logged_user in show_privacy(PrivacyDetails,user,request,'phnumber','null',0)):
            phnumber=det[0].phnumber
        if(logged_user in show_privacy(PrivacyDetails,user,request,'email','null',0)):
            email=det[0].email

    # print q.

    return render_to_response(
            'home.html',
            {'request':request,'friends': q,'reversed_friends':r,'mydocs': docs,'shared_docs':shared_docs,'find_friend':find_friend,'txt':form1,'form':form,'name':name,'age':age,
             'location':location,'phnumber':phnumber,'email':email,'user':user},
            context_instance=RequestContext(request)
        )



########################################################################################################################################################
def show_privacy(Privacytable,user,request,privacy_col_name,docfile_path,change):
        cursor = connection.cursor()
        if change:
            sql=Privacytable.objects.filter(user_name=user).filter(docfile=docfile_path)
            #sql = "select * from "+str(Privacytable)+" where user_name='"+user+"' and docfile='"+docfile_path+"'"
           # print sql
        else:
            sql=Privacytable.objects.filter(user_name=user)
            #sql = "select * from "+str(Privacytable)+" where user_name='"+user+"'"
        #print sql
        #privacy_row=cursor.execute(sql)
        if(not sql):
            return []
        fr = Friends.objects.filter(user_name=user)
        rfr = Friends.objects.filter(friend_name=user)
        friends =[]
        for f in fr:
            friends.append(f.friend_name)
        for rf in rfr:
            friends.append(rf.user_name)
        friend_list=[]
        friendsoffriends=[str(request.user.username)]
        for friend in friends:
            #print friend
            friend_list.append(str(friend))
            f2f =Friends.objects.filter(user_name=friend)
            f2fr =Friends.objects.filter(friend_name=friend)
            if(friend not in friendsoffriends):
                friendsoffriends.append(str(friend))
            for f in f2f:
                if(f.friend_name not in friendsoffriends):
                    friendsoffriends.append(str(f.friend_name))
            for f in f2fr:
                if(f.user_name not in friendsoffriends):
                    friendsoffriends.append(str(f.user_name))
        # for frnd in f2f:
        #     print "f2f" + frnd.friend_name
        # for frnd in friendsoffriends:
        #     print "friendsofrieds"+frnd
        #print list[0][1]
        # print friend_list
        # print friendsoffriends
        # print privacy_col_name
        # print "list[0][privacy_col_name] "+list[0][2]
        # print list[0][2]
        #return sql
        #print eval
        print getattr(sql[0],privacy_col_name)
        if str(getattr(sql[0],privacy_col_name)) =='1':
            return friend_list
        if str(getattr(sql[0],privacy_col_name)) =='2':
            return friendsoffriends
        if str(getattr(sql[0],privacy_col_name)) =='3':
            return [str(request.user.username)]
        else:
            return []

###################################################################################################################################################################################
def registration_complete(request):
    return render(request,'registration/registration_complete.html',{})
def friend(request):
    form = FriendForm(request.POST or None)
    q= Friends.objects.filter(user_name=request.user.username)
    return render_to_response(
        'friend.html',
        {'friends': q},
        context_instance=RequestContext(request)
    )    
    

def notification(request):
    if request.method == 'POST':
        form= FriendForm(request.POST)
        print "checking form validation"
        if form.is_valid():
            instance=form.save(commit=False)
            print "in form_valid(notification)"
            instance.user_name= request.user.username
            instance.friend_name = request.POST.get("frnd_name","")        
            print 'instance.frnd_req '+instance.friend_name
            instance.save() 
            e=Request_send.objects.filter(user_name=instance.friend_name,friend_req=request.user.username)
            e.delete();
            return HttpResponseRedirect('/')
        else:
            print "invalid_form"    
    sql ='Select * from request_send where friend_req= "%s" and user_name !="%s"' %(request.user.username,request.user.username)
    print sql
    all_users= Request_send.objects.raw(sql)
        #all_users=all_users.exclude(username=request.user)
    return render_to_response(
            'notification.html',
            {'users': all_users},
            context_instance=RequestContext(request)
        )

def readnotification(request):
    print "inside readnotification"
    if request.method=='POST':
        e = Request_send.objects.filter(user_name=request.POST.get("usr_name",""),friend_req=request.user.username,document_name=request.POST.get("doc_name",""))
        e.delete();
        return HttpResponseRedirect('/')


def shared(request):
    if request.method == 'POST':
        form= DocumentForm(request.POST or None)
        form_notification= RequestSendForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            print "in form_valid_docform"
            instance.user_name= request.POST.get("friend_select","")
            instance.docfile = request.POST.get("docfile","")
            instance.friend_name = request.POST.get("frnd_name","")
            instance.write = ((request.POST.get("write_select","")) in ("True","1"))
            #print "instance.write: "+ instance.write
            instance.grantor = request.user.username
            #print 'instance.frnd_req '+instance.friend_name
            instance.save()
        if form_notification.is_valid():
            print "form valid: notification"
            instance = form_notification.save(commit=False)
            instance.user_name  = request.user.username
            instance.document_name = request.POST.get("docfile","")
            instance.friend_req = request.POST.get("friend_select","")
            instance.save()
        else:
            print " notification invalid_form"

    #print "in form_invalid"
    # Load documents for the list page
    sql = "Select * from security_friends where user_name='%s'"%(request.user.username)
    #print sql
    friend = Friends.objects.raw(sql)
    sql = "Select * from documents where user_name='%s'"%(request.user.username)
    #print sql    
    shared = Document.objects.raw(sql)
    
        # Render list page with the documents and the form
    return render_to_response(
            'shared.html',
            {'shared': shared,'friends':friend,},
            context_instance=RequestContext(request)
        )    

def update_privacy(request):
    docs_privacyform = PrivacyDocumentForm(request.POST or None)
    print "checking form validation"
    if docs_privacyform.is_valid():
            print "docs_privacy form valid"
            privacy=PrivacyDocs.objects.filter(user_name=request.user.username)
            for p in privacy:
                form_param=request.POST.get(""+p.docfile.url,"")
                print "form_param"+form_param
                if p.privacy != form_param:
                    print "inside docs_privacy if"
                    filter_name = p.docfile.url[7:]
                    print filter_name
                    privacy.filter(docfile=filter_name).update(privacy=form_param)

    else:
        print "docs_privacy form invalid"
    return HttpResponseRedirect('/')
def save(request):
    form1 = SaveForm(request.POST or None)
    print "inside save form"
    if form1.is_valid():
        file_text= form1.cleaned_data.get("message")
        file_name = form1.cleaned_data.get("filePath")
        with open(MEDIA_ROOT+'/'+file_name,'w') as f:
            myfile= File(f)
            myfile.write(file_text)
        
        
        print file_text,file_name
        
    # context = {
    # "txt" : form1
    # }
    #
    return HttpResponseRedirect('/')


def demo(request):
    var=request.POST.get("SearchBox","")
    friend=''
    print var
    if(var):
        sql ='Select * from documents where user_name ="%s"' %(var)
        print sql
        friend= Document.objects.raw(sql)     
        
        
    return render_to_response(
        'demo.html',
        {'find_friend':friend},
        context_instance=RequestContext(request)
    )
def update_or_create(Model,username,defaults):
    data=Model.objects.filter(user_name=username)
    if(data):
        data=Model.objects.get(user_name=username)
        data.name=defaults['name']
        data.age=defaults['age']
        data.phnumber=defaults['phnumber']
        data.email=defaults['email']
        data.save()
        return 0
    data = Details(user_name=username,name=defaults['name'],age=defaults['age'],phnumber=defaults['phnumber'],email=defaults['email'])
    data.save()
    return 1
        


def save_details(request):
    if request.method=="POST":
        form= SaveDetailsForm(request.POST or None)
        form1 = PrivacyDetailsForm(request.POST or None)
        print "checking form validation"
        username= request.user.username
        name= request.POST.get("name","")
        age= request.POST.get("age","")
        location = request.POST.get("location","")
        phnumber = request.POST.get("phnumber","")
        email = request.POST.get("email","")
        #inserted= request.POST.get("inserted","")
        n= request.POST.get("privacy_name","")
        a= request.POST.get("privacy_age","")
        l = request.POST.get("privacy_location","")
        p = request.POST.get("privacy_phnumber","")
        e = request.POST.get("privacy_email","")
        if form.is_valid():
            default_dict={'name':name,'age':age,'location':location,'phnumber':phnumber,'email':email}
            created = update_or_create(Details,request.user.username,default_dict)
            # if created:
            #     print "created"
            # if(inserted=="0"):
            #     instance=form.save(commit=False)
            #     print "in form_valid"
            #     instance.user_name=username
            #     instance.name= name
            #     print request.POST.get("name","default_value")
            #     instance.age = age
            #     instance.location= location
            #     instance.phnumber = phnumber
            #     instance.email = email
            #     instance.save()
            # else:
            #     cursor=connection.cursor()
            #     print name+" "+age+" "+location+" "+phnumber+" "+email+" "
            #     sql="update profile_details set name= '"+name+"',age='"+age+"' ,location='"+location+"' ,phnumber= '"+phnumber+"' ,email='"+email+"' where user_name='"+username+"'"
            #     print sql
            #     cursor.execute(sql)
        if form1.is_valid():
                pick = PrivacyDetails.objects.filter(user_name=request.user.username)
                print pick
                print n+" "+a+" "+l+" "+p+" "+e+" "
                if (pick):
                    cursor=connection.cursor()

                    sql="update profile_privacy set name= '"+n+"',age='"+a+"' ,location='"+l+"' ,phnumber= '"+p+"' ,email='"+e+"' where user_name='"+username+"'"
                    print sql
                    cursor.execute(sql)
                else:
                    instance=form1.save(commit=False)
                    print "in form_valid"
                    instance.user_name=username
                    instance.name= n
                #print request.POST.get("name","default_value")
                    instance.age = a
                    instance.location= l
                    instance.phnumber = p
                    instance.email = e
                    instance.save()
        return HttpResponseRedirect('/')
    return render_to_response(
    'home.html',
    {},context_instance=RequestContext(request))


# def user_registered_handler(sender,**kwargs):
#     print kwargs['user']
#     #print kwargs['sender']
#
#
# user_registered.connect(user_registered_handler)

######################################################Registration Redux ###################################################
def registration_complete(request):
    return render(request,'registration/registration_complete.html',{})

######################################################Registration Redux ###################################################
#####################################################Object Label Creation########################################
def doc_rwlabel(self):
    self.object_id = Document_mongo.objects.create(
            title= "title",
            user_id= self.user.username,
            #date_created= datetime.now(),
            entities= "entities",
            is_public=False,
        )
    temp = {"_id":str(self.object_id),"is_public":False}
    result = MakeRWLabel(temp,self.session)
    print 'label created'+str(result['bool'])
    return
###
