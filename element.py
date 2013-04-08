import copy

class Element:

	def __init__(self,name="",cat=[],iden=[],attr=[],children=[],depth=0,content="",closed=True,multiples=0):
		self.name = name
		self.cat = cat
		self.iden = iden
		self.attr = attr
		self.children = children
		self.depth = depth
		self.content = content
		self.closed = closed
		self.multiples = multiples

	def write(self):
		name = self.name
		cat = "class='{}'".format(" ".join([str(x) for x in self.cat])) if self.cat else ""
		iden = "id='{}'".format(" ".join([str(x) for x in self.iden])) if self.iden else ""
		attr = " ".join("{}={}".format(attr[0],attr[1]) for attr in self.attr) if self.attr else ""
		depth = "\t" * self.depth
		content = self.content
		closetag = "" if not self.closed else "</{}>".format(name)
		if not self.children:
			print "{}<{}>{}{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content,closetag)
		else:
			print "{}<{}>{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content)
			for child in self.children:
				if child.name == "":
					break
				child.write()
			print "{}{}".format(depth,closetag)

		#tag = "{}<{}>{}{}".format(depth," ".join(x for x in [name,cat,iden,attr]),content,closetag)

	def addChild(self,child):
		x = copy.deepcopy(child)
		self.children += [x]