import re

class Parser:
	
	def __init__(self,filepath):
		self.line = 0
		self.depth = 0
		self.filepath = filepath
		self.stack = []
		self.template = r"""^(?P<tabs>\t*)
							(?P<name>[^\W\d_]*)(?P<s>[^\S\r\n])*
							(?P<classid>(?:[\.|\#][^\W\d]+[^\W]*(?P=s)*)*)(?P=s)*
							(?P<content>\".*?\")*(?P=s)*
							(?:\*(?P=s)*(?P<multiples>\d))$"""

	def lastElement(self):
		return self.stack[-1]

	def addElement(self,element):
		self.stack += [element]

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
		lines = open(self.filepath,'r').readlines()
		for line in lines:
			self.line += 1
			parsed = parseLine(line)
			if parsed is not None:
				self.depth = parsed['depth']
				element = Element(**parsed)
				if self.stack == []:
					self.addElement(element)
				elif self.lastElement().depth < self.depth:
					self.lastElement().addChild(element)
					self.addElement(element)
				elif self.lastElement().depth >= self.depth:
					while self.lastElement().depth >= self.depth:
						self.stack.pop

				# aaaaaaaah