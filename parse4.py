from simpleparse.common import numbers, strings, comments
from simpleparse.parser import Parser as SimpleParse
from element import Element

class Parser:

	def __init__(self):
		self.line	= 0
		self.stack	= []
		self.depth	= 0
		declaration = r'''
		file		::= line+
		line		::=	depth, expr+, '\n'?
		depth		::= [ \t]*
		>expr<		::= symbol, ws*
		<ws>		::= whitespace
		>symbol<	::= method/element
		>element<	::= attr/cat/iden/name/num/content
		method		::= "def:", whitespace*, (element, whitespace*)+
		name		::= [a-zA-Z]+, [0-9]*
		cat			::= ".", name
		iden		::= "#", name
		attr		::= name, "=", !, value
		value		::= name/[0-9]+/content
		>num<		::= "*", whitespace*, !, multiples
		multiples	::= [0-9]+
		content		::= ('"',!,-'"'*,'"')/("'",!,-"'"*,"'")
		'''
		self.parser = SimpleParse(declaration, "line")
		self.parse()

	def parseLine(self,line):
		b={}
		success, children, nextcharacter = self.parser.parse(line)
		for child in children:
			if child[0] == "attr":
				attr = line[child[1]:child[2]].split('=')
				if not child[0] in b:
					b[child[0]] = {}
				b[child[0]][attr[0]] = attr[1]
			elif child[0] == "content":
				content = line[child[1]:child[2]][1:-1]
				if not child[0] in b:
					b[child[0]] = []
				b[child[0]] += [content]
			else:
				if not child[0] in b:
					b[child[0]] = ""
				b[child[0]]+= line[child[1]:child[2]]
		return self.compileLine(b)

	def compileLine(self,line):
		self.compiled = {
			"depth":	len(line['depth']) if 'depth' in line else 0,
			"name":		line['name'] if 'name' in line else '',
			"cat":		line['cat'] if 'cat' in line else '',
			"iden":		line['iden'] if 'iden' in line else '',
			"attr":		line['attr'] if 'attr' in line else [],
			"children":	[],
			"content":	line['content'] if 'content' in line else [''],
			"closed":	True,
			"multiples":int(line['multiples']) if 'multiples' in line else 1
		}
		# print self.compiled['content']
		return self.compiled

	def lastElement(self):
		return self.stack[-1]

	def addElement(self,element,first=False):
		if first is True:
			self.toplevel = element
		else:
			self.lastElement().addChild(element)
		self.stack += [element]

	def parse(self):
		page = open('asptest.txt','r').readlines()
		for line in page:
			self.line += 1
			parsed = self.parseLine(line)
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
				# print self.lastElement().name, self.line
				self.stack.pop()
				# print self.lastElement().name, self.line
				self.addElement(element)

		self.toplevel.write()

a = Parser()