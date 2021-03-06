#!/usr/bin/python
'''
Created on Sep 25, 2012

@author: slarinier
'''

from actions import Actions
import argparse
from history.history import History
import sys
import threading



    
if __name__ == '__main__':
    scriptsJS=['harvesting/googlesearch.js','harvesting/bingsearch.js','harvesting/yahoosearch.js']
    h=History()
    result=[]
    domaine_ip={}

#limit=sys.argv[4]
    
    
    parser = argparse.ArgumentParser(description='metaharvester')
    parser.add_argument('--db', dest='db', help='db in mongo to store informations')
    parser.add_argument('--toto', dest='toto')
    parser.add_argument('--action', dest='action')
    parser.add_argument('--criteria', dest='criteria')
    parser.add_argument('--collection', dest='collection')
    parser.add_argument('--attr', dest='attr')
    parser.add_argument('--threadpool', dest='threadpool')
    parser.add_argument('--filters', dest='filters')
    args = parser.parse_args()
    db=args.db
    filters=args.filters
    criteria=args.criteria
    if criteria==None:
        criteria=''
    geoloc=args.toto
    if geoloc==None:
        geoloc=''
    collection=args.collection
    attr=args.attr
    msg=db+' '+ ' '+args.action+' '+criteria
    h.register(msg)
    act=Actions(db)
    if args.action=='reset':
        act.reset()
    elif args.action=='metasearch':
        if criteria and scriptsJS and db and geoloc:
            criteria=criteria.split(',')
            act.metasearch(criteria,scriptsJS,geoloc)    
    elif args.action=='search_ip':
        act.search_ip(geoloc,scriptsJS)
    elif args.action =='create_network':
        act.create_network()    
    elif args.action=='metadata':
        act.metadata_exctract()
    elif args.action == 'create_result':
        if not criteria and not db:
            parser.print_help()
        else:
            if collection:
                act.create_result(collection,criteria)
    elif args.action =='dnstree':
            if db:
                act.dnstree()
    elif args.action =='crawl':
            if db:
                act.crawl()
    elif args.action =='cleandb':
            if db and filters:
                act.clean_db(filters)
    elif args.action == 'screenshots':
            if db and args.threadpool:
                act.screenshots(args.threadpool)
            else:
                parser.print_help()
    elif args.action == 'init':
        if db and attr and collection:
            act.init(collection, attr)
        else:
            parser.print_help()    
    else:       
        
        parser.print_help()
        sys.exit(1)