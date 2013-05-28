%define boost_version 1.32

Name:           CGAL
Version:        3.3.1
Release:        2%{?dist}
Summary:        Computational Geometry Algorithms Library

Group:          System Environment/Libraries
License:        QPL and LGPLv2 and LGPLv2+
URL:            http://www.cgal.org/
Source0:        ftp://ftp.mpi-sb.mpg.de/pub/outgoing/CGAL/%{name}-%{version}.tar.gz
Source10:       CGAL-README.Fedora
Patch1:         CGAL-install_cgal-SUPPORT_REQUIRED.patch
Patch2:         CGAL-3.3-build-library.patch
Patch4:         CGAL-3.2.1-install_cgal-no_versions_in_compiler_config.h.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Required devel packages.
BuildRequires: gmp-devel
BuildRequires: boost-devel >= %boost_version
BuildRequires: qt-devel >= 3.0
BuildConflicts:qt-devel < 4
BuildRequires: zlib-devel
BuildRequires: blas-devel lapack-devel
#%if 0%fedora > 7
BuildRequires: mpfr-devel
#%endif

# Required tools
BuildRequires: gawk

# for chmod in prep:
BuildRequires: coreutils

# CGAL-libs is renamed to CGAL.
Obsoletes:     %{name}-libs < %{version}-%{release}
Provides:      %{name}-libs = %{version}-%{release}

%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.


%package devel
Group:          Development/Libraries
Summary:        Development files and tools for CGAL applications
Requires:       %{name} = %{version}-%{release}
Requires:       boost-devel >= %{boost_version}
Requires:       blas-devel lapack-devel qt-devel zlib-devel gmp-devel
Requires:       %{_sysconfdir}/profile.d
%description devel
The %{name}-devel package provides the headers files and tools you may need to 
develop applications using CGAL.


%package demos-source
Group:          Documentation
Summary:        Examples and demos of CGAL algorithms
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-demo < %{version}-%{release}
Provides:       %{name}-demo = %{version}-%{release}
%description demos-source
The %{name}-demos-source package provides the sources of examples and demos of
CGAL algorithms.


%prep
%setup -q 

%patch1 -p0 -b .support-required.bak
%patch2 -p1 -b .build-library.bak

%patch4 -p1 -b .no_versions.bak

chmod a-x examples/Nef_3/handling_double_coordinates.cin



# fix end-of-lines of several files
sed -i 's/\r//' \
    examples/Surface_mesh_parameterization/data/mask_cone.off \
    examples/Boolean_set_operations_2/test.dxf

for f in demo/Straight_skeleton_2/data/vertex_event_9.poly \
         demo/Straight_skeleton_2/data/vertex_event_0.poly;
do
  [ -r $f ] && sed -i 's/\r//' $f;
done

# Install README.Fedora here, to include it in %doc
install -m 644 %{SOURCE10} ./README.Fedora

%build
#export QTDIR=%{_prefix}
source %{_sysconfdir}/profile.d/qt.sh

./install_cgal -ni g++ --CUSTOM_CXXFLAGS "$RPM_OPT_FLAGS" \
               --without-autofind \
               --with-ZLIB \
               --with-BOOST \
               --with-BOOST_PROGRAM_OPTIONS \
               --with-X11 \
               --with-GMP \
               --with-GMPXX \
               --with-MPFR \
               --with-QT3MT \
               --with-REFBLASSHARED \
               --with-DEFAULTLAPACK \
               --with-OPENGL \
               --disable-static


%install
rm -rf %{buildroot}

# Install headers
mkdir -p %{buildroot}%{_includedir}
cp -a include/* %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_includedir}/CGAL/config/msvc*
mv %{buildroot}%{_includedir}/CGAL/config/*/CGAL/compiler_config.h %{buildroot}%{_includedir}/CGAL/
rm -rf %{buildroot}%{_includedir}/CGAL/config

# Install scripts (only those prefixed with "cgal_").
mkdir -p %{buildroot}%{_bindir}
cp -a scripts/cgal_* %{buildroot}%{_bindir}

