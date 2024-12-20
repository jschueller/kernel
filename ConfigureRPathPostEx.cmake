# Copyright (C) 2012-2024  CEA, EDF, OPEN CASCADE
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

# The only goal of this file is to run RPATH configuration from custom command.
# NOTE: Now this script fails because it can't get property from targets.

include(${CMAKE_CURRENT_LIST_DIR}/ConfigureRPath.cmake)

# This is a space-separated string of all targets in the project
message(STATUS "all_targets in post build: ${all_targets}")
string(REPLACE " " ";" all_targets "${all_targets}")
message(STATUS "all_targets in post build after replacement: ${all_targets}")

configure_rpath_bytarget(${all_targets})