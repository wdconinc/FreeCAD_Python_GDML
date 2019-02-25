
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 Keith Sloan <keith@sloan-home.co.uk>               *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         * 
#*   Acknowledgements : Ideas & code copied from			   * 
#*                      https://github.com/ignamv/geanTipi		   *
#*                                                                         *
#***************************************************************************
__title__="FreeCAD - GDML exporter Version"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_Geant4"]

import FreeCAD, os, Part, math
from FreeCAD import Vector

# xml handling
import argparse
#import xml.etree.ElementTree as ET
import lxml.etree as ET
from   xml.etree.ElementTree import XML 
global ET
#################################
# Globals
global gdml

try: import FreeCADGui
except ValueError: gui = False
else: gui = True

#***************************************************************************
# Tailor following to your requirements ( Should all be strings )          *
# no doubt there will be a problem when they do implement Value
if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    #rough_string = ET.tostring(elem, 'utf-8')
    rough_string = ET.tostring(elem).decode()
    #print rough_string
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
    #return(rough_string)

#################################
# Switch functions
################################
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

#################################
#  Setup GDML environment
#################################
def GDMLstructure() :
    print("Setup GDML structure")
    #################################
    # globals
    ################################
    global gdml, define, materials, solids, structure, setup
    global defineCnt

    defineCnt = 1
    gdml = ET.Element('gdml', {
          'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
          'xsi:noNamespaceSchemaLocation': "http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd"
})
    define = ET.SubElement(gdml, 'define')
    materials = ET.SubElement(gdml, 'materials')
    solids = ET.SubElement(gdml, 'solids')
    structure = ET.SubElement(gdml, 'structure')
    setup = ET.SubElement(gdml, 'setup', {'name': 'Default', 'version': '1.0'})
    ET.SubElement(setup, 'world', {'ref': 'worldLV'})
    #ET.ElementTree(gdml).write("test2", 'utf-8', True)


def defineMaterials():
    print("Define Materials")
    global materials
