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
// Modified by : $LastChangedBy$
// Date        : $LastChangedDate: 2007-03-01 13:40:26 +0100 (Thu, 01 Mar 2007) $
// Id          : $Id$
//
#ifndef _CALCIUM_PORT_PROVIDES_HXX_
#define _CALCIUM_PORT_PROVIDES_HXX_

#include <SALOMEconfig.h>

#include "Calcium_Ports.hh"
#include "CalciumGenericProvidesPort.hxx"
#include "CalciumCouplingPolicy.hxx"


CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_integer_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_Integer_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_long,CORBA::Long> ) \

CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_real_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_Real_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_float,CORBA::Float> ) \

CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_double_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_Double_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_double,CORBA::Double> ) \

CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_complex_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_Complex_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_float,CORBA::Float> ) \

CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_logical_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_Logical_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_boolean,CORBA::Boolean> ) \

CALCIUM_GENERIC_PROVIDES_PORT_HXX(calcium_string_port_provides,		\
			      POA_Ports::Calcium_Ports::Calcium_String_Port, \
			      seq_u_manipulation<Ports::Calcium_Ports::seq_string,char *> ) \

#endif