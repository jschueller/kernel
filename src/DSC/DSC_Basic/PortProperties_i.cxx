//  Copyright (C) 2007-2008  CEA/DEN, EDF R&D, OPEN CASCADE
//
//  Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
//  CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
//
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either
//  version 2.1 of the License.
//
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
//
//  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
//
//  File   : PortProperties_i.cxx
//  Author : André RIBES (EDF)
//  Module : KERNEL
//
#include "PortProperties_i.hxx"

PortProperties_i::PortProperties_i() {}

PortProperties_i::~PortProperties_i() {}

void
PortProperties_i::set_property(const char * name, const CORBA::Any& value)
  throw (Ports::NotDefined, Ports::BadType)
{
  // Default case, the object has no properties.
  throw Ports::NotDefined();
}

CORBA::Any* 
PortProperties_i::get_property(const char* name)
  throw (Ports::NotDefined)
{
  // Default case, the object has no properties.
  throw Ports::NotDefined();
}
