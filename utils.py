import os
import json

def db_save(path='DB/db.json',data={}, flag="w"):
	if not os.path.exists(path=path):
		open(path, 'w').close()
	try:
		json.dump(data, open(path, flag), indent=4)
	except Exception as ex:
		print(ex)

def get_data(path="DB/db.json", flag="r"):
	if not os.path.exists(path=path):
		open(path, "w").close()
	try:
		return json.load(open(path, flag))
	except:
		return {}