# Install libraries
mkdir -p %{buildroot}%{_libdir}
cp -a lib/*/lib* %{buildroot}%{_libdir}

# Install makefile:
mkdir -p %{buildroot}%{_datadir}/CGAL
touch -r make %{buildroot}%{_datadir}/CGAL
cp -p make/makefile_* %{buildroot}%{_datadir}/CGAL/cgal.mk

# Install demos and examples
mkdir -p %{buildroot}%{_datadir}/CGAL/
touch -r demo %{buildroot}%{_datadir}/CGAL/
cp -a demo %{buildroot}%{_datadir}/CGAL/demo
cp -a examples %{buildroot}%{_datadir}/CGAL/examples

# Modify makefile
cat > makefile.sed <<'EOF'
s,CGAL_INCL_DIR *=.*,CGAL_INCL_DIR = %{_includedir},;
s,CGAL_LIB_DIR *=.*,CGAL_LIB_DIR = %{_libdir},;
/CUSTOM_CXXFLAGS/ s/-O2 //;
/CUSTOM_CXXFLAGS/ s/-g //;
/CGAL_INCL_DIR/ s,/CGAL/config/.*,,;
s,/$(CGAL_OS_COMPILER),,g;
/-I.*CGAL_INCL_CONF_DIR/ d
EOF

sed -i -f makefile.sed %{buildroot}%{_datadir}/CGAL/cgal.mk

# check if the sed script above has worked:
grep -q %{_builddir} %{buildroot}%{_datadir}/CGAL/cgal.mk && false
grep -q %{buildroot} %{buildroot}%{_datadir}/CGAL/cgal.mk && false
grep -q CGAL/config %{buildroot}%{_datadir}/CGAL/cgal.mk && false
grep -q -E 'CUSTOM_CXXFLAGS.*(-O2|-g)' %{buildroot}%{_datadir}/CGAL/cgal.mk && false

# Remove -L and -R flags from the makefile
cat > makefile-noprefix.sed <<'EOF'
/'-L$(CGAL_LIB_DIR)'/ d;
/-R$(CGAL_LIB_DIR)/ d;
/'-I$(CGAL_INCL_DIR)'/ d;
EOF

sed -i -f makefile-noprefix.sed  %{buildroot}%{_datadir}/CGAL/cgal.mk

# check that the sed script has worked
grep -q -E -- '-[LI]\$' %{buildroot}%{_datadir}/CGAL/cgal.mk && false
grep -q -E -- '-R' %{buildroot}%{_datadir}/CGAL/cgal.mk && false


# Create %{_sysconfdir}/profile.d/ scripts
cd %{buildroot}
mkdir -p .%{_sysconfdir}/profile.d
cat > .%{_sysconfdir}/profile.d/cgal.sh <<EOF
if [ -z "\$CGAL_MAKEFILE" ] ; then
  CGAL_MAKEFILE="%{_datadir}/CGAL/cgal.mk"
  export CGAL_MAKEFILE
fi
EOF

cat > .%{_sysconfdir}/profile.d/cgal.csh <<EOF
if ( ! \$?CGAL_MAKEFILE ) then
  setenv CGAL_MAKEFILE "%{_datadir}/CGAL/cgal.mk"
endif
EOF
chmod 644 .%{_sysconfdir}/profile.d/cgal.*sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL LICENSE.QPL CHANGES README.Fedora
%{_libdir}/libCGAL*.so.2
%{_libdir}/libCGAL*.so.2.0.1


%files devel
%defattr(-,root,root,-)
%{_includedir}/CGAL
%{_libdir}/libCGAL*.so
%dir %{_datadir}/CGAL
%{_datadir}/CGAL/cgal.mk
%{_bindir}/*
%exclude %{_bindir}/cgal_make_macosx_app
%config(noreplace) %{_sysconfdir}/profile.d/cgal.*


%files demos-source
%defattr(-,root,root,-)
%dir %{_datadir}/CGAL
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/*.vcproj
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation


%changelog
* Mon Sep  3 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-2%{dist}
- Fix soversion.

* Mon Sep  3 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-1%{dist}
- New upstream bug-fixes release.

* Fri Aug 24 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-7%{dist}
- Add BR: mpfr since F-8.

* Fri Aug 24 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-6%{dist}
- Add BR: gawk

* Thu Aug 23 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-5%{dist}
- License: tag fixed.

* Thu Jun  7 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-4%{?dist}
- Move the makefile back to %%{_datadir}/CGAL, and rename it cgal.mk (sync
  with Debian package). That file is not a config file, but just an example
  .mk file that can be copied and adapted by users.
- Fix the %%{_sysconfdir}/profile.d/cgal.* files (the csh one was buggy).
- CGAL-devel now requires all its dependancies.

* Sat Jun  2 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-2%{?dist}
- Officiel CGAL-3.3 release
- Skip file named "skip_vcproj_auto_generation"

* Wed May 30 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-0.1.RC1%{?dist}
- New upstream version: 3.3-RC1
- Obsolete patches CGAL-3.2.1-build-libCGALQt-shared.patch,
                   CGAL-3.2.1-build-no-static-lib.patch,
                   CGAL-3.2.1-config.h-endianness_detection.patch.
  These patchs have been merged and adapted by upstream.
- New option --disable-static
- Shipped OpenNL and CORE have been renamed by upstream:
    - %%{_includedir}/OpenNL is now %{_includedir}/CGAL/OpenNL
    - %%{_includedir}/CORE is now %{_includedir}/CGAL/CORE
    - libCORE has been rename libCGALcore++
  Reasons:
    - CGAL/OpenNL is a special version of OpenNL, rewritten for CGAL 
      in C++ by the OpenNL author,
    - CGAL/CORE is a fork of CORE-1.7. CORE-1.7 is no longer maintained by 
      its authors, and CORE-2.0 is awaited since 2004.
  In previous releases of this package, CORE was excluded from the package, 
  because %%{_includedir}/CORE/ was a name too generic (see comment #8 of
  #bug #199168). Since the headers of CORE have been moved to
  %%{_includedir}/CGAL/CORE, CORE is now shipped with CGAL.
- move %%{_datadir}/CGAL/make/makefile to %%{_sysconfdir}/CGAL/makefile
(because it is a config file).

* Thu Nov  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-19
- Fix CGAL-3.2.1-build-libCGALQt-shared.patch (bug #213675)

* Fri Sep 15 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-18
- Move LICENSE.OPENNL to %%doc CGAL-devel (bug #206575).

* Mon Sep 11 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-17
- libCGALQt.so needs -lGL
- remove %%{_bindir}/cgal_make_macosx_app

* Sat Sep  11 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-16
- Remove CORE support. Its acceptance in Fedora is controversial (bug #199168).
- Exclude .vcproj files from the -demos-source subpackage.
- Added a patch to build *shared* library libCGALQt.
- Added a patch to avoid building static libraries.
- Fixed the License: tag.

* Thu Aug 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-15
- Change the permissions of %%{_sysconfdir}/profile.d/cgal.*sh
- Remove the meta package CGAL. CGAL-libs is renamed CGAL.
- Added two patchs:
  - CGAL-3.2.1-config.h-endianness_detection.patch which is an upstream patch
    to fix the endianness detection, so that is is no longer hard-coded in
    <CGAL/compiler_config.h>,
  - CGAL-3.2.1-install_cgal-no_versions_in_compiler_config.h.patch that
    removes hard-coded versions in <CGAL/compiler_config.h>.

* Wed Aug 16 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-14
- Simplified spec file, for Fedora Extras.

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-13
- Change CGAL-README.Fedora, now that Installation.pdf is no longer in the
tarball.

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-12
- Remove unneeded  -R/-L/-I flags from %%{_datadir}/CGAL/make/makefile

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-11
- Fix the soversion.
- Fix %%{cgal_prefix} stuff!!
- Quote 'EOF', so that the lines are not expanded by the shell.

* Tue Jul  4 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-10
- Fix makefile.sed so that %%{buildroot} does not appear in 
  %%{_datadir}/CGAL/make/makefile.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-9
- Remove Obsoletes: in the meta-package CGAL.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-8
- Fix the localisation of demo and examples.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-6
- Set Requires, in sub-packages.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-5
- CGAL-3.2.1
- Sub-package "demo" is now named "demos-source" (Fedora guidelines).
- Fix some rpmlint warnings
- Added README.Fedora, to explain why the documentation is not shipped, and how CGAL is divided in sub-packages.


* Sat Jul  1 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-4
- Use %%{_datadir}/CGAL instead of %%{_datadir}/%%{name}-%%{version}
- Fix %%{_datadir}/CGAL/makefile, with a sed script.
- Added a new option %%set_prefix (see top of spec file).

* Sat Jul  1 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-3
- Use less "*" in %%files, to avoid futur surprises.
- Remove %%{_sysconfdir}/profile.d/cgal.* from %%files if %%cgal_prefix is not empty.
- Fix %%build_doc=0 when %%fedora is set. New option macro: %%force_build_doc.

* Fri Jun 30 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-2
- Fix some end-of-lines in %%prep, to please rpmlint.

* Mon May 22 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-1
- Remove README from %%doc file: it describes the tarball layout.
- Updated to CGAL-3.2.
- Added examples in the -demo subpackage.
- Cleaning up, to follow Fedora Guidelines.
- The -doc subpackage cannot be build on Fedora (no license).
- Add ldconfig back.
- No prefix.

* Fri Apr 28 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.447
- Update to CGAL-3.2-447.

* Fri Apr 21 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.440
- Updated to CGAL-3.2-I-440.

* Wed Apr 19 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.438
- Added a patch to install_cgal, to require support for BOOST, BOOST_PROGRAM_OPTIONS, X11, GMP, MPFR, GMPXX, CORE, ZLIB, and QT.
- Move scripts to %%{_bindir}
- %%{_libdir}/CGAL-I now belong to CGAL and CGAL-devel, so that it disappears when the packages are removed.

* Wed Apr 12 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.431
- Updated to CGAL-3.2-I-431.
- Remove the use of ldconfig.
- Changed my email address.
- No longer need for patch0.
- Pass of rpmlint.
- Remove unneeded Requires: tags (rpm find them itself).
- Change the release tag.
- Added comments at the beginning of the file.
- Added custom ld flags, on 64bits archs (so that X11 is detected).

* Tue Apr 11 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org>
- Removed -g and -O2 from CUSTOM_CXXFLAGS, in the makefile only.
  They are kept during the compilation of libraries.
- Added zlib in dependencies.
- Added a patch to test_ZLIB.C, until it is merged upstream.

* Fri Mar 31 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- adding a test in the setup section.

* Mon Mar 13 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- delete the patch that fixes the perl path.
- add build_doc and build_demo flags.

* Fri Mar 10 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- Adding new sub-packages doc(pdf&html) and demo.
- Add internal_release flag. 

* Thu Mar 09 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- Cleanup a specfile.

