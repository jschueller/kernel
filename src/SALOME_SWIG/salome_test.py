#  SALOME SALOME_SWIG : binding of C++ implementation and Python
#
#  Copyright (C) 2003  CEA/DEN, EDF R&D
#
#
#
#  File   : salome_test.py
#  Module : SALOME

print "Test the application loading  GEOM, SMESH, VISU, MED, components and doing some"
print "operation within the components."

import salome
from salome import sg
import SALOMEDS
import os

print "======================================================================"
print "           Create Study "
print "======================================================================"

import geompy

print "================================="
print "       create AttributeReal      "
print "================================="
A = geompy.myBuilder.FindOrCreateAttribute(geompy.father, "AttributeReal")
if A == None :
	raise  RuntimeError, "Can't create AttributeReal attribute"
A = A._narrow(SALOMEDS.AttributeReal)
A.SetValue(0.0001)
if A.Value() != 0.0001:
	raise  RuntimeError, "Error : wrong value of  AttributeReal"

print
print " ===========  Test Geometry  =========================="
print

print "==================================="
print "     define a box"
print "==================================="

box = geompy.MakeBox(0., 0., 0., 100., 200., 300.)
idbox = geompy.addToStudy(box,"box")

print
print "=============  Test SMESH  ============================="
print

import SMESH
import smeshpy

geom = salome.lcc.FindOrLoadComponent("FactoryServer", "Geometry")
myBuilder = salome.myStudy.NewBuilder()

smeshgui = salome.ImportComponentGUI("SMESH")
smeshgui.Init(salome.myStudyId);

ShapeTypeCompSolid = 1
ShapeTypeSolid = 2
ShapeTypeShell = 3
ShapeTypeFace = 4
ShapeTypeWire = 5
ShapeTypeEdge = 6
ShapeTypeVertex = 7

# ---- define a box

box = geompy.MakeBox(0., 0., 0., 100., 200., 300.)
idbox = geompy.addToStudy(box,"box")

# ---- add first face of box in study

subShapeList=geompy.SubShapeAll(box,ShapeTypeFace)
face=subShapeList[0]
name = geompy.SubShapeName( face._get_Name(), box._get_Name() )
print name
idface=geompy.addToStudyInFather(box,face,name)

# ---- add shell from box  in study

subShellList=geompy.SubShapeAll(box,ShapeTypeShell)
shell = subShellList[0]
name = geompy.SubShapeName( shell._get_Name(), box._get_Name() )
print name
idshell=geompy.addToStudyInFather(box,shell,name)

# ---- add first edge of face in study

edgeList = geompy.SubShapeAll(face,ShapeTypeEdge)
edge=edgeList[0];
name = geompy.SubShapeName( edge._get_Name(), face._get_Name() )
print name
idedge=geompy.addToStudyInFather(face,edge,name)

# ---- launch SMESH, init a Mesh with the box
gen=smeshpy.smeshpy()
mesh=gen.Init(idbox)

idmesh = smeshgui.AddNewMesh( salome.orb.object_to_string(mesh) )
smeshgui.SetName(idmesh, "Meshbox");
smeshgui.SetShape(idbox, idmesh);

# ---- create Hypothesis

print "-------------------------- create Hypothesis"
print "-------------------------- LocalLength"
hyp1=gen.CreateHypothesis("LocalLength")
hypLen1 = hyp1._narrow(SMESH.SMESH_LocalLength)
hypLen1.SetLength(100)
print hypLen1.GetName()
print hypLen1.GetId()
print hypLen1.GetLength()

idlength = smeshgui.AddNewHypothesis( salome.orb.object_to_string(hypLen1) );
smeshgui.SetName(idlength, "Local_Length_100");

print "-------------------------- NumberOfSegments"
hyp2=gen.CreateHypothesis("NumberOfSegments")
hypNbSeg1=hyp2._narrow(SMESH.SMESH_NumberOfSegments)
hypNbSeg1.SetNumberOfSegments(7)
print hypNbSeg1.GetName()
print hypNbSeg1.GetId()
print hypNbSeg1.GetNumberOfSegments()

idseg = smeshgui.AddNewHypothesis( salome.orb.object_to_string(hypNbSeg1) );
smeshgui.SetName(idseg, "NumberOfSegments_7");

