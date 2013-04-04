import re

class Parser:
	
	def __init__(self,filepath):
		self.line = 0
		self.depth = 0
		self.filepath = filepath
		self.template = r"""^(?P<tabs>\t*)
							(?P<name>[^\W\d_]+)(?P<s>[^\S\r\n])*
							(?P<classid>(?:[\.|\#][^\W\d]+[^\W]*(?P=s)*)*)(?P=s)*
							(?P<content>\".*?\")*(?P=s)*
							(?:\*(?P=s)*(?P<multiples>\d))$"""

	def parseLine(self,line):
		parsed = re.match(self.template,line,re.X)
		if parsed is None:
			return parsed
		name = parsed.group('name')
		classid = parsed.group('classid')
		content = parsed.group('content')
		multiples = parsed.group('multiples')
		depth = len(parsed.group('tabs'))
		return {"name":name,"classid":classid,"content":content,"multiples":multiples,"depth":depth}

	def parse(self, block=None):
		lines = open(self.filepath,'r').readlines()
		if block is None:
			block = Element()
		with block as element:
			for line in lines:
				parsedLine = parseLine(line)
				if parsedLine is not None:
					pass