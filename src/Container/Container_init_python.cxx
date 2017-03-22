// Copyright (C) 2007-2016  CEA/DEN, EDF R&D, OPEN CASCADE
//
// Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
// CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
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

#include <time.h>
#ifndef WIN32
  #include <sys/time.h>
#endif
#include <string>

#include "utilities.h"
#include "Container_init_python.hxx"

#if PY_VERSION_HEX < 0x03050000
static wchar_t*
Py_DecodeLocale(const char *arg, size_t *size)
{
    wchar_t *res;
    unsigned char *in;
    wchar_t *out;
    size_t argsize = strlen(arg) + 1;

    if (argsize > PY_SSIZE_T_MAX/sizeof(wchar_t))
        return NULL;
    res = (wchar_t*) PyMem_RawMalloc(argsize*sizeof(wchar_t));
    if (!res)
        return NULL;

    in = (unsigned char*)arg;
    out = res;
    while(*in)
        if(*in < 128)
            *out++ = *in++;
        else
            *out++ = 0xdc00 + *in++;
    *out = 0;
    if (size != NULL)
        *size = out - res;
    return res;
}
#endif

void KERNEL_PYTHON::init_python(int argc, char **argv)
{
  if (Py_IsInitialized())
    {
      MESSAGE("Python already initialized");
      return;
    }
  MESSAGE("=================================================================");
  MESSAGE("Python Initialization...");
  MESSAGE("=================================================================");
  // set stdout to line buffering (aka C++ std::cout)
  setvbuf(stdout, (char *)NULL, _IOLBF, BUFSIZ);
  wchar_t* salome_python;
  char* env_python=getenv("SALOME_PYTHON");
  if(env_python != 0)
    {
      wchar_t* salome_python = Py_DecodeLocale(env_python, NULL);
      Py_SetProgramName(salome_python);
    }
  Py_Initialize(); // Initialize the interpreter
  if (Py_IsInitialized())
    {
      MESSAGE("Python initialized eh eh eh");
    }
  wchar_t **changed_argv = new wchar_t*[argc]; // Setting arguments
  for (int i = 0; i < argc; i++)
  {
    changed_argv[i] = Py_DecodeLocale(argv[i], NULL);
  }
  PySys_SetArgv(argc, changed_argv);

  PyRun_SimpleString("import threading\n");
  // VSR (22/09/2016): This is a workaround to prevent invoking qFatal() from PyQt5
  // causing application aborting
  std::string script;
  script += "def _custom_except_hook(exc_type, exc_value, exc_traceback):\n";
  script += "  import sys\n";
  script += "  sys.__excepthook__(exc_type, exc_value, exc_traceback)\n";
  script += "  pass\n";
  script += "\n";
  script += "import sys\n";
  script += "sys.excepthook = _custom_except_hook\n";
  script += "del _custom_except_hook, sys\n";
  int res = PyRun_SimpleString(script.c_str());
  // VSR (22/09/2016): end of workaround
  PyEval_InitThreads(); // Create (and acquire) the interpreter lock
  PyThreadState *pts = PyGILState_GetThisThreadState(); 
  PyEval_ReleaseThread(pts);
  //delete[] changed_argv;
}

