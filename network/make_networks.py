from mongodb import mongodb
import re
from IPy import IP
class make_networks(object):

	def __init__(self,host,db):
		self.db=mongodb.mongodb(host,27017,db)
		self.networks={}
	
	def createNetworks(self,collection):
		result = self.db.selectall(collection)
		for domaine in result:
			try:
				network=domaine['network']
				fqdn=domaine['domaine']
				netname = domaine['netname']
				if network in self.networks:
					nt=self.networks[network]
					nt.append((fqdn,netname))
					self.networks[network]=nt
				else:
					self.networks[network]=[(fqdn,netname)]
			except KeyError:
				print 'probleme de cle '+str(domaine)
	def exportFile(self,namefile):
		keys =iter(self.networks)
		result=''
		with open(namefile,'w') as fw:
			for key in keys:
				try:
					result=''
					cidr=None
					try:
						cidr=IP(key.replace(' ',''))
					except ValueError:
						cidr=''
					
					#fw.write(key + ';')
					add=result.join(":"+str(item) for item in self.networks[key])

					fw.write(key + ';'+ add+';')
					fw.write(str(cidr)+'\n')
				except AttributeError:
						print 'erreur ' + key.replace(' ','')
						print cidr
				
		fw.close()
