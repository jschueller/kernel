
#ifndef _NAMINGSERVICETEST_HXX_
#define _NAMINGSERVICETEST_HXX_

#include <cppunit/extensions/HelperMacros.h>
#include "SALOME_NamingService.hxx"

#include <SALOMEconfig.h>
#include CORBA_SERVER_HEADER(nstest)

class NSTEST_echo_i : public virtual POA_NSTEST::echo,
		      public virtual PortableServer::RefCountServantBase
{
public:
  NSTEST_echo_i();
  NSTEST_echo_i(CORBA::Long num);
  ~NSTEST_echo_i();
  CORBA::Long getId();
private:
  int _num;
};

class NSTEST_aFactory_i : public virtual POA_NSTEST::aFactory,
			  public virtual PortableServer::RefCountServantBase
{
public:
  NSTEST_aFactory_i();
  ~NSTEST_aFactory_i();
  NSTEST::echo_ptr createInstance();
private:
  int _num;
};

class NamingServiceTest : public CppUnit::TestFixture
{
  CPPUNIT_TEST_SUITE( NamingServiceTest );
  CPPUNIT_TEST( testConstructorDefault );
  CPPUNIT_TEST( testConstructorOrb );
  CPPUNIT_TEST( testRegisterResolveAbsNoPath );
  CPPUNIT_TEST( testRegisterResolveRelativeNoPath );
  CPPUNIT_TEST( testRegisterResolveAbsWithPath );
  CPPUNIT_TEST( testRegisterResolveRelativeWithPath );
  CPPUNIT_TEST( testResolveBadName );
  CPPUNIT_TEST( testResolveBadNameRelative );
  CPPUNIT_TEST( testResolveFirst );
  CPPUNIT_TEST( testResolveFirstRelative );
  CPPUNIT_TEST( testResolveFirstUnknown );
  CPPUNIT_TEST( testResolveFirstUnknownRelative );
  CPPUNIT_TEST( testResolveComponentOK );
  CPPUNIT_TEST( testResolveComponentEmptyHostname );
  CPPUNIT_TEST( testResolveComponentUnknownHostname );
  CPPUNIT_TEST( testResolveComponentEmptyContainerName );
  CPPUNIT_TEST( testResolveComponentUnknownContainerName );
  CPPUNIT_TEST( testResolveComponentEmptyComponentName );
  CPPUNIT_TEST( testResolveComponentUnknownComponentName );
  CPPUNIT_TEST( testResolveComponentFalseNbproc );
  CPPUNIT_TEST( testContainerName );
  CPPUNIT_TEST( testContainerNameParams );
  CPPUNIT_TEST( testBuildContainerNameForNS );
  CPPUNIT_TEST( testBuildContainerNameForNSParams );
  CPPUNIT_TEST( testFind );
  CPPUNIT_TEST( testCreateDirectory );
  CPPUNIT_TEST( testChangeDirectory );
  CPPUNIT_TEST( testCurrentDirectory );
  CPPUNIT_TEST( testList );
  CPPUNIT_TEST( testListDirectory );
  CPPUNIT_TEST( testListDirectoryRecurs );
  CPPUNIT_TEST( testListSubdirs );
  CPPUNIT_TEST( testDestroyName );
  CPPUNIT_TEST( testDestroyDirectory );
  CPPUNIT_TEST( testDestroyFullDirectory );
  CPPUNIT_TEST( testGetIorAddr );
//   CPPUNIT_TEST(  );
//   CPPUNIT_TEST(  );
//   CPPUNIT_TEST(  );

  CPPUNIT_TEST_SUITE_END();

public:

  void setUp();
  void tearDown();

  void testConstructorDefault();
  void testConstructorOrb();
  void testRegisterResolveAbsNoPath();
  void testRegisterResolveRelativeNoPath();
  void testRegisterResolveAbsWithPath();
  void testRegisterResolveRelativeWithPath();
  void testResolveBadName();
  void testResolveBadNameRelative();
  void testResolveFirst();
  void testResolveFirstRelative();
  void testResolveFirstUnknown();
  void testResolveFirstUnknownRelative();
  void testResolveComponentOK();
  void testResolveComponentEmptyHostname();
  void testResolveComponentUnknownHostname();
  void testResolveComponentEmptyContainerName();
  void testResolveComponentUnknownContainerName();
  void testResolveComponentEmptyComponentName();
  void testResolveComponentUnknownComponentName();
  void testResolveComponentFalseNbproc();
  void testContainerName();
  void testContainerNameParams();
  void testBuildContainerNameForNS();
  void testBuildContainerNameForNSParams();
  void testFind();
  void testCreateDirectory();
  void testChangeDirectory();
  void testCurrentDirectory();
  void testList();
  void testListDirectory();
  void testListDirectoryRecurs();
  void testListSubdirs();
  void testDestroyName();
  void testDestroyDirectory();
  void testDestroyFullDirectory();
  void testGetIorAddr();

protected:
  CORBA::ORB_var _orb;
  SALOME_NamingService _NS;

  PortableServer::POA_var _root_poa;
  PortableServer::POAManager_var _pman;
  PortableServer::ObjectId_var _myFactoryId;
  NSTEST_aFactory_i * _myFactory;
  CORBA::Object_var _factoryRef;
};

#endif