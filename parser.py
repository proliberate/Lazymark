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
					{classid}
					{attr}
					{content}
					(?:\*(?P=s)*(?P<multiples>\d))?
				)	
			)""".format(classid=classid,attr=attr,content=content)

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
		params = {}
		params["name"] = parsed.group('name') or None
		params["cat"] = re.findall(r"[\.]([^\W\d_]+[\w])",parsed.group('classid')) or None
		params["iden"] = re.findall(r"[\#]([^\W\d_]+[\w])",parsed.group('classid')) or None
		params["attr"] = re.findall(r"([^\W\d]+[^\W]*)=((?P<qu>[\"|'])?\w+(?P=qu)?)",parsed.group('attr'))
		params["content"] = parsed.group('content') or ""
		params["multiples"] = int(parsed.group('multiples') or 1)
		params["depth"] = len(parsed.group('tabs')) or 0
		params["children"] = []
		return params

	def parse(self, block=None):
		lines = open(self.filepath,'r').readlines()
		for line in lines:
			self.line += 1
			parsed = self.parseLine(line)
			#print parsed
			if parsed['name'] is not None:
				self.depth = parsed['depth']
				element = Element(**parsed)
				if self.stack == []:
					self.addElement(element,True)
				elif self.lastElement().depth < self.depth:
					assert(self.lastElement().children is not element.children)
					self.lastElement().addChild(element)
					self.addElement(element)
				elif self.lastElement().depth > self.depth:
					while self.lastElement().depth > self.depth:
						self.stack.pop()
				elif self.lastElement().depth == self.depth:
					self.stack.pop()
					self.lastElement().addChild(element)
					self.addElement(element)
		
		self.toplevel.write()

import sys
blue = Parser("lazytest.txt")