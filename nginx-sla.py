#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

statsurl='http://127.0.0.1/sla_status'

def discovery():
 try:
  res=urllib2.urlopen(statsurl)
 except:
  return 'ZBX_NOTSUPPORTED'

 dkeys=[]
 for line in res.readlines():
  mo=re.match('^(\S+) = (\d+)$',line)
  if mo is not None:
   nkey=mo.group(1)
   dkey=re.sub(r'\.(http(_...)?|([0-9]+|inf)(\.agg)?|[0-9]+%|time\.avg(\.mov)?)$','',nkey)
   if dkey not in dkeys:
    dkeys.append(dkey)

 result='{"data":['
 first=1
 for dkey in dkeys:
  pool,backend=dkey.split('.',1)
  if ':' not in backend:
   if first!=1:
    result+=','
   result+='{"{#POOL}":"%s","{#BACKEND}":"%s"}'%(pool,backend)
   first=0
 result+=']}'
 return result


def getdata(key):
 try:
  res=urllib2.urlopen('%s?key=%s'%(statsurl,key))
  return res.readline()
 except:
  return 'ZBX_NOTSUPPORTED'


if len(sys.argv)<2:
 print 'ZBX_NOTSUPPORTED'
 sys.exit(1)

key=sys.argv[1]

if key=='discovery':
 value=discovery()
else:
 value=getdata(key)

print value
