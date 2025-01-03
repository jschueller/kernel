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

# The only goal of this file is to run RPATH configuration on post install step.
# This is needed because the RPATH is not known until the installation is complete.

# Usage:
# Add after the install command for a target:
# install(CODE "
#     set(TARGET_FILE \"${SALOME_INSTALL_LIBS}/libSalomeContainer.so\")
#     set(MAX_RPATH_LENGTH 2000)
#     include(\"${CMAKE_SOURCE_DIR}/ConfigureRPathPostEx.cmake\")
# ")

# TODO: delete debug output after work is done.


include(CMakePrintHelpers)

if(NOT DEFINED TARGET_FILE)
    message(FATAL_ERROR "TARGET_FILE is not defined")
endif()

cmake_print_variables(TARGET_FILE)

get_filename_component(TARGET_FILE_ABS "${CMAKE_INSTALL_PREFIX}/${TARGET_FILE}" ABSOLUTE)
cmake_print_variables(TARGET_FILE_ABS)

# Read the RPATH using chrpath
execute_process(
    COMMAND chrpath -l ${TARGET_FILE_ABS}
    OUTPUT_VARIABLE chrpath_output
    RESULT_VARIABLE chrpath_result
)

cmake_print_variables(chrpath_output)
cmake_print_variables(chrpath_result)

# Check if RPATH exists
if(NOT chrpath_result EQUAL 0)
    message(STATUS "No RPATH found for ${TARGET_FILE_ABS}")
    return()
endif()

# Extract the RPATH
string(REGEX MATCH "(RPATH|RUNPATH)=[^\n]*" rpath_line "${chrpath_output}")
cmake_print_variables(rpath_line)
string(REPLACE "RPATH=" "" rpath_line "${rpath_line}")
string(REPLACE "RUNPATH=" "" old_rpath "${rpath_line}")
cmake_print_variables(old_rpath)

# Initialize new RPATH list
set(new_rpath "")

# Split the colon-separated list into individual elements
string(REPLACE ":" ";" old_rpath_list "${old_rpath}")

# Iterate over each path in the old RPATH
foreach(path IN LISTS old_rpath_list)
    cmake_print_variables(path)

    # Check if the path is a system path
    # TODO: make sure that this check covers all system paths
    list(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${path}" isSystemDir)
    if(NOT "${isSystemDir}" STREQUAL "-1" OR "${path}" MATCHES "^/usr/lib")
        #message(STATUS "Using system path as is: ${path}")
        list(APPEND new_rpath "${path}")
        continue()
    endif()
    
    string(LENGTH "${path}" cur_path_length)
    
    if(cur_path_length GREATER 0)
        # Ensure path is an absolute path
        get_filename_component(PATH_ABS ${path} ABSOLUTE)
        cmake_print_variables(PATH_ABS)
        
        # Compute the relative path using $ORIGIN
        file(RELATIVE_PATH relative_path ${TARGET_FILE_ABS} ${PATH_ABS})
        cmake_print_variables(relative_path)
        list(APPEND new_rpath "\$ORIGIN/${relative_path}")
    endif()
endforeach()

# Join the new RPATH list into a single string
string(REPLACE ";" ":" new_rpath_str "${new_rpath}")
message(STATUS "New RPATH: ${new_rpath}")

# Check the size of the new RPATH
string(LENGTH "${new_rpath_str}" new_rpath_length)
message(STATUS "New RPATH length: ${new_rpath_length}")

if(new_rpath_length GREATER MAX_RPATH_LENGTH)
    message(FATAL_ERROR "New RPATH length (${new_rpath_length}) exceeds the maximum allowed length (${MAX_RPATH_LENGTH})")
endif()

# Replace the old RPATH with the new RPATH using chrpath
execute_process(
    COMMAND chrpath -r ${new_rpath_str} ${TARGET_FILE_ABS}
    RESULT_VARIABLE chrpath_replace_result
)

if(NOT chrpath_replace_result EQUAL 0)
    message(FATAL_ERROR "Failed to replace RPATH for ${TARGET_FILE_ABS}")
endif()

message(STATUS "Successfully updated RPATH for ${TARGET_FILE_ABS}")
