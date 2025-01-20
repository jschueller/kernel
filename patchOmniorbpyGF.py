#  -*- coding: utf-8 -*-
# Copyright (C) 2025  CEA, EDF
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import sys
import re
import os
from pathlib import Path

def locateStub( fname ):
    print( f"Treating {fname}" )
    with open( fname ) as f:
        lines = f.readlines()
    pat0 = "Stub files contributing to this module"
    loc0 = [ (i,elt) for i,elt in enumerate(lines) if pat0 in elt]
    if len(loc0) != 1:
        return False
    pat1 = "Sub-modules"
    loc1 = [ (i,elt) for i,elt in enumerate(lines) if pat1 in elt]
    if len(loc1) != 1:
        return False
    print( f"Yes ... Treating {fname}" )
    pat2 = re.compile( "^import[\s]+([^\s]+)$" )
    writeNeeded = False
    for i in range( loc0[0][0] + 1 , loc1[0][0]):
        m = pat2.match( lines[i] )
        if m:
            writeNeeded = True
            newLine = "from .. import {}\n".format( m.group(1) )
            lines[i] = newLine
    #
    pat3 = re.compile( "^omniORB.updateModule[\s]*\(([^\)]+)\)$" )
    loc3 = [ i for i,elt in enumerate(lines) if pat3.match(elt) ]
    assert len(loc3) == 1
    i = loc3[0]
    m = pat3.match( lines[i] )
    modName = eval( m.group(1) )
    lines[i] = "omniORB.updateModule(\"salome.kernel.{}\")\n".format( modName )
    lines.append( lines[i] )
    print( f"End treating {fname}" )
    if writeNeeded:
        print( f"Updating {fname}" )
        with open( fname, "w" ) as f:
            f.writelines( lines )
    return True

def locateStub2( fname ):
    print( f"Treating {fname}" )
    with open( fname ) as f:
        lines = f.readlines()
    pat = re.compile( "^import[\s]+([^\s]+)$" )
    zeMatch = [ (i,elt) for i,elt in enumerate(lines) if pat.match(elt) ]
    writeNeeded = False
    for i,elt in zeMatch:
        newLine = "from . import {}\n".format( pat.match(elt).group(1) )
        writeNeeded = True
        lines[i] = newLine
    pat2 = re.compile( "^([^\s]+)[\s]*=[\s]*omniORB.openModule[\s]*\(([^\)]+)\)$" )
    zeMatch = [ (i,elt) for i,elt in enumerate(lines) if pat2.match(elt) ]
    for i,elt in zeMatch:
        m = pat2.match( elt )
        st = m.group(2)
        st = st.strip()
        params = re.split(",[\s]+",st)
        if len(params) == 1:
            newLine = "{} = omniORB.openModule(\"salome.kernel.{}\")\n".format( m.group(1) , eval( params[0] ) )
        else:
            newLine = "{} = omniORB.openModule(\"salome.kernel.{}\" , {})\n".format( m.group(1) , eval( params[0] ), params[1] )
        writeNeeded = True
        lines[i] = newLine
    if writeNeeded:
        print( f"Updating {fname}" )
        with open( fname, "w" ) as f:
            f.writelines( lines )
    return True

initFile = "__init__.py"
#installDir = sys.argv[1]
installDir = "/home/H87074/salome/990_CEA/SALOME-master-native-DB11-SRC/SOURCES/kernel_install"
filesToTreat = []
for root,dirs,fis in os.walk( installDir ):
    if initFile in fis:
        filesToTreat.append( ( Path(root) / initFile ).as_posix() )
for elt in filesToTreat:
    locateStub( elt )
filesToTreat = []
for root,dirs,fis in os.walk( installDir ):
    filesToTreat += [ ( Path(root) / fi ).as_posix() for fi in fis if fi[-7:] == "_idl.py" ]
print( "\n".join( filesToTreat ) )
for elt in filesToTreat:
    locateStub2( elt )
