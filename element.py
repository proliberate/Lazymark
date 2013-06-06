import copy

class Element:

	def __init__(self,name="",cat=[],iden=[],attr=[],children=[],depth=0,content="",closed=True,multiples=0):
		self.name = name or "div"
		self.cat = cat
		self.iden = iden
		self.attr = attr
		self.children = children
		self.depth = depth
		self.content = content
		self.closed = closed
		self.multiples = multiples
		self.method = None

	def write(self):
		name = self.name
		cat = "class='{}'".format(" ".join(self.cat.split(".")[1:])) if self.cat else ""
		iden = "id='{}'".format(" ".join(self.iden.split("#")[1:])) if self.iden else ""
		attr = " ".join("{}={}".format(attr[0],attr[1]) for attr in self.attr.iteritems()) if self.attr else ""
		depth = "\t" * self.depth
		content = self.content
		closetag = "" if not self.closed else "</{}>".format(name)
		singleton = "" if self.closed else "/"
		x = [x for x in [name,cat,iden,attr,singleton] if x]
		if not self.children:
			for i in range(self.multiples):
				for content in self.content:
					print "{}<{}>{}{}".format(depth," ".join(x),content,closetag)
		else:
			if self.name == "title": print self.children
			for i in range(self.multiples):
				for content in self.content:
					print "{}<{}>{}".format(depth," ".join(x),content)
					for child in self.children:
						if child.name == "":
							break
						child.write()
					print "{}{}".format(depth,closetag)

		#tag = "{}<{}>{}{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content,closetag)

	def addChild(self,child):
		self.children.append(child)

	def addMethod(self,method):
		self.method.append(method)