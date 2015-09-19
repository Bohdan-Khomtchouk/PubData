import os,json

def create_directory_structure(rootdir,d={}):

    for path, _, files in os.walk(rootdir):
    	d[path]=files

	with open('newjson.json','w')as f:
		json.dump(d,f,indent=4)


def change_path(file_name,source,destination):

	with open('newjson.json','r+')as f:
		dic_structure=json.load(f)
		try:
			files=dic_structure[source]
			files.remove(file_name)
			dic_structure[source]=files
			des=dic_structure[destination]
			des.append(file_name)
			dic_structure[destination]=des
			with open('newjson.json','w')as f:
				json.dump(dic_structure,f,indent=4)
		except KeyError:
			print('Your path is wrong Please try again later with a valid path')

def remove_path(file_name,path):

	with open('newjson.json','r+')as f:
		dic_structure=json.load(f)
	try:
		files=dic_structure[path]
		files.remove(file_name)
		dic_structure[path]=files
		with open('newjson.json','w')as f:
			json.dump(dic_structure,f,indent=4)
	except KeyError:
			print('Your path is wrong Please try again later with a valid path')
