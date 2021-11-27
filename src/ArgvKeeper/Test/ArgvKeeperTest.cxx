// Copyright (C) 2007-2021  CEA/DEN, EDF R&D, OPEN CASCADE
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
//
// See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
//

#include "ArgvKeeperTest.hxx"
#include "ArgvKeeper.hxx"

#include <string>
#include <vector>

void ArgvKeeperUnitTests::TEST_argvKeeper()
{
  // args not set
  CPPUNIT_ASSERT_EQUAL(GetArgcArgv().size(), size_t(0));

  // args set
  std::vector<std::string> params = {"aaa", "bbb", "ccc"};
  SetArgcArgv(params);
  CPPUNIT_ASSERT_EQUAL(GetArgcArgv().size(), size_t(3));
  CPPUNIT_ASSERT_EQUAL(GetArgcArgv()[0], params[0]);
  CPPUNIT_ASSERT_EQUAL(GetArgcArgv()[1], params[1]);
  CPPUNIT_ASSERT_EQUAL(GetArgcArgv()[2], params[2]);
}
