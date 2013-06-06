import string

class Line:
	def __init__(self,line):
		self.depth = 0
		self.name = "div"
		self.cat = []
		self.iden = []
		self.attr = {}
		self.content = []
		self.multiples = 1
		self.expected = ""
		self.word = ""
		self.escaped = False
		self.lastexpected = ""
		self.line = line

	def setDepth(self,depth):
		self.depth = depth

	def setName(self,name):
		self.name = name
		# print name

	def addClass(self,cat):
		self.cat += [cat]

	def addID(self,iden):
		self.iden += [iden]

	def addAttribute(self,attr,value):
		self.attr[attr] = value

	def addContent(self,content):
		self.content += content
		print content

	def multiply(self,multiples):
		self.multiples *= multiples

	def expecting(self,expect):
		return self.expected == expect

	def append(self,char):
		self.word += char
		# print char if char == "=" else None

	def isEmpty(self):
		return not bool(self.word)

	def setEscaped(self,escaped):
		self.escaped = escaped

	def isEscaped(self):
		return self.escaped

	def openQuote(self,quote):
		self.lastexpected = quote

	def isEndquote(self,char):
		return char == self.lastexpected or char

	def expect(self,expect):
		word = self.word
		self.word = ""
		if self.expecting("tabs"):
			self.setDepth(len(word))
		elif self.expecting("abc"):
			if expect == "=":
				self.word = word + "="
			elif word:
				self.setName(word)
		elif self.expecting("class"):
			self.addClass(word)
		elif self.expecting("id"):
			self.addID(word)
		elif self.expecting("attr"):
			try:
				# print(word.split('='),expect,word)
				self.addAttribute(*word.split('='))
			except Exception as e:
				print e, [x for x in word.split('=')]
		elif self.expecting("content"):
			self.addContent(word)
		elif self.expecting("multiples"):
			self.multiply(word)
		expectdict = {
			"abc" : "abc",
			"tabs" : "tabs",
			"." : "class",
			"#" : "id",
			"=" : "attr",
			"\"" : "content",
			"'" : "content",
			"*" : "multiples"
		}
		# or "unexpected" included to prevent searching expectdict for NoneType
		if expect in expectdict:
			# print expectdict[expect], word
			self.expected = expectdict[expect]
			self.openQuote(expect)
		elif str(expect) in string.letters:
			self.expected = expectdict["abc"]
			self.openQuote(expect)
		else:
			self.expected = None

	def compile(self):
		compiled = {
			"depth":self.depth,
			"name":self.name,
			"cat":self.cat,
			"iden":self.iden,
			"attr":self.attr,
			"content":self.content,
			"multiples":self.multiples
		}
		return compiled if len(self.line) > self.depth else None