#
#   Some hardcoded isotopes, elements & materials
#
#   ISOTOPES
#
#   C0 - Carbon
#
    iso = ET.SubElement(materials,'isotope', \
                {'N': '12', 'Z': '6', 'name': "C120x56070ee874f0" })
    #ET.ElementTree(gdml).write("test7", 'utf-8', True)
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '12'})
    iso = ET.SubElement(materials,'isotope', {'N': '13', 'Z': '6', \
                        'name': "C130x56070ee940b0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '13.0034'})
    #ET.ElementTree(gdml).write("test3", 'utf-8', True)

#
#   N - Nitrogen
#
    iso = ET.SubElement(materials,'isotope', {'N': '14', 'Z': '7', \
                        'name': "N140x56070ee89030"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '14.0031'})
    iso = ET.SubElement(materials,'isotope', {'N': '15', 'Z': '7', \
                        'name': "N150x56070ee8feb0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '15.0001'})
#
#   O0 - Oxygen
#
    iso = ET.SubElement(materials,'isotope', {'N': '16', 'Z': '8', \
                        'name': "O160x56070ee8fa60"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '15.9949'})
    iso = ET.SubElement(materials,'isotope', {'N': '17', 'Z': '8', \
                        'name': "O170x56070ee8a570"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '16.9991'})
    iso = ET.SubElement(materials,'isotope', {'N': '18', 'Z': '8', \
                        'name': "O180x56070ee90cb0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '17.9992'})
    #ET.ElementTree(gdml).write("test3a", 'utf-8', True)
#
#   Cr Chromium
#
    iso = ET.SubElement(materials,'isotope', {'N': '50', 'Z': '24', \
                        'name': "Cr500x56070ee875e0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '49.946'})
    iso = ET.SubElement(materials,'isotope', {'N': '52', 'Z': '24', \
                        'name': "Cr520x56070ee897e0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '51.9405'})
    iso = ET.SubElement(materials,'isotope', {'N': '53', 'Z': '24', \
                        'name': "Cr530x56070ee89830"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '52.9407'})
    iso = ET.SubElement(materials,'isotope',{'N': '54', 'Z': '24', \
                        'name': "Cr540x56070ee89880"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '53.9389'})
    #ET.ElementTree(gdml).write("test3a2", 'utf-8', True)
#
#   Ni - Nickel
#
    iso = ET.SubElement(materials,'isotope', {'N': '58', 'Z': '28', \
                        'name': "Ni580x56070ee899c0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '57.9353'})
    iso = ET.SubElement(materials,'isotope', {'N': '60', 'Z': '28', \
                         'name': "Ni600x56070ee89a10"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '59.9308'})
    iso = ET.SubElement(materials,'isotope', {'N': '61', 'Z': '28', \
                         'name': "Ni610x56070ee89a60"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '61.9311'})
    iso = ET.SubElement(materials,'isotope', {'N': '62', 'Z': '28', \
                         'name': "Ni620x56070ee89ab0"})
    ET.SubElement(iso,'atom', {'uniti': 'g/mole', 'value': '61.9283'})
    iso = ET.SubElement(materials,'isotope', {'N': '64', 'Z': '28', \
                         'name': "Ni640x56070ee87ca0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '63.928'})
    #ET.ElementTree(gdml).write("test3b", 'utf-8', True)
#
#   Ar - Argon
#
    iso = ET.SubElement(materials,'isotope', {'N': '36', 'Z': '18', \
                         'name': "Ar360x56070ee8aba0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '35.9675'})
    iso = ET.SubElement(materials,'isotope', {'N': '38', 'Z': '18', \
                          'name': "Ar380x56070ee87400"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '37.9627'})
    iso = ET.SubElement(materials,'isotope', {'N': '40', 'Z': '18', \
                          'name': "Ar400x56070ee90c20"})
    ET.SubElement(iso,'atom', {'unitr': 'g/mole', 'value': '37.9627'})
#
#   Fe - Iron
#
    iso = ET.SubElement(materials,'isotope', {'N': '54', 'Z': '26', \
                           'name': "Fe540x56070ee87130"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '53.9396'})
    iso = ET.SubElement(materials,'isotope', {'N': '56', 'Z': '26', \
                            'name': "Fe560x56070ee95300"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '55.9349'})
    iso = ET.SubElement(materials,'isotope', {'N': '57', 'Z': '26', \
                            'name': "Fe570x56070ee8eff0"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '56.9354'})
    iso = ET.SubElement(materials,'isotope', {'N': '58', 'Z': '26', \
                             'name': "Fe580x56070ee8d300"})
    ET.SubElement(iso,'atom', {'unit': 'g/mole', 'value': '57.9333'}) 
    #ET.ElementTree(gdml).write("test4", 'utf-8', True)
#
#   ELEMENTS
#
    elem = ET.SubElement(materials,'element', {'name': "Iron0x56070eea0880"})
    ET.SubElement(elem,'fraction', {'n': '0.05845', 'ref': "Fe540x56070ee87130"})
    ET.SubElement(elem,'fraction', {'n': '0.91754', 'ref': "Fe560x56070ee95300"})
    ET.SubElement(elem,'fraction', {'n': '0.02119', 'ref': "Fe570x56070ee8eff0"})
    ET.SubElement(elem,'fraction', {'n': '0.00282', 'ref': "Fe580x56070ee8d300"})
    elem = ET.SubElement(materials,'element', {'name': "Chromium0x56070eea004"})
    ET.SubElement(elem,'fraction', {'n': '0.04345', 'ref': "Cr500x56070ee875e0"})
    ET.SubElement(elem,'fraction', {'n': '0.83789', 'ref': "Cr520x56070ee897e0"})
    ET.SubElement(elem,'fraction', {'n': '0.09501', 'ref': "Cr530x56070ee89830"})
    ET.SubElement(elem,'fraction', {'n': '0.02365', 'ref': "Cr540x56070ee89880"})
    elem = ET.SubElement(materials,'element', {'name': "Nickel0x56070ee81420"})
    ET.SubElement(elem,'fraction', {'n': '0.680769', 'ref': "Ni580x56070ee899c0"})
    ET.SubElement(elem,'fraction', {'n': '0.262231', 'ref': "Ni600x56070ee89a10"})
    ET.SubElement(elem,'fraction', {'n': '0.011399', 'ref': "Ni610x56070ee89a60"})
    ET.SubElement(elem,'fraction', {'n': '0.036345', 'ref': "Ni620x56070ee89ab0"})
    ET.SubElement(elem,'fraction', {'n': '0.009256', 'ref': "Ni640x56070ee87ca0"}) 
    elem = ET.SubElement(materials,'element', {'name': "N0x56070ee94e30"})
    ET.SubElement(elem,'fraction', {'n': '0.99632', 'ref': "N140x56070ee89030"})
    ET.SubElement(elem,'fraction', {'n': '0.00368', 'ref': "N150x56070ee8feb0"})
    elem = ET.SubElement(materials,'element', {'name': "O0x56070eea0370"})
    ET.SubElement(elem,'fraction', {'n': '0.99757', 'ref': "O160x56070ee8fa60"})
    ET.SubElement(elem,'fraction', {'n': '0.00038', 'ref': "O170x56070ee8a570"})
    ET.SubElement(elem,'fraction', {'n': '0.00205', 'ref': "O180x56070ee90cb0"})
    elem = ET.SubElement(materials,'element', {'name': "Ar0x56070eea07c0"})
    ET.SubElement(elem,'fraction', {'n': '0.003365', 'ref': "Ar360x56070ee8aba0"})
    ET.SubElement(elem,'fraction', {'n': '0.000632', 'ref': "Ar380x56070ee87400"})
    ET.SubElement(elem,'fraction', {'n': '0.996003', 'ref': "Ar400x56070ee90c20"})
    #ET.ElementTree(gdml).write("test5", 'utf-8', True)

#
#   MATERIALS
#
    sst = ET.SubElement(materials,'material', \
            {'name': "SSteel0x56070ee87d10", 'state': "gas"})
    ET.SubElement(sst,'T', {'unit': "K", 'value': '293.15'})
    ET.SubElement(sst,'MEE', {'unit': "eV", 'value': '282.530633667015'})
    ET.SubElement(sst,'D', {'unit': "g/cm3", 'value': '1.286547719061e-18'})
    ET.SubElement(elem,'fraction', {'n': '0.74', 'ref': "Iron0x56070eea0880"})
    ET.SubElement(elem,'fraction', {'n': '0.18', 'ref': "Chromium0x56070eea0040"}) 
    ET.SubElement(elem,'fraction', {'n': '0.08', 'ref': "Nickel0x56070ee81420"})
    sst = ET.SubElement(materials, 'material', \
            {'name': "SG4_AIR0x56070ee81710", 'state': "gas"})
    ET.SubElement(sst,'T', {'unit': "K", 'value': '293.15'})
    ET.SubElement(sst,'MEE', {'unit': "eV", 'value': '85.7'})
    ET.SubElement(sst,'D', {'unit': "g/cm3", 'value': '0.00120479'})
    ET.SubElement(elem,'fraction', {'n': '0.000124000124000124', \
                   'ref': "C0x56070ee949e0"})
    ET.SubElement(elem,'fraction', {'n': '0.755267755267755',  \
                   'ref': "N0x56070ee94e30"})
    ET.SubElement(elem,'fraction', {'n': '0.231781231781232', \
                   'ref': "O0x56070eea0370"})
    ET.SubElement(elem,'fraction', {'n': '0.0128270128270128', \
                     'ref': "Ar0x56070eea07c0"})
    #ET.ElementTree(gdml).write("test6", 'utf-8', True)
   
def defineBoundingBox(exportList,bbox):
    x = 1
    # Does not work if just a mesh`
    #for obj in exportList :
    #    print("{} + {} = ".format(bbox, obj.Shape.BoundBox))
    #    bbox.add(obj.Shape.BoundBox)
    #    print(bbox)


def constructWorld():
    print("Construct World")
    #ET.ElementTree(gdml).write("test9b", 'utf-8', True)
    # Volumes get added to structue section of gdml ( structure is a global )
    worldLV = ET.SubElement(structure,'volume', {'name': 'worldLV'})
    ET.SubElement(worldLV, 'materialref',{'ref': 'G4_AIR'})
    ET.SubElement(worldLV, 'solidref',{'ref': 'world'})
    # Solids get added to solids section of gdml ( solids is a global )
    ET.SubElement(solids, 'box',{'name': 'World','x': '0,1000','y': '0,1000','z': '0,1000','lunit' : 'mm'})
    #ET.ElementTree(gdml).write("test9c", 'utf-8', True)

    # Python has automatic garbage collection system.
    # Geometry objects must be defined as GLOBAL not to be deleted.
    #global sld_world, lv_world, pv_world, va_world

    #sld_world= G4Box("world", 1.*m, 1.*m, 1.*m)
    #lv_world= G4LogicalVolume(sld_world, air, "world")
    #pv_world= G4PVPlacement(G4Transform3D(), lv_world, "world",
    #                        None, False, 0)

    #va_world= G4VisAttributes()
    #va_world.SetVisibility(False)
    #lv_world.SetVisAttributes(va_world)

    # solid object (dummy)
    #    global sld_brep_box, sld_sld, lv_sld, pv_sld

    #solidBox = G4Box("dummy", 10.*cm, 10.*cm, 10.*cm)
    #lvBox = G4LogicalVolume(solidBox,SSteel,"box")

    #pos_x = G4double(-1.0*meter)
    #pos_x = -1.0
    #pos_y = G4doule(0.0*meter)
    #pos_y = 0.0
    #pos_z = G4double(0.0*meter)
    #pos_z = 0.0

    # Look for better constructor options for G4PVPlacement
    #pvBox = G4PVPlacement(G4RotationMatrix(),  # no rotaion \
    #                  G4ThreeVector(pos_x, pos_y, pos_z),   \
    #                  G4String("Box"),         # its name   \ 
    #                  lvBox,                   # its logical volume \
    #                  pv_world,                # its mother (physical) volume \
    #                  False,0)


    #    p1 = G4ThreeVector(0.0,0.0,0.0)
    #    p2 = G4ThreeVector(0.0,50.0,0.0)

def createLVandPV(obj,solidName):
    #
    # Logical & Physical Volumes get added to structure section of gdml
    #
    #ET.ElementTree(gdml).write("test9d", 'utf-8', True)
    #print("Object Base")
    #dir(obj.Base)
    #print dir(obj)
    #print dir(obj.Placement)
    name = obj.Name
    lvName = 'LV'+name
    pvName = 'PV'+name
    pos  = obj.Placement.Base
    angles = obj.Placement.Rotation.toEuler()
    print ("Angles")
    print angles
    lvol = ET.SubElement(structure,'volume', {'name':pvName})
    ET.SubElement(lvol, 'materialref', {'ref': 'SSteal'})
    ET.SubElement(lvol, 'solidref', {'ref': solidName})
    phys = ET.SubElement(lvol, 'physvol', {'name': str('PV'+name)})
    ET.SubElement(phys, 'volumeref', {'ref': lvName})
    ET.SubElement(phys, 'position', {'name': name+'_pos', 'unit': 'mm', \
                  'x': str(pos[0]), 'y': str(pos[1]), 'z': str(pos[2]) })
    ET.SubElement(phys, 'rotation', {'name': name+'_pos', 'unit': 'deg', \
                  'x': str(-angles[2]), \
                  'y': str(-angles[1]), \
                  'z': str(-angles[0])})

def reportObject(obj) :
    
    print("Report Object")
    print(obj)
    print("Name : "+obj.Name)
    print("Type : "+obj.TypeId) 
    print("Placement")
    print("Pos   : "+str(obj.Placement.Base))
    print("axis  : "+str(obj.Placement.Rotation.Axis))
    print("angle : "+str(obj.Placement.Rotation.Angle))
    
    while switch(obj.TypeId) :

      if case("Part::Sphere") :
         print("Sphere Radius : "+str(obj.Radius))
         break
           
      if case("Part::Box") : 
         print("cube : ("+ str(obj.Length)+","+str(obj.Width)+","+str(obj.Height)+")")
         break

      if case("Part::Cylinder") : 
         print("cylinder : Height "+str(obj.Height)+ " Radius "+str(obj.Radius))
         break
   
      if case("Part::Cone") :
         print("cone : Height "+str(obj.Height)+ " Radius1 "+str(obj.Radius1)+" Radius2 "+str(obj.Radius2))
         break

      if case("Part::Torus") : 
         print("Torus")
         print(obj.Radius1)
         print(obj.Radius2)
         break

      if case("Part::Prism") :
         print("Prism")
         break

      if case("Part::RegularPolygon") :
         print("RegularPolygon")
         break

      if case("Part::Extrusion") :
         print("Extrusion")
         break

      if case("Circle") :
         print("Circle")
         break

      if case("Extrusion") : 
         print("Wire extrusion")
         break

      print("Other")
      print(obj.TypeId)
      break

def fc2g4Vec(v) :
    print(str(v[0])+" : "+str(v[1])+" : "+str(v[2]))
    #    return(G4ThreeVector(int(v[0]),int(v[1]),int(v[2])))

def createFacet(v0,v1,v2) :
    global facet
    print("Create Facet : ")
    print(str(v0)+" : "+str(v1)+" : "+str(v2))
# following should work but does not wait for weyner response in forum
#    facet = MyG4TriangularFacet(v0,v1,v2)
    v0g4 = fc2g4Vec(v0)
    v1g4 = fc2g4Vec(v1)
    v2g4 = fc2g4Vec(v2)
    print(str(v0g4)+" : "+str(v1g4)+" : "+str(v2g4))
    #facet = MyG4TriangularFacet(v0g4,v1g4,v2g4)
    print("Facet constructed")
#   facet = G4VFacet() cannot be initiated from python
#   G4TrianglerFacet needs to be constructed with all three vectors
#   otherwise Isdefined is false and one gets an error 
# need to convert FreeCAD base.Vector to Geant4 vector Hep3Vector
    #print("Number Vert   : "+str(facet.GetNumberOfVertices()))
    #print("Area          : "+str(facet.GetArea()))
    #print("Is defined    : "+str(bool(facet.IsDefined)))
    #print(facet.GetVertex(0))
    #print(facet.GetVertex(1))
    #print(facet.GetVertex(2))
    #return(facet)

#    Add XML for TessellateSolid
def mesh2Tessellate(mesh, name) :
     global defineCnt

     baseVrt = defineCnt
     print "mesh"
     print mesh
     print dir(mesh)
     print "Facets"
     print mesh.Facets
     print "mesh topology"
     print dir(mesh.Topology)
     print mesh.Topology
#
#    mesh.Topology[0] = points
#    mesh.Topology[1] = faces
#
#    First setup vertex in define section vetexs (points) 
     print("Add Vertex positions")
     for fc_points in mesh.Topology[0] : 
         print(fc_points)
         v = 'v'+str(defineCnt)
         ET.SubElement(define, 'position', {'name': v, \
                  'x': str(fc_points[0]), \
                  'y': str(fc_points[1]), \
                  'z': str(fc_points[2]), \
                  'unit': 'mm'})
         defineCnt += 1         
#                  
#     Add faces
#
     print("Add Triangular vertex")
     tess = ET.SubElement(structure,'tessellated',{'name': name})
     for fc_facet in mesh.Topology[1] : 
       print(fc_facet)
       vrt1 = 'v'+str(baseVrt+fc_facet[0])
       vrt2 = 'v'+str(baseVrt+fc_facet[1])
       vrt3 = 'v'+str(baseVrt+fc_facet[2])
       ET.SubElement(tess,'triangular',{ \
         'vertex1': vrt1, 'vertex2': vrt2 ,'vertex3': vrt3, 'type': 'ABSOLUTE'})


def processMesh(obj) :

    print("Create Tessellate Logical Volume")
    createLVandPV(obj,"tessellated")
    mesh2Tessellate(obj.Mesh,obj.Name)
    #tessellate = mesh2Tessellate(obj.Mesh)

def shape2Mesh(shape) :
     import MeshPart
     return (MeshPart.meshFromShape(Shape=shape, Deflection = 0.0))
#            Deflection= params.GetFloat('meshdeflection',0.0)) 

def processObjectShape(obj) :
    print("Process Object Shape")
    print(obj)
    print(obj.PropertiesList)
    shape = obj.Shape
    print shape
    print(shape.ShapeType)
    while switch(shape.ShapeType) : 

         if case("Mesh::Feature") :
            print("Mesh - Should not occur should have been handled")
            #print("Mesh")
	    #tessellate = mesh2Tessellate(mesh) 
            #return(tessellate)
            #break

	 print("ShapeType Not handled")
         print(shape.ShapeType)
         break

#   Dropped through to here
#   Need to check has Shape
    print("Faces")
    for f in shape.Faces :
        print f
#        print dir(f)

# Create Mesh from shape & then Process Mesh to create Tessellated Solid in Geant4
    processMesh(wv,shape2Mesh(shape))
    createLVandPV(obj,"tessellated")


def processBoxObject(obj) :
    x = 1
    #solidBox = G4Box("dummy", 10.*cm, 10.*cm, 10.*cm)
    #lvBox = G4LogicalVolume(solidBox,SSteel,"box")

    #pos_x = -1.0
    #pos_y = 0.0
    #pos_z = 0.0

    # Look for better constructor options for G4PVPlacement
    #pvBox = G4PVPlacement(G4RotationMatrix(),  # no rotaion \
    #                  G4ThreeVector(pos_x, pos_y, pos_z),   \
    #                  G4String("Box"),         # its name   \
    #                  lvBox,                   # its logical volume \
    #                  wv,                # its mother (physical) volume \
    #                  False,0)


def processObject(obj) :
   
    print("\nProcess Object")
    #ET.ElementTree(gdml).write("test9a", 'utf-8', True)
    while switch(obj.TypeId) :
      #
      # Deal with non solids
      #
      if case("Part::Cut") :
         print("Cut")
         break

      if case("Part::Fuse") :
         print("Union")
         break

      if case("Part::Common") :
         print("intersection")
         break

      if case("Part::MultiFuse") :
         print("Multifuse") 
         break

      if case("Part::MultiCommon") :
         print("Multi Common / intersection")
         break

      if case("Mesh::Feature") :
         print("Mesh Feature") 
         processMesh(obj)
         break
      #
      #  Now deal with solids
      #
      while switch(obj.TypeId) :

         if case("Part::Box") :
            print("Box")
            processBoxObject(obj)
            break

         # Not a Solid that translated to GDML solid
         # Dropped through so treat object as a shape
         # Need to check obj has attribute Shape
         # Create a mesh & tessellate
         #
         processObjectShape(obj)
         break

def export(exportList,filename) :
    "called when FreeCAD exports a file"
   
    # process Objects
    print("\nStart GDML Export 0.1")
    GDMLstructure()
    defineMaterials()

    bbox = FreeCAD.BoundBox()
    defineBoundingBox(exportList,bbox)
    constructWorld()
    for obj in exportList :
        reportObject(obj)
        processObject(obj)
    #ET.ElementTree(gdml).write("test9e", 'utf-8', True)

    # write GDML file 
    print("Write to GDML file : "+filename)
    #gdml_pretty = prettify(gdml)
    gdml_pretty = ET.tostring(gdml,encoding='utf8').decode('utf8')
    #xmlstr = minidom.parseString(gdml_pretty).toprettyxma(indet=" ")
    #print xmlstr
    print(gdml_pretty)
    #/ET.ElementTree(gdml_pretty).write(filename, 'utf-8', True)
    print("GDML")
    #print(str(gdml))
    #ET.ElementTree(gdml).write(filename, 'utf-8', True)
    print("GDML file written")
