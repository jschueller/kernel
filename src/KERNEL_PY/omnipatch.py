"""
  This patch of omniORB is made to make it work with multiple interpreters
  and to correct the problem of incomplete import of CORBA packages
  in some situations common in SALOME

  This patch add or modify functions in omniORB module.

  In multiple interpreters context, omniORB module is meant to be shared among
  all interpreters
"""
import sys,string,imp
import omniORB
# Map of partially-opened modules
_partialModules = {}
# Map of modules to share
shared_imported={}

# Function to return a Python module for the required IDL module name
def openModule(mname, fname=None):
    # Salome modification start
    # Be sure to use the right module dictionnary
    import sys
    # Salome modification end

    if mname == "CORBA":
        mod = sys.modules["omniORB.CORBA"]

    elif sys.modules.has_key(mname):
        mod = sys.modules[mname]

        if _partialModules.has_key(mname):
            pmod = _partialModules[mname]
            mod.__dict__.update(pmod.__dict__)
            del _partialModules[mname]

    elif _partialModules.has_key(mname):
        mod = _partialModules[mname]

    else:
        mod = newModule(mname)

    # Salome modification start
    shared_imported[mname]=mod
    # Salome modification end

    if not hasattr(mod, "__doc__") or mod.__doc__ is None:
        mod.__doc__ = "omniORB IDL module " + mname + "\n\n" + \
                      "Generated from:\n\n"

    if fname is not None:
        mod.__doc__ = mod.__doc__ + "  " + fname + "\n"

    return mod

# Function to create a new module, and any parent modules which do not
# already exist
def newModule(mname):
    # Salome modification start
    # Be sure to use the right module dictionnary
    import sys
    # Salome modification end

    mlist   = string.split(mname, ".")
    current = ""
    mod     = None

    for name in mlist:
        current = current + name

        if sys.modules.has_key(current):
            mod = sys.modules[current]

        elif _partialModules.has_key(current):
            mod = _partialModules[current]

        else:
            newmod = imp.new_module(current)
            if mod: setattr(mod, name, newmod)
            _partialModules[current] = mod = newmod

        current = current + "."

    return mod

# Function to update a module with the partial module store in the
# partial module map
def updateModule(mname):
    if _partialModules.has_key(mname):
        pmod = _partialModules[mname]
        mod  = sys.modules[mname]
        mod.__dict__.update(pmod.__dict__)
        del _partialModules[mname]

omniORB.updateModule=updateModule
omniORB.newModule=newModule
omniORB.openModule=openModule
