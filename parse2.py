import re, copy, pdb
from element import Element
from line import Line

class Parser:
	
	def __init__(self,filepath):
		self.line = 0
		self.depth = 0
		self.filepath = filepath
		self.stack = []
		self.toplevel = None
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
		line = Line(line)
		line.expect("tabs")
		line.setEscaped(False)
		for char in line.line:
			if line.isEscaped():
				if not line.expecting("content") and not line.expecting("multiples"):
					line.append(char)
					line.setEscaped(False)
			elif char == "\\":
				line.setEscaped(True)
			else:
				if line.expecting(None):
					line.expect(char)
				if line.expecting("tabs"):
					if char == "\t":
						line.append(char)
					else:
						line.expect("abc")
				if line.expecting("abc"):
					if char.isalpha() or (char.isalnum() and not line.isEmpty()):
						line.append(char)
					else:
						line.expect(char)
				if line.expecting("content"):
					if not line.isEndquote(char):
						line.append(char)
					elif not line.isEmpty():
						line.expect(None)
				if line.expecting("class") or line.expecting("id"):
					if not char.isspace():
						if char.isalpha() or (char.isalnum() and not line.isEmpty()):
							line.append(char)
						else:
							line.expect(char)
					elif not line.isEmpty():
						line.expect(None)
				if line.expecting("attr"):
					if not line.isEndquote('"') and not line.isEndquote("'"):
						if char.isalnum():
							line.append(char)
						elif line.isEndquote("=") and (char == "'" or char == '"'):
							line.openQuote(char)
							line.append(char)
						elif not char == "=" :
							line.expect(char)
					elif line.isEndquote(char) and char != "=":
						line.append(char)
						line.expect(None)
				if line.expecting("multiples"):
					if char.isdigit():
						line.append(char)
					elif not line.isEmpty():
						line.expect(None)
		print line.compile()
		return line.compile()




	def parse(self, block=None):
		lines = open(self.filepath,'r').readlines()
		for line in lines:
			self.line += 1
			parsed = self.parseLine(line)
			if parsed:
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