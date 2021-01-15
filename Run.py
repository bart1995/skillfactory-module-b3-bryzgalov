class HTML():
	def __init__(self, output):
		self.output = output
		self.children = []

	def __iadd__(self, other):
		self.children.append(other)
		return self

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		html='<!DOCTYPE html>\n<html>\n'
		for child in self.children:
			html += str(child) + '\n'
		html+='</html>'
		t=open(self.output, 'w')
		return t.write(html)

class TopLevelTag():

	def __init__(self, tag):
		self.tag = tag
		self.children = []



	def __iadd__(self, other):
		self.children.append(other)
		return self
		

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def __str__(self):
		code='<{tag}>\n'.format(tag = self.tag)
		for child in self.children:
			code +=str(child) + '\n'

		code += '</{tag}>'.format(tag = self.tag)
		return code

class Tag():
	def __init__(self, tag, klass = None, is_single=False, **kwargs):
		self.tag = tag
		self.klass = klass
		self.is_single = is_single
		self.text = ''
		self.attributes = {}
		self.children = []

		for attribute, value in kwargs.items():
			self.attributes[attribute+' = '] = '"' + value + '"'

	def __iadd__(self, other):
		self.children.append(other)
		return self

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def __str__(self):
		tag = '<{tag}'.format(tag=self.tag)
		if self.klass:
			classNames=' class = "'
			for className in self.klass:
				classNames += className + ' '
			tag += classNames + '"'
		else:
			classNames=''

		attr=''
		for attribute in self.attributes.items():
			attr+=' '+''.join(attribute)

		tag += attr+'>'

		for child in self.children:
			tag += '\n'+str(child)+'\n'

		tag +=self.text

		if self.is_single==False:
			closetag='</%s>\n'%(self.tag)
		else:
			closetag=''

		tag += closetag


		return tag




with HTML(output="test.html") as doc:
	with TopLevelTag("head") as head:
		with Tag("title") as title:
			title.text = "hello"
			head += title
		doc += head

	with TopLevelTag("body") as body:
		with Tag("h1", klass=("main-text",)) as h1:
			h1.text = "Test"
			body += h1

		with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
			with Tag("p") as paragraph:
				paragraph.text = "another test"
				div += paragraph

			with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
				div += img
			body += div
		doc += body
