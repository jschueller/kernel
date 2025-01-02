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

# An updated example from cmake documentation at:
# https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling#default-rpath-settings
#
# NOTE: RUNPATH is preferred over RPATH on platforms where RUNPATH is supported,
# so CMake appears to be setting RUNPATH whenever we use its RPATH functionality.
# It's a reason why we need to check RUNPATH section in the ELF to check if the RPATH is set correctly.
# An example of how to check the RPATH in the ELF:
# readelf -d /path/to/your/library.so | grep 'RPATH\|RUNPATH'
# or
# objdump -x /path/to/your/library.so | grep 'RPATH\|RUNPATH'


# Define the maximum RPATH length variable with a default value
set(MAX_RPATH_LENGTH 2000 CACHE STRING "Maximum allowed length for RPATH")


###########################################################
# Collect all targets in the project

function(get_all_targets var)
    message(STATUS "Collecting all targets...")
    message(STATUS "Current binary directory: ${CMAKE_BINARY_DIR}")

    set(targets)
    # get_all_targets_recursive(targets ${CMAKE_CURRENT_SOURCE_DIR})
    get_all_targets_recursive(targets ${CMAKE_CURRENT_BINARY_DIR})
    # get_all_targets_recursive(targets ${CMAKE_BINARY_DIR})
    set(${var} ${targets} PARENT_SCOPE)

    message(STATUS "All targets: ${targets}")
endfunction()

macro(get_all_targets_recursive targets dir)
    message(STATUS "Collecting targets in directory: ${dir}")
    if(NOT EXISTS ${dir})
        message(STATUS "Directory does not exist: ${dir}")
        return()
    endif()

    # Check if the directory has been processed by CMake
    if(NOT EXISTS "${dir}/CMakeFiles")
        message(STATUS "Directory ${dir} has not been processed by CMake yet.")
        # return()
    endif()

    get_property(subdirectories DIRECTORY ${dir} PROPERTY SUBDIRECTORIES)
    # get_directory_property(subdirectories ${dir} PROPERTY SUBDIRECTORIES)
    message(STATUS "Subdirectories: ${subdirectories}")
    foreach(subdir ${subdirectories})
        get_all_targets_recursive(${targets} ${subdir})
    endforeach()

    get_property(current_targets DIRECTORY ${dir} PROPERTY BUILDSYSTEM_TARGETS)
    # get_directory_property(current_targets ${dir} PROPERTY BUILDSYSTEM_TARGETS)
    message(STATUS "Current targets: ${current_targets}")
    list(APPEND ${targets} ${current_targets})
endmacro()


###########################################################
# Collect RPATH directories for a target

# This location will be used to make the RPATH relative to the target binary directory
function(get_lib_location lib lib_location)

    get_target_property(is_imported ${lib} IMPORTED)
    message(STATUS "Library ${lib} is imported: ${is_imported}")

    if(is_imported)
        # Use IMPORTED_LOCATION for imported targets
        get_target_property(lib_location ${lib} IMPORTED_LOCATION)
        set(lib_location ${lib_location} PARENT_SCOPE)
    else()
        # Use generator expressions for non-imported targets
        get_target_property(lib_type ${lib} TYPE)
        message(STATUS "Library type: ${lib_type}")

        if(lib_type STREQUAL "EXECUTABLE" OR
           lib_type STREQUAL "STATIC_LIBRARY" OR
           lib_type STREQUAL "SHARED_LIBRARY" OR
           lib_type STREQUAL "MODULE_LIBRARY")
            # set(lib_location $<TARGET_FILE:${lib}> PARENT_SCOPE)
            # set(lib_location "$<TARGET_FILE:${lib}>" PARENT_SCOPE)
            get_property(lib_location TARGET ${lib} PROPERTY LOCATION)
            set(lib_location ${lib_location} PARENT_SCOPE)
            message(STATUS "Supported lib type, location: ${lib_location}")
        else()
            message(STATUS "Unsupported target type: ${lib_type}")
            return()
        endif()
    endif()

    message(STATUS "Library location: ${lib_location}")
endfunction()

