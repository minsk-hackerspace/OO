#!/usr/bin/python


import CommonMark
import sys
from pprint import pprint
import json
import datetime


md_text = ''

for line in sys.stdin:
	md_text += line

parser = CommonMark.DocParser()
	
ast = parser.parse(md_text)

# CommonMark.dumpAST(ast)
# quit()

files_dir = 'md2tex/'
config = {
	'header' : files_dir + '01_header.tex',
	'macro' : files_dir + '02_macro.tex',
	'hypersetup' : files_dir + '03_hypersetup.tex',
	'title' : files_dir + '04_title.tex'
	}

def md2tex_file(name):
	with open (name, 'r') as myfile:
		print("".join(myfile.readlines()))

md2tex_file(config['header'])
md2tex_file(config['macro'])
md2tex_file(config['hypersetup'])


'''
Code blocks may be used for python code in future.

For all document:
	Replace &mdash; with "---


Before 1-st SetextHeader - title page.



After 1-st SetextHeader - body.
	SetextHeader - first - \section{}, next - \newpage\section{}
	Paragraph - \begin{numberedpars}
	List - \begin{itemize} 
	ListItem - \item
	Emph - \emph{}
	Strong - \textbf{\large


'''

today = datetime.date.today()
year = today.year
day = today.day
month = {'January': 'января',
		'Feburary': 'февраля', 
		'March': 'марта', 
		'April': 'апреля', 
		'May': 'мая', 
		'June': 'июня', 
		'July': 'июля', 
		'August': 'августа', 
		'September': 'сентября', 
		'October': 'октября', 
		'November': 'ноября', 
		'December': 'декабря'
	}[today.strftime("%B")]



in_title_page = True
in_list_item = False

start = 'start'
end = 'end'

convert_dict ={
	False:	{
		'Document': {
			start: '\n\n\\begin{document}\n\n', 
			end: '\n\n\\end{document}\n\n'
		},
		'SetextHeader': { 
			start: '\n\\section{', 
			end: '}\n'
		},
		'Paragraph': { 
			start: '\n\\begin{numberedpars}\n', 
			end: '\n\\end{numberedpars}\n'
		},
		'List': { 
			start: '\n\\begin{itemize}\n', 
			end: '\n\\end{itemize}\n'
		},
		'ListItem': { 
			start: '\n\\item\n',
			end: '\n'
		},
		'Emph': { 
			start: '\\emph{',
			end: '}'
		},
		'Softbreak': {
			start: '\n'
		},
		'Entity': {},
		'Str': {},
		'Strong': {},
		'FencedCode': {}
	},
	True: {
		'Emph': { 
			start: '\\emph{',
			end: '}'
		},
		'Softbreak': {
			start: '\n'
		}
	}
}

def iter_ast (node):
	global in_title_page
	global in_list_item
	global convert_dict
	
	cd = convert_dict[in_list_item]

	if node.t in cd and start in cd[node.t] and len(cd[node.t][start]) > 0:
		print(cd[node.t][start], end='')
	
	if node.t == 'Document':
		print('\\date{\\large г. Минск\\\\%d}' % year)
		
		print('\\titlehead{\\raggedleft \\begin{minipage}{15em}\\flushleft')
		print('Утвержден \\\\\n Учредительным Общим Собранием Просветительского общественного объединения \\RuName \\\\')
		print('года %d %s «%d»' % (year, month, day))
		print('\\end{minipage}}')
		
		md2tex_file(config['title'])

	
	if node.t == 'ListItem':
		in_list_item = True
	
	if type(node.children) is list and len(node.children) > 0:
		for n in node.children:
			iter_ast(n)
			
	if type(node.inline_content) is list and len(node.inline_content) > 0:
		for n in node.inline_content:
			iter_ast(n)
			
	if type(node.c) is list and len(node.c) > 0:
		for n in node.c:
			iter_ast(n)
			
	if node.t == 'Entity':	
		print({
				'&mdash;': '"---'
			}[node.c], end='')
	elif type(node.c) is str:
		print(node.c, end='')	

	if node.t == 'ListItem':
		in_list_item = False
	
	if node.t == 'SetextHeader' and in_title_page:
		in_title_page = False
		convert_dict[False]['SetextHeader'][start] = '\\newpage\\section{'		
	
	if node.t in cd and end in cd[node.t] and len(cd[node.t][end]) > 0:
		print(cd[node.t][end], end='')



iter_ast(ast)


