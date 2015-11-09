import requests

class Model():

	def __init__(self,app_host=None):
		self.host = app_host

	def getAll(self):

		response = requests.get(self.host + '/brand')

		assert response.status_code == 200

		return response.json()