# Function to make the RPATH relative to the target binary directory
function(make_relative_path lib_location target_binary_dir out_rpath_dirs)
    message(STATUS "Making relative path for library location: ${lib_location}")

    get_filename_component(lib_dir ${lib_location} DIRECTORY)
    message(STATUS "Library directory: ${lib_dir}")

    set(rpath_dirs ${${out_rpath_dirs}})

    # Check if the directory is a system directory because we don't want to add them to RPATH
    list(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${lib_dir}" isSystemDir)
    if("${isSystemDir}" STREQUAL "-1")
        # Check if the directory is inside the build tree
        if(${lib_dir} MATCHES "^${CMAKE_BINARY_DIR}")
            message(STATUS "Converting absolute path to relative path using $ORIGIN")

            file(RELATIVE_PATH rel_path "${target_binary_dir}" "${lib_dir}")
            list(APPEND rpath_dirs "\$ORIGIN/${rel_path}")
        else()
            message(STATUS "Library directory is outside the build tree: ${lib_dir}")
            list(APPEND rpath_dirs "${lib_dir}")
        endif()
    else()
        message(STATUS "Library directory is a system directory: ${lib_dir}")
    endif()

    # Return the modified rpath_dirs
    set(${out_rpath_dirs} ${rpath_dirs} PARENT_SCOPE)

    message(STATUS "RPATH directories after making relative paths: ${rpath_dirs}")
endfunction()


# Function to collect RPATH directories for a target
function(collect_rpath_dirs target target_binary_dir result)
    # Collect all linked libraries
    get_target_property(libs ${target} LINK_LIBRARIES)
    message(STATUS "Linked libraries for target ${target}: ${libs}")

    set(collected_dirs "")
    foreach(lib ${libs})
        if(NOT TARGET ${lib})
            message(STATUS "Library ${lib} is not a target")
            continue()
        endif()

        get_lib_location(${lib} lib_location)
        if(NOT lib_location)
            continue()
        endif()

        make_relative_path(${lib_location} ${target_binary_dir} collected_dirs)
    endforeach()

    # Remove duplicates
    list(REMOVE_DUPLICATES collected_dirs)

    # Return the collected RPATH directories
    set(${result} ${collected_dirs} PARENT_SCOPE)
    message(STATUS "RPATH directories for target ${target}: ${collected_dirs}")
endfunction()


###########################################################
# Set RPATH directories for a target

# Function to set RPATH for a target
function(set_rpath target rpath_dirs)
    message(STATUS "Setting RPATH for target ${target}: ${rpath_dirs}")
    if(NOT rpath_dirs)
        message(STATUS "No RPATH directories found for target ${target}")
        return()
    endif()

    # Print the RPATH for debugging purposes
    get_target_property(rpath_property ${target} INSTALL_RPATH)
    message(STATUS "Before RPATH for target ${target}: ${rpath_property}")

    # Set the combined RPATH for the target
    set_target_properties(${target} PROPERTIES INSTALL_RPATH "${rpath_dirs}")

    # Print the RPATH for debugging purposes
    get_target_property(rpath_property ${target} INSTALL_RPATH)
    message(STATUS "After RPATH for target ${target}: ${rpath_property}")

    # Check the total length of the RPATH
    string(LENGTH "${rpath_property}" RPATH_LENGTH)
    message(STATUS "Total length of the RPATH for target ${target}: ${RPATH_LENGTH} bytes")
    if(RPATH_LENGTH GREATER ${MAX_RPATH_LENGTH})
        message(FATAL_ERROR "The total length of the RPATH for target ${target} exceeds ${MAX_RPATH_LENGTH} bytes: ${RPATH_LENGTH} bytes")
    endif()
endfunction()


# Function to determine dependencies and set RPATH with relative paths
function(configure_target_rpath target)
    message(STATUS "Configuring RPATH for target ${target}...")

    get_target_property(target_type ${target} TYPE)
    if(NOT target_type)
        return()
    endif()

    # Get the binary directory for the target
    get_target_property(target_binary_dir ${target} RUNTIME_OUTPUT_DIRECTORY)
    if(NOT target_binary_dir)
        get_target_property(target_binary_dir ${target} LIBRARY_OUTPUT_DIRECTORY)
    endif()
    if(NOT target_binary_dir)
        set(target_binary_dir ${CMAKE_CURRENT_BINARY_DIR})
    endif()

    # Collect RPATH directories
    collect_rpath_dirs(${target} ${target_binary_dir} rpath_dirs)
    message(STATUS "Collected RPATH directories in parent scope for target ${target}: ${rpath_dirs}")

    # Set RPATH for the target
    set_rpath(${target} "${rpath_dirs}")
endfunction()

# This CMake script sets the RPATH (runtime library search path) for each target individually.
# 
# RPATH is used to specify the directories where the runtime linker should look for shared libraries.
# Setting RPATH individually for each target ensures that each target can have its own specific
# library search paths, which can be useful in complex projects where different targets may depend
# on different versions of the same library or on libraries located in different directories.
# 
# Note: Setting RPATH globally can lead to conflicts and unintended behavior if different targets
# require different library search paths. By setting RPATH individually, we avoid these potential
# issues and maintain better control over the runtime environment of each target.
# function(configure_rpath_bytarget all_targets)
function(configure_rpath_bytarget)
    message(STATUS "Configuring RPATH for all targets...")

    # Set global RPATH settings:
    # Do not use the install RPATH when running executables from the build directory.
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

    # when building, don't use the install RPATH already
    # (but later on when installing)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

    # Add directories to the install RPATH that are outside the project but are needed for linking.
    # Turned off to have an ability to check the total size of the RPATH,
    # because this options adds all paths on the install phase.
    # set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

    # Collect all targets in the project
    get_all_targets(all_targets)

    # Configure RPATH for each target
    foreach(target ${all_targets})
        configure_target_rpath(${target})
    endforeach()

    message(STATUS "RPATH configuration completed.")
endfunction()

# Configure the same RPATH for all targets in the project,
# except part of RPATH that is set automatically by CMake.
macro(configure_rpath)
    # RPATH settings:
    # use, i.e. don't skip the full RPATH for the build tree
    set(CMAKE_SKIP_BUILD_RPATH FALSE)

    # when building, don't use the install RPATH already
    # (but later on when installing)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

    # add the automatically determined parts of the RPATH
    # which point to directories outside the build tree to the install RPATH
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

    # Initialize the BUILD_RPATH_USE_ORIGIN target property for all targets
    # set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)

    # the RPATH to be used when installing, but only if it's not a system directory
    # list(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
    # if("${isSystemDir}" STREQUAL "-1")
    #     # $ORIGIN/../../../../../lib/salome
    #     set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib/salome")
    # endif()

    # message(STATUS "Updated CMAKE_INSTALL_RPATH: ${CMAKE_INSTALL_RPATH}")

    # # Check the total length of the RPATH
    # string(LENGTH "${CMAKE_INSTALL_RPATH}" RPATH_LENGTH)
    # message(STATUS "Total length of the RPATH: ${RPATH_LENGTH} bytes")
    # if(RPATH_LENGTH GREATER ${MAX_RPATH_LENGTH})
    #     message(FATAL_ERROR "The total length of the RPATH exceeds ${MAX_RPATH_LENGTH} bytes: ${RPATH_LENGTH} bytes")
    # endif()
endmacro()