print "-------------------------- MaxElementArea"
hyp3=gen.CreateHypothesis("MaxElementArea")
hypArea1=hyp3._narrow(SMESH.SMESH_MaxElementArea)
hypArea1.SetMaxElementArea(2500)
print hypArea1.GetName()
print hypArea1.GetId()
print hypArea1.GetMaxElementArea()

idarea1 = smeshgui.AddNewHypothesis( salome.orb.object_to_string(hypArea1) );
smeshgui.SetName(idarea1, "MaxElementArea_2500");

print "-------------------------- MaxElementArea"
hyp3=gen.CreateHypothesis("MaxElementArea")
hypArea2=hyp3._narrow(SMESH.SMESH_MaxElementArea)
hypArea2.SetMaxElementArea(500)
print hypArea2.GetName()
print hypArea2.GetId()
print hypArea2.GetMaxElementArea()

idarea2 = smeshgui.AddNewHypothesis( salome.orb.object_to_string(hypArea2) );
smeshgui.SetName(idarea2, "MaxElementArea_500");

print "-------------------------- Regular_1D"
alg1=gen.CreateHypothesis("Regular_1D")
algo1=alg1._narrow(SMESH.SMESH_Algo)
listHyp=algo1.GetCompatibleHypothesis()
for hyp in listHyp:
    print hyp
algoReg=alg1._narrow(SMESH.SMESH_Regular_1D)
print algoReg.GetName()
print algoReg.GetId()

idreg = smeshgui.AddNewAlgorithms( salome.orb.object_to_string(algoReg) );
smeshgui.SetName(idreg, "Regular_1D");

print "-------------------------- MEFISTO_2D"
alg2=gen.CreateHypothesis("MEFISTO_2D")
algo2=alg2._narrow(SMESH.SMESH_Algo)
listHyp=algo2.GetCompatibleHypothesis()
for hyp in listHyp:
    print hyp
algoMef=alg2._narrow(SMESH.SMESH_MEFISTO_2D)
print algoMef.GetName()
print algoMef.GetId()

idmef = smeshgui.AddNewAlgorithms( salome.orb.object_to_string(algoMef) );
smeshgui.SetName(idmef, "MEFISTO_2D");

# ---- add hypothesis to edge

print "-------------------------- add hypothesis to edge"
edge=salome.IDToObject(idedge)
submesh=mesh.GetElementsOnShape(edge)
ret=mesh.AddHypothesis(edge,algoReg)
print ret
ret=mesh.AddHypothesis(edge,hypLen1)
print ret

idsm1 = smeshgui.AddSubMeshOnShape( idmesh,
                                    idedge,
                                    salome.orb.object_to_string(submesh),
                                    ShapeTypeEdge )
smeshgui.SetName(idsm1, "SubMeshEdge")
smeshgui.SetAlgorithms( idsm1, idreg );
smeshgui.SetHypothesis( idsm1, idlength );

print "-------------------------- add hypothesis to face"
face=salome.IDToObject(idface)
submesh=mesh.GetElementsOnShape(face)
ret=mesh.AddHypothesis(face,hypArea2)
print ret

idsm2 = smeshgui.AddSubMeshOnShape( idmesh,
                                    idface,
                                    salome.orb.object_to_string(submesh),
                                    ShapeTypeFace )
smeshgui.SetName(idsm2, "SubMeshFace")
smeshgui.SetHypothesis( idsm2, idarea2 );

# ---- add hypothesis to box

print "-------------------------- add hypothesis to box"
box=salome.IDToObject(idbox)
submesh=mesh.GetElementsOnShape(box)
ret=mesh.AddHypothesis(box,algoReg)
print ret
ret=mesh.AddHypothesis(box,hypNbSeg1)
print ret
ret=mesh.AddHypothesis(box,algoMef)
print ret
ret=mesh.AddHypothesis(box,hypArea1)
print ret

smeshgui.SetAlgorithms( idmesh, idreg );
smeshgui.SetHypothesis( idmesh, idseg );
smeshgui.SetAlgorithms( idmesh, idmef );
smeshgui.SetHypothesis( idmesh, idarea1 );

gen.Compute(mesh, idbox)
sg.updateObjBrowser(1);

print
print "=============  Test  Supervisor  ============================="
print

