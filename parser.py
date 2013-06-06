import re, copy
from element import Element

class Parser:
	
	def __init__(self,filepath):
		self.line = 0
		self.depth = 0
		self.filepath = filepath
		self.stack = []
		self.toplevel = None
		classid = r"(?P<classid>(?:[\.|\#][^\W\d]+[^\W]*(?P=s)*)*)(?P=s)*"
		attr = r"(?P<attr>(?:[^\W\d]+[^\W]*=(?P<qu>[\"|'])?\w+(?P=qu)?(?P=s)*)*)(?P=s)*"
		content = r"(?:[\"|'](?P<content>.*?)[\"|'])*(?P=s)*"
		self.template = r"""^(?P<tabs>\t*)
			(?:	
				(?:
					(?:def)[^\S\r\n]*(?P<def>[^\W\d]+[^\W]*):(?P<defwrite>:)?[^\S\r\n]*
				)?
				(?:
					(?P<name>[^\W\d_]*)(?P<s>[^\S\r\n])*
					(?P<stuff>[^\*]*)
					(?:\*(?P=s)*(?P<multiples>\d))?
				)	
			)""".format(classid=classid,attr=attr,content=content)
		self.noclose = ["area","base","br","col","command","embed","hr","img","input","link","meta","param","source"]
		self.parse()

	def lastElement(self):
		return self.stack[-1]

	def addElement(self,element,first=False):
		if first is True:
			self.toplevel=element
		else:
			self.lastElement().addChild(element)
		self.stack += [element]

	def parseLine(self,line):
		parsed = re.match(self.template,line,re.X)
		if parsed is None:
			return parsed #if there is no match, return None
		params = {}
		stuff = self.parseStuff(parsed.group('stuff'))
		params["name"] = parsed.group('name') or None
		params["attr"] = re.findall(r"([^\W\d]+[^\W]*)=((?:'.+?')|(?:\".+?\")|\w+)",stuff[0])
		stuff[0] = re.sub(r"([^\W\d]+[^\W]*)=((?:'.+?')|(?:\".+?\")|\w+)","",stuff[0])
		params["cat"] = re.findall(r"[\.]([^\W\d_]+[\w])",stuff[0]) or None
		params["iden"] = re.findall(r"[\#]([^\W\d_]+[\w])",stuff[0]) or None
		params["content"] = stuff[1] or [""]
		params["multiples"] = int(parsed.group('multiples') or 1)
		params["depth"] = len(parsed.group('tabs')) or 0
		params["children"] = []
		if params["name"] == "js":
			params["name"] = "script"
			params["attr"] += [("type","'text/javascript'")]
			params["attr"] += [("src","'"+''.join(params["content"]),"'")]
			params["content"] = [""]
		if params["name"] == "css":
			params["name"] = "link"
			params["attr"] += [("rel","'stylesheet'")]
			params["attr"] += [("type","'text/css'")]
			params["attr"] += [("href","'"+''.join(params["content"]),"'")]
			params["content"] = [""]
		if parsed.group('def'):
			params["defname"] = parsed.group('def')
			params["defwrite"] = True if parsed.group('defwrite') else False
		params["closed"] = params["name"] not in self.noclose
		return params

	#parseStuff separates content from classes, ids, and attrs.
	#we do this so these can be written in any order
	#but all content must be preceeded by one or more spaces
	def parseStuff(self,stuff):
		pattern = [r"(?:^|\s)\"(.*?)\"",r"(?:^|\s)'(.*?)'"]
		content = re.findall(pattern[0],stuff)
		stuff = re.sub(pattern[0],'',stuff)
		content += re.findall(pattern[1],stuff)
		stuff = re.sub(pattern[1],'',stuff)
		return [stuff,content]

	def parse(self, block=None):
		lines = open(self.filepath,'r').readlines()
		for line in lines:
			self.line += 1
			parsed = self.parseLine(line)
			#Only add a new element if it has a name
			if [parsed[x] is not None for x in ['name','cat','iden','attr','content']]:
				self.depth = parsed['depth']
				element = Element(**parsed)
				if self.stack == []:
					self.addElement(element,True)
				elif self.lastElement().depth < self.depth:
					self.addElement(element)
				elif self.lastElement().depth > self.depth:
					while self.lastElement().depth >= self.depth:
						self.stack.pop()
					self.addElement(element)
				elif self.lastElement().depth == self.depth:
					self.stack.pop()
					self.addElement(element)
		
		self.toplevel.write()

Parser("lazytest.txt")