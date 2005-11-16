//  Copyright (C) 2004  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
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
//  See http://www.opencascade.org/SALOME/ or email : webmaster.salome@opencascade.org 
//
//
//
//  File   : FileTraceCollector.cxx
//  Author : Paul RASCLE (EDF)
//  Module : KERNEL
//  $Header$

#include <iostream>
#include <sstream>
#include <fstream>
#include <cstdlib>

using namespace std;

//#define _DEVDEBUG_
#include "FileTraceCollector.hxx"

// Class attributes initialisation, for class method FileTraceCollector::run

std::string FileTraceCollector::_fileName = "";

// ============================================================================
/*!
 *  This class is for use without CORBA, inside or outside SALOME.
 *  SALOME uses SALOMETraceCollector, to allow trace collection via CORBA.
 *  Type of trace (and corresponding class) is choosen in LocalTraceBufferPool.
 *
 *  Guarantees a unique object instance of the class (singleton thread safe)
 *  a separate thread for loop to print traces is launched.
 */
// ============================================================================

BaseTraceCollector* FileTraceCollector::instance(const char *fileName)
{
  if (_singleton == 0) // no need of lock when singleton already exists
    {
      int ret;
      ret = pthread_mutex_lock(&_singletonMutex); // acquire lock to be alone
      if (_singleton == 0)                     // another thread may have got
	{                                      // the lock after the first test
	  DEVTRACE("FileTraceCollector:: instance()");
	  BaseTraceCollector* myInstance = new FileTraceCollector();
	  _fileName = fileName;
	  DEVTRACE(" _fileName: " << _fileName);

	  sem_init(&_sem,0,0); // to wait until run thread is initialized
	  pthread_t traceThread;
	  int bid;
	  int re2 = pthread_create(&traceThread, NULL,
				   FileTraceCollector::run, (void *)bid);
	  sem_wait(&_sem);
	  _singleton = myInstance; // _singleton known only when init done
	  DEVTRACE("FileTraceCollector:: instance()-end");
	}
      ret = pthread_mutex_unlock(&_singletonMutex); // release lock
    }
  return _singleton;
}

// ============================================================================
/*!
 *  In a separate thread, loop to print traces.
 *  Mutex garantees intialisation on instance method is done and only one run
 *  allowed (double check ...)
 *  Loop until there is no more buffer to print,
 *  and no ask for end from destructor.
 *  Get a buffer. If type = ABORT then exit application with message.
 */
// ============================================================================

void* FileTraceCollector::run(void *bid)
{
  //DEVTRACE("init run");
  _threadId = new pthread_t;
  *_threadId = pthread_self();
  sem_post(&_sem); // unlock instance

  LocalTraceBufferPool* myTraceBuffer = LocalTraceBufferPool::instance();
  LocalTrace_TraceInfo myTrace;

  // --- opens a file with append mode
  //     so, several processes can share the same file

  ofstream traceFile;
  const char *theFileName = _fileName.c_str();
  DEVTRACE("try to open trace file "<< theFileName);
  traceFile.open(theFileName, ios::out | ios::app);
  if (!traceFile)
    {
      cerr << "impossible to open trace file "<< theFileName << endl;
      exit (1);
    }

  // --- Loop until there is no more buffer to print,
  //     and no ask for end from destructor.
  DEVTRACE("Begin loop");
  while ((!_threadToClose) || myTraceBuffer->toCollect() )
    {
      if (_threadToClose)
	{
	  DEVTRACE("FileTraceCollector _threadToClose");
	  //break;
	}

      int fullBuf = myTraceBuffer->retrieve(myTrace);
      if (myTrace.traceType == ABORT_MESS)
	{
#ifndef WNT
	  traceFile << "INTERRUPTION from thread " << myTrace.threadId
		    << " : " <<  myTrace.trace;
#else
	  traceFile << "INTERRUPTION from thread "
		    << (void*)(&myTrace.threadId)
		    << " : " <<  myTrace.trace;
#endif
	  traceFile.close();
	  cout << flush ;
#ifndef WNT
	  cerr << "INTERRUPTION from thread " << myTrace.threadId
	       << " : " <<  myTrace.trace;
#else
	  cerr << "INTERRUPTION from thread " << (void*)(&myTrace.threadId)
	       << " : " <<  myTrace.trace;
#endif
	  cerr << flush ; 
	  exit(1);     
	}
      else
	{
#ifndef WNT
	  traceFile << "th. " << myTrace.threadId
		    << " " << myTrace.trace;
#else
	  traceFile << "th. " << (void*)(&myTrace.threadId)
		    << " " << myTrace.trace;
#endif
	}
    }
  DEVTRACE("traceFile.close()");
  traceFile.close();
  DEVTRACE("traceFile.close()_end");
  pthread_exit(NULL);
}

// ============================================================================
/*!
 *  Destructor: wait until printing thread ends (FileTraceCollector::run)
 */
// ============================================================================

FileTraceCollector:: ~FileTraceCollector()
{
  int ret;
  ret = pthread_mutex_lock(&_singletonMutex); // acquire lock to be alone
  if (_singleton)
    {
      DEVTRACE("FileTraceCollector:: ~FileTraceCollector()");
      LocalTraceBufferPool* myTraceBuffer = LocalTraceBufferPool::instance();
      _threadToClose = 1;
      myTraceBuffer->insert(NORMAL_MESS,"end of trace\n"); // to wake up thread
      if (_threadId)
	{
	  int ret = pthread_join(*_threadId, NULL);
	  if (ret) cerr << "error close FileTraceCollector : "<< ret << endl;
	  else DEVTRACE("FileTraceCollector destruction OK");
	  _threadId = 0;
	  _threadToClose = 0;
	}
      _singleton = 0;
    }
  ret = pthread_mutex_unlock(&_singletonMutex); // release lock
}

// ============================================================================
/*!
 * Constructor: no need of LocalTraceBufferPool object initialization here,
 * thread safe singleton used in LocalTraceBufferPool::instance()
 */
// ============================================================================

FileTraceCollector::FileTraceCollector()
{
  _threadId=0;
  _threadToClose = 0;
}

