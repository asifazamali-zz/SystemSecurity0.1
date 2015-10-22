# Create your views here.
from django.http import HttpResponse 	
from pymongo import Connection
from bson import ObjectId
import django_tables2 as tables
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json
from django.core.exceptions import PermissionDenied
from ifc.rwlabel import RWFM,LabelManager

def napublic(request):
	html = "<html><head><title>403.1 Execute access forbidden</title><body><H2>Error 403.1 Execute access forbidden</H2><H3>You are not allowed to make the document public or downgrade readers.</H3></body></html>"
	return HttpResponse(html)
def naprivate(request):
	html = "<html><head><title>403.1 Execute access forbidden</title><body><H2>Error 403.1 Execute access forbidden</H2><H3>You are not allowed to upgrade readers.</H3></body></html>"

	return HttpResponse(html)
def updatedoc(request):
	lm = LabelManager()
	rw = RWFM()
	print "updatedoc"
	is_public = request.POST.get("is_public")
	doc_res =  request.POST.get("doc_res")
	doc_id = (doc_res.split("/api/documents/")[1]).split("/")[0]
	doc_id = str(doc_id)
	temp2 = lm.getLabel(doc_id)
	print  "temp2"
	print temp2
	
	assignees = json.loads(request.POST.get("assignees"))
	print assignees	
	
	sublabel = request.session["rwlabel"]	
	temp3 = {}
	r3 = []
	w3 = temp2["writers"]
	print is_public
	if is_public=="true":
		print  "public"
		readers = User.objects.all()
		for x in readers:
			r3.append(x.id)
		for x in assignees:
			if x["permission"]=="can_edit":
				w3.append(x["id"])
		temp3 = {"owner":temp2["owner"],"readers":r3,"writers":w3,"doc_id":doc_id} 
	else:
		print "private"
		for x in assignees:
			if x["permission"]=="can_view":
				r3.append(x["id"])
			if x["permission"]=="can_edit":
				r3.append(x["id"])
				w3.append(x["id"])
		
		r = []
		readers = User.objects.all()
		for x in readers:
			r.append(x.id)
		if temp2["readers"] == r:
			temp3 = {"owner":temp2["owner"],"readers":list((set(r3).union(set(temp2["owner"])))),"writers":w3,"doc_id":doc_id}
		else:
			temp3 = {"owner":temp2["owner"],"readers":list((set(r3).union(set(temp2["readers"])))),"writers":w3,"doc_id":doc_id}

		

	print "temp3"
	print temp3	
	print temp2["readers"]
	if len(temp2["readers"]) > len(temp3["readers"]):		
		print "upgrade"
		if rw.checkUpgrade(sublabel,temp2,temp3):
			print temp3
			if lm.updatelabel(doc_id,temp3):
				request.session["rwlabel"] = sublabel
				return HttpResponseRedirect("/documents/"+doc_id+"/")
			else:
				print "error" 
		


		else:
			# cant upgrade
			return HttpResponseRedirect("/rwlabel/naprivate/")
	elif len(temp2["readers"]) < len(temp3["readers"]):
		print "downgrade"
		if rw.checkDowngrade(sublabel,temp2,temp3):
			if lm.updatelabel(doc_id,temp3):				
				request.session["rwlabel"] = sublabel				
				return HttpResponseRedirect("/documents/"+doc_id+"/")
			else:
				print "error"


		else:
			# cant downgrade
			raise PermissionDenied
			#return HttpResponseRedirect("/rwlabel/napublic/")
	
	else:
		if lm.updatelabel(doc_id,temp3):
			request.session["rwlabel"] = sublabel
			return HttpResponseRedirect("/documents/"+doc_id+"/")
		else:
			print "error"


def index(request):
# 	databaseName = "dbpatterns"
# 	connection = Connection()
	
# 	db = connection[databaseName]
# 	documents = db['documents']	
# 	rwlabel = db["rwlabel"]
# 	print "searching"
# 	for e in documents.find():		
# 		print e["_id"]
# 		r = []
# 		w = []
# 		print e["is_public"]
# 		if not e["is_public"]:			
# 			for x in e["assignees"]:			
# 				if x["permission"]=="can_view":
# 					r.append(x["id"])
# 				if x["permission"]=="can_edit":
# 					r.append(x["id"])
# 					w.append(x["id"])
# 				print "   "	
# 			temp = { "doc_id" : e["_id"],"owner" :e["user_id"],"readers": r,"writers": w }
# 			if rwlabel.find_one({"doc_id":e["_id"]}):
# 				rwlabel.update({'doc_id':e["_id"]}, {"$set": temp}, upsert=False)
# 			else:
# 				rwlabel.save(temp)
# 			print "saved"
# 		else:
# 			r.append("*")
# 			w.append(e["user_id"])
# 			temp = { "doc_id" : e["_id"],"owner" :e["user_id"],"readers": r,"writers": w }
# 			if rwlabel.find_one({"doc_id":e["_id"]}):
# 				rwlabel.update({'doc_id':e["_id"]}, {"$set": temp}, upsert=False)
# 			else:
# 				rwlabel.save(temp)
# 			print "saved"
	
# 	return 	render(request,'rwlabel/index.html',create_table())


# def create_table():
# 	databaseName = "dbpatterns"
# 	connection = Connection()
# 	db = connection[databaseName]
# 	rwlabel = db["rwlabel"]
# 	data = []