from SuperV import *
import SALOMEDS
myStudy = salome.myStudy
myBuilder = myStudy.NewBuilder()

SuperVision = lcc.FindOrLoadComponent("SuperVisionContainer","Supervision")
father = myStudy.FindComponent("SUPERV")
if father is None:
        father = myBuilder.NewComponent("SUPERV")
        A1 = myBuilder.FindOrCreateAttribute(father, "AttributeName");
        FName = A1._narrow(SALOMEDS.AttributeName)
        FName.SetValue("Supervision")
      	A2 = myBuilder.FindOrCreateAttribute(father, "AttributePixMap");
      	aPixmap = A2._narrow(SALOMEDS.AttributePixMap);
	aPixmap.SetPixMap( "ICON_OBJBROWSER_Supervision" );
	myBuilder.DefineComponentInstance(father,SuperVision)

def addStudy(ior):
    dataflow = SuperVision.getGraph(ior)
    name=dataflow.Name()
    itr = myStudy.NewChildIterator(father)
    while itr.More():
        item=itr.Value()
        res,A=item.FindAttribute("AttributeName")
        if res:
            aName = A._narrow(SALOMEDS.AttributeName)
            if aName.Value() == name :
	        print myBuilder.FindOrCreateAttribute(item, "AttributeIOR")
		A  = myBuilder.FindOrCreateAttribute(item, "AttributeIOR")
		print "A = ", A
		if A is not None :
                   #res,A = myBuilder.FindOrCreateAttribute(item, "AttributeIOR")
                   anIOR  = A._narrow(SALOMEDS.AttributeIOR);
		   print "anIOR.SetValue(dataflow.getIOR())"
		   anIOR.SetValue(dataflow.getIOR()) 
                return
        itr.Next()
    obj = myBuilder.NewObject(father)
    A=myBuilder.FindOrCreateAttribute(obj, "AttributeName")
    aName=A._narrow(SALOMEDS.AttributeName)
    aName.SetValue(name)
    A=myBuilder.FindOrCreateAttribute(obj, "AttributeIOR")
    anIOR  = A._narrow(SALOMEDS.AttributeIOR)
    anIOR.SetValue(dataflow.getIOR())

import os
dir= os.getenv("SALOME_ROOT_DIR")
if dir == None:
	raise RuntimeError, "SALOME_ROOT_DIR is not defined"
xmlfile = dir +"/../SALOME_ROOT/SuperVisionTest/resources/GraphEssai.xml"
print "Load dataflow from the file : "
print xmlfile
print

myGraph = Graph ( xmlfile )

# This DataFlow is "valid" : no loop, correct links between Nodes etc...
print "myGraph.IsValid() = ", myGraph.IsValid()

# Get Nodes
myGraph.PrintNodes()
Add,Sub,Mul,Div = myGraph.Nodes()

# Load Datas
Addx = Add.Input("x",3.)
Addy = Add.Input("y",4.5)
Subx = Sub.Input("x",1.5)

# Get Output Port
Addz = Add.Port('z')
Subz = Sub.Port('z')
Mulz = Mul.Port('z')
Divz = Div.Port('z')

# This DataFlow is "executable" : all pending Ports are defined with Datas
print myGraph.IsExecutable()

# Starts only execution of that DataFlow and gets control immediatly
print myGraph.Run()

# That DataFlow is running ==> 0 (false)
print myGraph.IsDone()

# Events of execution :
aStatus,aNode,anEvent,aState = myGraph.Event()
while aStatus :
    print aNode.Thread(),aNode.SubGraph(),aNode.Name(),anEvent,aState
    aStatus,aNode,anEvent,aState = myGraph.Event()
print "myGraph.IsDone() = ",myGraph.IsDone()

# Wait for Completion (but it is already done after event loop ...)
print "Done : ",myGraph.DoneW()

# Get result
print "Result : ",Divz.ToString()

# Intermediate results :
print "Intermediate Result Add\z : ",Addz.ToString()
print "Intermediate Result Sub\z : ",Subz.ToString()
print "Intermediate Result Mul\z : ",Mulz.ToString()

print " "
#print "Type : print myGraph.IsDone()"
#print "       If execution is finished ==> 1 (true)"
res=myGraph.IsDone()
if res != 1:
	raise RuntimeError, "myGraph.Run() is not done"

