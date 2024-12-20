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

# The only goal of this file is to put execution of ConfigureRPathPostEx.cmake script
# at the end of the installation process. This is necessary to ensure that
# all the targets are already installed and all the paths are set correctly.
# NOTE: Now this script fails because it can't get property from targets.

install(CODE "
include(${CMAKE_SOURCE_DIR}/ConfigureRPath.cmake)
configure_rpath_bytarget(${GLOBAL_TARGET_LIST})
")
