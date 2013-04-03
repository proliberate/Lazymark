class Element:

	def __init__(self):
		self.name = ""
		self.cat = []
		self.iden = []
		self.attr = []
		self.level = 0
		self.content = ""
		self.open = False;

	def __enter__(self):
		return self

	def __exit__(self):
		self.write()

	def setName(self,name):
		self.name = name

	def setClass(self,*cat):
		self.cat += list(cat)

	def setID(self,*iden):
		self.iden += list(iden)

	def setAttribute(self,*attr):
		self.attr += list(attr)

	def setContent(self,content):
		self.contents = contents

	def write(self):
		name = self.name
		cat = "class='{}'".format(" ".join([str(x) for x in self.cat]))
		iden = "id='{}'".format(" ".join([str(x) for x in self.iden]))
		attr = " ".join("{}={}".format(attr[0],attr[1]) for attr in self.attr)
		content = self.content
		closetag = "" if self.open else "</{}>".format(name)
		tag = "<{}>{}{}".format(" ".join(x for x in [name,cat,iden,attr]),content,closetag)
		print tag