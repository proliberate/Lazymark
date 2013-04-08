class Element:

	def __init__(self,name="",cat=[],iden=[],attr=[],children=[],depth=0,content="",closed=True):
		self.name = ""
		self.cat = cat
		self.iden = iden
		self.attr = attr
		self.children = children
		self.depth = depth
		self.content = content
		self.closed = closed

	def write(self):
		name = self.name
		cat = "class='{}'".format(" ".join([str(x) for x in self.cat]))
		iden = "id='{}'".format(" ".join([str(x) for x in self.iden]))
		attr = " ".join("{}={}".format(attr[0],attr[1]) for attr in self.attr)
		depth = "\t" * self.depth
		content = self.content
		closetag = "" if not self.closed else "</{}>".format(name)
		if not self.children:
			print "{}<{}>{}{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content,closetag)
		else:
			print "{}<{}>{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content)
			for child in self.children:
				child.write()
			print "{}{}".format(depth,closetag)

		#tag = "{}<{}>{}{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content,closetag)

	def addChild(self,child):
		self.children += [child]

	def expandAll(self):
		self.expandTag