import re

class Parser:
	
	def __init__(self,filepath):
		self.line = 0
		self.depth = 0
		self.filepath = filepath
		self.stack = []
		self.toplevel = None
		self.template = r"""^(?P<tabs>\t*)
							(?P<name>[^\W\d_]*)(?P<s>[^\S\r\n])*
							(?P<classid>(?:[\.|\#][^\W\d]+[^\W]*(?P=s)*)*)(?P=s)*
							(?P<content>\".*?\")*(?P=s)*
							(?:\*(?P=s)*(?P<multiples>\d))$"""

		self.parse()

	def lastElement(self):
		return self.stack[-1]

	def addElement(self,element,first=False):
		self.stack += [element]
		if first is True:
			self.toplevel=element

	def parseLine(self,line):
		parsed = re.match(self.template,line,re.X)
		if parsed is None:
			return parsed #if there is no match, return None
		name = parsed.group('name') or None
		cat = re.findall(r"([\.][^\W\d_]+[\w])",parsed.group('classid')) or None
		iden = re.findall(r"([\#][^\W\d_]+[\w])"),parsed.group('classid') or None
		content = parsed.group('content') or None
		multiples = parsed.group('multiples') or None
		depth = len(parsed.group('tabs')) or None
		return {"name":name,"cat":cat,"iden":iden,"content":content,"multiples":multiples,"depth":depth}

	def parse(self, block=None):
		#lines = open(self.filepath,'r').readlines()
		lines = ["html","	body"]
		for line in lines:
			self.line += 1
			parsed = self.parseLine(line)
			print line
			print parsed
			# if parsed['name'] is not None:
			# 	self.depth = parsed['depth']
			# 	element = Element(**parsed)
			# 	if self.stack == []:
			# 		self.addElement(element,True)
			# 	elif self.lastElement().depth < self.depth:
			# 		self.lastElement().addChild(element)
			# 		self.addElement(element)
			# 	elif self.lastElement().depth >= self.depth:
			# 		while self.lastElement().depth >= self.depth:
			# 			self.stack.pop()
		#
		#self.toplevel.write()

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

blue = Parser("lazytest.txt")