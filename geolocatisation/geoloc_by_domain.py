from network import networks
import argparse
import sys
from geolocatisation import dschield

parser = argparse.ArgumentParser(description='Geolocalisation by domains')
parser.add_argument('--domaine', dest='fqdn',help='make a fqdn for geolocalisation')
parser.add_argument('--filename',dest='list_domaine')
parser.add_argument('--geoloc_file',dest='geoloc_file')
parser.add_argument('--resolve_dns',dest='resolve_dns')
parser.add_argument('--geoloc_IP',dest='geoloc_IP')
parser.add_argument('--geoloc_country',dest='geoloc_country')
parser.add_argument('--outfile',dest='outfile')                 

args=parser.parse_args()
domaines=[]
geoloc=None
geoloc_country=False
if args.fqdn != None:
    domaines=[args.fqdn]
if args.list_domaine != None:
    print "Read Domaine List"
    with open(args.list_domaine,'r') as fr:
        for ligne in fr:
            domaines.append(ligne.strip())
if args.geoloc_IP != None:
    print "Geolocalisation Load"
    geoloc=[]
    if args.geoloc_file == None:
        parser.print_help()
        sys.exit(-1)
    print "geoloc"
    
if args.geoloc_country:
    print "Geolocalisation country ok"
    geoloc_country=True
            
for domaine in domaines:
    ip='0.0.0.0'
    ip=networks.resolve_dns(domaine)
    if ip != None:
        temp=ip+','+domaine
        if geoloc != None:
            geo=networks.geolocIP(args.geoloc_file,ip)
            temp=temp+','+geo
        if geoloc_country ==True:
            ds=dschield.dschield('http://dshield.org/ipinfo_ascii.html?ip=')
            ip,country,asname,network=ds.response(ip)              
            temp=temp+','+country
        print temp	
        geoloc.append(temp)
    else: 
        geoloc.append('DNS Failure: '+domaine)
if args.outfile != None:
    with open(args.outfile,'w') as fw:
        for ligne in geoloc:
            fw.write(ligne+'\n') 