# 	for e in rwlabel.find():
# 		print e["doc_id"]
# 		print e["owner"]
# 		print e["readers"]
# 		print "why"
# 		print e["writers"]
# 		temp = {"Document_ID":e["doc_id"],"Owner":e["owner"],"Readers":e["readers"],"Writers":e["writers"]}
# 		data.append(temp)
	
# 	class NameTable(tables.Table):
# 		Document_ID = tables.Column()
# 		Owner = tables.Column()
# 		Readers = tables.Column()
# 		Writers = tables.Column()
# 	success = "Saving the updated RW Labels in the database... Check MongoDb for the updated values"
# 	table = NameTable(data)	
# 	print "done"
# 	context = {'table': table}

 	return context

def MakeRWLabel(document,session):
	lm = LabelManager()
	rw = RWFM()
	print  "MakeRWLabel"
	# databaseName = "dbpatterns"
	# connection = Connection()
	
	# db = connection[databaseName]
	# rwlabel = db["rwlabel"]
	sublabel = session["rwlabel"]
	r2  = session["rwlabel"]["readers"]
	w = session["rwlabel"]["writers"]
	# just after creation label
	temp2  = rw.createObjLabel(sublabel,document["_id"])
	# temp2 = { "doc_id" : document["_id"],"owner" : session["rwlabel"]["owner"],"readers": r2,"writers": w }
	print temp2
	if document["is_public"]:
		# readers = *
		readers = User.objects.all()
		r3 = []
		for x in readers:
			r3.append(x.id)
		# label is made to public
		temp3 = {"doc_id" : document["_id"],"owner" : session["rwlabel"]["owner"],"readers": r3,"writers": w}
		if rw.checkDowngrade(sublabel,temp2,temp3):
			# rwlabel.save(temp3)
			lm.updatelabel(document["_id"],temp3)
			# connection.disconnect()
			return {"bool": True, "type":"public"}
		else:
			# rwlabel.save(temp2)

			# connection.disconnect()
			return {"bool": False, "type":"public"}
	else:
		# if private make readers same as readers of subject.. then check for assignee.
		#readers  = owner
		#temp3 = {"doc_id" : document["_id"],"owner" : session["rwlabel"]["owner"],"readers": session["rwlabel"]["owner"],"writers": w}
		# rwlabel.save(temp2)
		# connection.disconnect()
		return {"bool":True,"type":"private"}


def MakeForkLabel(document,session):
	# databaseName = "dbpatterns"
	# connection = Connection()
	lm = LabelManager()
	rw = RWFM()
	# db = connection[databaseName]
	# rwlabel = db["rwlabel"]
	sublabel = session["rwlabel"]
	# r2  = session["rwlabel"]["readers"]
	# w = session["rwlabel"]["writers"]
	# just after creation of label
	rw.createObjLabel(sublabel,document["_id"])
	# temp2 = { "doc_id" : document["_id"],"owner" : session["rwlabel"]["owner"],"readers": r2,"writers": w }
	# rwlabel.save(temp2)
	# connection.disconnect()
	return {"bool":True}

# def checkDowngrade(sublabel,temp2,temp3):
# 	if(set(sublabel["owner"]).issubset(set(temp2["readers"]))):
# 		if(sublabel["owner"]==temp2["owner"]==temp3["owner"]):
# 			if(set(sublabel["readers"])==set(temp2["readers"])):
# 				if(set(sublabel["writers"])==set(temp2["writers"])==set(temp3["writers"])):
# 					if(set(temp2["readers"]).issubset(set(temp3["readers"] ))):
# 						if((set(sublabel["writers"])==set(sublabel["owner"])) or (set(set(temp3["readers"]).difference(set(temp2["readers"]))).issubset(set(temp2["writers"])))):
# 							return True
# 						else:
# 							print "6"
# 							return False
# 					else:
# 						print "5"
# 						return False
# 				else:
# 					print "4"
# 					return False
# 			else:
# 				print "3"
# 				return False
# 		else:
# 			print "2"
# 			return False
# 	else:
# 		print "1"
# 		return False

		

# def checkUpgrade(sublabel,temp2,temp3):
# 	if((set(sublabel["owner"]).issubset(set(temp2["readers"]))) and (sublabel["owner"]==temp2["owner"]==temp3["owner"]) and (set(sublabel["readers"]).issubset(set(temp2["readers"] ))) and (set(sublabel["writers"])==set(temp2["writers"])==set(temp3["writers"])) and  (set(temp3["readers"]).issubset(set(sublabel["readers"])))):
# 		return True
# 	else:
# 		return False

# def getLabel(i):
# 	print "getLabel"	
# 	databaseName = "dbpatterns"
# 	connection = Connection()	
# 	db = connection[databaseName]
# 	rwlabel = db["rwlabel"]
# 	i = str(i)
# 	label = rwlabel.find_one({"doc_id":i})
# 	connection.disconnect()
# 	if label:
# 		print label	
# 		return label
# 	else:
# 		return None

# def updatelabel(doc_id,temp3):
# 	print "updatelabel"
# 	databaseName = "dbpatterns"
# 	connection = Connection()	
# 	db = connection[databaseName]
# 	rwlabel = db["rwlabel"]
# 	label = rwlabel.find_one({"doc_id":doc_id})
# 	if label:
# 		rwlabel.update({'doc_id':doc_id}, {"$set": temp3}, upsert=False)
# 		connection.disconnect()
# 		return True
# 	else:
# 		return False

		







