"""
Author: Collin Strassburg
Date Created: December 15, 2018
"""

import requests
import bs4
import json

#http://www.ni.com/en-us/shop/select/pxi-controller
#http://www.ni.com/en-us/shop/select/pxi-chassis



class CompactRIO:

	def getCompactRIO(self):
		return

class PCBasedSystems:
	def __init__(self):
		return

class PXIChassis:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class PXIController:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class PXIModule:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class PXI:

	def getController(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/pxi-controllers-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				if "remote-control" in item.a["href"]:	# JSON breaks for this type for PXI Controllers (caused by extra comma at char 22039 of controllerDict)
					controllerDict = controllerDict[0:22039] + controllerDict[22040:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current PXI Controller type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return PXIController(metadata)

	def getChassis(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/pxi-chassis-category",timeout=5)	# Creates list of pxi chassis categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Chassis
		for item in framework:		# Iterates over types of PXI Chassis
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				if "remote-control" in item.a["href"]:	# JSON breaks for this type for PXI Controllers (caused by extra comma at char 22039 of controllerDict)
					controllerDict = controllerDict[0:22039] + controllerDict[22040:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current PXI Chasis type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return PXIChassis(metadata)




	def getModule(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/pxi-modules-category",timeout=5)	# Creates list of pxi module categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Modules
		for item in framework:		# Iterates over types of PXI Modules
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict).replace("\\", "")
				if "remote-control" in item.a["href"]:	# JSON breaks for this type for PXI Controllers (caused by extra comma at char 22039 of controllerDict)
					controllerDict = controllerDict[0:22039] + controllerDict[22040:]
				#print(controllerDict[51560])
				d = json.loads(controllerDict)	# Creates dictionary of table info for current PXI Module type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						print(d["attrHeadInfo"])
						metadata = d
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return PXIModule(metadata)


class CompactRIOController:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class CompactRIOChassis:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class CompactRIOModule:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class CompactRIO:



	def getController(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactrio-controllers-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				#print(controllerDict[143087])
				if "compactrio-controller" in item.a["href"]:	# JSON breaks for this type for compactRIO Controllers (caused by extra comma at char 143087 of controllerDict)
					controllerDict = controllerDict[0:143087] + controllerDict[143088:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Controller type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text or "User Guide" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactRIOController(metadata)

	def getChassis(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactrio-chassis-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				#print(controllerDict[17630])
				if "compactrio-chassis" in item.a["href"]:	# JSON breaks for this type for compactRIO Chassis (caused by extra comma at char 17630 of controllerDict)
					controllerDict = controllerDict[0:17630] + controllerDict[17631:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Chassis type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactRIOChassis(metadata)


	def getModule(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactrio-modules-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				#print(controllerDict[16967])
				if "c-series-universal-analog-input-module" in item.a["href"]:	# JSON breaks for this type for compactRIO Chassis (caused by extra comma at char 17630 of controllerDict)
					controllerDict = controllerDict[0:16967] + controllerDict[16968:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Chassis type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactRIOModule(metadata)


class CompactDAQController:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class CompactDAQChassis:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)

class CompactDAQModule:
	def __init__(self,group):
		self.name = group
		self.info = (group["attrHeadInfo"][0]["attributeVals"][0] if group is not None else None)


class CompactDAQ:
	def getController(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactdaq-controllers-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				#print(controllerDict[24513])
				if "compactdaq-controller" in item.a["href"]:	# JSON breaks for this type for compactRIO Controllers (caused by extra comma at char 143087 of controllerDict)
					controllerDict = controllerDict[0:24513] + controllerDict[24514:]
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Controller type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text or "User Guide" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactDAQController(metadata)


	def getChassis(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactdaq-chassis-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Controller type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text or "User Guide" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactDAQChassis(metadata)


	def getModule(self, controllerName):
		metadata = None
		controller_response = requests.get("http://www.ni.com/en-us/shop/select/compactdaq-modules-category",timeout=5)	# Creates list of pxi controller categories
		controller_content =  bs4.BeautifulSoup(controller_response.content,"html.parser")
		framework = controller_content.find_all("div", attrs={"class":"ni-product-name ni-margin-1x"})	# Gets all types of PXI Controllers
		for item in framework:		# Iterates over types of PXI Controllers
			#print(item.a.text)		#Prints type names
			category = requests.get("http://www.ni.com/en-us/shop/select/"+item.a["href"],timeout=5)
			if controllerName in category.text:
				category_content = bs4.BeautifulSoup(category.content, "html.parser")
				js_text = category_content.find_all('script')
				count = 0
				while "var pnTableItem = {" not in js_text[count].text:
					count += 1
				controllerDict = js_text[count].text.split("var pnTableItem = ")
				controllerDict = "".join(controllerDict)
				controllerDict = controllerDict.split("var")[0]
				controllerDict = "".join(controllerDict)
				d = json.loads(controllerDict)	# Creates dictionary of table info for current compactRIO Controller type
				for item in d["tableItems"]:
					if item["modelName"] == controllerName:
						#print(d["attrHeadInfo"])
						metadata = d
						# print(item["modelName"])
						downloadable = False
						if "pdf" in item["techDocs"]:
							manual = requests.get(item["techDocs"])
							downloadable = True
						else:
							search_response = requests.get("http://www.ni.com" + item["techDocs"], timeout=5)
							search_content = bs4.BeautifulSoup(search_response.content, "html.parser")
							links = search_content.findAll("a")
							for link in links:
								if "User Manual and Specifications" in link.text or "User Guide" in link.text:
									manual = requests.get(link["href"])
									downloadable = True
						if downloadable:
							with open(item["modelName"] + ";Data.pdf", "wb") as f:
								f.write(manual.content)
						else:
							print("Sorry, there's currently no datasheet on the website for "+controllerName+"!")
		return CompactDAQModule(metadata)