print " "
print "Type : print Divz.ToString()"
print "       You will get the result"
Divz.ToString()

print " "
print "Type : myGraph.PrintPorts()"
print "       to see input and output values of the graph"
myGraph.PrintPorts()

print " "
print "Type : Add.PrintPorts()"
Add.PrintPorts()

print "Type : Sub.PrintPorts()"
Sub.PrintPorts()

print "Type : Mul.PrintPorts()"
Mul.PrintPorts()

print "Type : Div.PrintPorts()"
print "       to see input and output values of nodes"
Div.PrintPorts()

# Export will create newsupervisionexample.xml and the corresponding .py file
tmpdir=os.getenv("TmpDir")
if tmpdir is None:
	tmpdir="/tmp"
file = tmpdir + "/newsupervisionexample"
print "--------------\n"+file+"\n--------------\n"
myGraph.Export(file)

ior = salome.orb.object_to_string(myGraph.G)
addStudy(ior)

GraphName = myGraph.Name()
print "Befor save ",
#nodes = myGraph.Nodes()
nodes = myGraph.G.Nodes().FNodes
length_bs = len(nodes)
print "ListOfNodes length = ", length_bs
names=[]
for node in nodes:
	names.append(node.Name())
print names

print "Load FactorialComponent component, create dataflow using its services and run execution"
myPy = Graph('myPy')

eval = myPy.Node('FactorialComponent','FactorialComponent','eval')
eval.SetContainer('FactoryServerPy')

myPy.IsValid()

myPy.PrintPorts()

myPy.Run( 3 )

myPy.DoneW()

myPy.State()

myPy.PrintPorts()


sg.updateObjBrowser(1);

print
print "=============  Test  VISU  and MED ============================="
print
import sys
import SALOMEDS
import SALOME
import SALOME_MED
import VISU

import visu_gui

medFile = "pointe.med"
medFile = os.getenv('SALOME_ROOT_DIR') + '/../SALOME_ROOT/data/' + medFile
print "Load ", medFile

studyCurrent = salome.myStudyName

med_comp = salome.lcc.FindOrLoadComponent("FactoryServer", "Med")
myVisu = salome.lcc.FindOrLoadComponent("FactoryServer", "Visu")

try:
    if os.access(medFile, os.R_OK) :
       if os.access(medFile, os.W_OK) :
           med_comp.readStructFileWithFieldType(medFile,studyCurrent)
           med_obj = visu_gui.visu.getMedObjectFromStudy()
           print "med_obj - ", med_obj

           myField = visu_gui.visu.getFieldObjectFromStudy(2,1)
           aMeshName = "FILED_DOUBLE_MESH"
           anEntity = VISU.NODE
           aTimeStampId = 0
           
           myResult1 = myVisu.ImportMedField(myField)
           aMesh1 = myVisu.MeshOnEntity(myResult1, aMeshName, anEntity);
           
           aScalarMap1= myVisu.ScalarMapOnField(myResult1, aMeshName, anEntity, myField.getName(), aTimeStampId)
           if(myField.getNumberOfComponents() > 1) :
               aVectors = myVisu.VectorsOnField(myResult1, aMeshName, anEntity, myField.getName(), aTimeStampId)

           myResult2 = myVisu.ImportFile(medFile)
           aMeshName = "maa1"
           anEntity = VISU.NODE
           aMesh2 = myVisu.MeshOnEntity(myResult2, aMeshName, anEntity)

           aScalarMap2 = myVisu.ScalarMapOnField(myResult2, aMeshName, anEntity, myField.getName(), aTimeStampId)
           if(myField.getNumberOfComponents() > 1) :
             aCutPlanes = myVisu.CutPlanesOnField(myResult2, aMeshName, anEntity, myField.getName(), aTimeStampId)

           sg.updateObjBrowser(0)
       else :  print "We have no permission to rewrite medFile, so readStructFileWithFieldType can't open this file";
    else :  print  "We have no permission to read medFile, it will not be opened"; 

except:
    if sys.exc_type == SALOME.SALOME_Exception :
        print "There is no permission to read " + medFile
    else :
        print sys.exc_type 
        print sys.exc_value
        print sys.exc_traceback

sg.updateObjBrowser(1);