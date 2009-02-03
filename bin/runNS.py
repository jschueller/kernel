#!/usr/bin/env python
#  Copyright (C) 2007-2008  CEA/DEN, EDF R&D, OPEN CASCADE
#
#  Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
#  CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#log files localization
#
import os, commands, sys, re, string, socket
from Utils_Identity import getShortHostName

if sys.platform == "win32":
  # temporarily using home directory for Namning Service logs
  # to be replaced with TEMP later...
  os.environ["BaseDir"]=os.environ["HOME"]
else:
  os.environ["BaseDir"]="/tmp"

os.environ["Username"]=os.environ["USER"]

# kill OmniNames if exists

#killall -q -9 omniNames

# clear log files

def startOmni():
  try:
    os.mkdir(os.environ["BaseDir"] + "/logs")
    os.chmod(os.environ["BaseDir"] + "/logs", 0777)
  except:
    #print "Can't create " + os.environ["BaseDir"] + "/logs"
    pass
  
  upath = os.environ["BaseDir"] + "/logs/" + os.environ["Username"]

  try:
    os.mkdir(upath)
  except:
    #print "Can't create " + upath
    pass

  #os.system("touch " + upath + "/dummy")
  for fname in os.listdir(upath):
    try:
      if not fname.startswith("."): os.remove(upath + "/" + fname)
    except:
      pass
  #os.system("rm -f " + upath + "/omninames* " + upath + "/dummy " + upath + "/*.log")

  print "Name Service... "
  #hname=os.environ["HOST"] #commands.getoutput("hostname")
  if sys.platform == "win32":
          hname=getShortHostName()
  else:
    hname=socket.gethostname()

  print "hname=",hname
  
  f=open(os.environ["OMNIORB_CONFIG"])
  ss=re.findall("NameService=corbaname::" + hname + ":\d+", f.read())
  print "ss = ", ss
  f.close()
  aPort=re.findall("\d+", ss[0])[0]
  
  #aSedCommand="s/.*NameService=corbaname::" + hname + ":\([[:digit:]]*\)/\1/"
  #print "sed command = ", aSedCommand
  #aPort = commands.getoutput("sed -e\"" + aSedCommand + "\"" + os.environ["OMNIORB_CONFIG"])
  global process_id
  print "port=", aPort
  if sys.platform == "win32":          
          #import win32pm
          #command = ['omniNames -start ' , aPort , ' -logdir ' , '\"' + upath + '\"']
          #os.system("start omniNames -start " + aPort + " -logdir " + "\"" + upath + "\"" )
          command = "start omniNames -start " + aPort + " -logdir " + "\"" + upath + "\""
          #print command
          pid = win32pm.spawnpid( string.join(command, " "), -nc )
          process_id[pid]=command
  else:
    os.system("omniNames -start " + aPort + " -logdir " + upath + " &")

  print "ok"
  print "to list contexts and objects bound into the context with the specified name : showNS "

# In LifeCycleCORBA, FactoryServer is started with rsh on the requested
#    computer if this Container does not exist. Default is localhost.
#    Others Containers are started with start_impl method of FactoryServer Container.
# For using rsh it is necessary to have in the ${HOME} directory a .rhosts file
# Warning : on RedHat the file /etc/hosts contains by default a line like :
# 127.0.0.1               bordolex bordolex.paris1.matra-dtv.fr localhost.localdomain localhost  
#   (bordolex is the station name). omniNames on bordolex will be accessible from other
#   computers only if the computer name is removed on that line like :
#   127.0.0.1               bordolex.paris1.matra-dtv.fr localhost.localdomain localhost

# To start dynamically Containers on several computers you need to
# put in the ${OMNIORB_CONFIG} file a computer name instead of "localhost"
# example : ORBInitRef NameService=corbaname::dm2s0017

# If you need to use several omniNames running on the same computer, you have to :
#1. put in your ${OMNIORB_CONFIG} file a computer name and port number
# example : ORBInitRef NameService=corbaname::dm2s0017:1515
#2. start omninames with this port number in runNS.sh
# example : omniNames -start 1515 -logdir ${BaseDir}/logs/${Username} &