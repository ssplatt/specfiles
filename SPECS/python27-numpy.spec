%global  __python27 /usr/bin/python2.7
%global python27_sitearch %{_libdir}/python2.7/site-packages

# Fix byte-compilation:
%define __os_install_post %{__python27_os_install_post}

Name:           python27-numpy
Version:        1.7.1
Release:        1%{?dist}
Summary:        A fast multi-dimensional array facility for Python

Group:          Development/Languages

#The majority of numpy is BSD however:
#numpy/core/_mx_datetime_parser.py includes eGenix public license 1.1.0.
#which is based on the Python license.
#numpy/lib/utils.py contains a SafeEval class which carries the Python license.
#numpy/random/mtrand/{distributions.c,distributions.h,mtrand.pyx,randomkit.h}
#carry MIT licenses.
#numpy/random/mtrand/randomkit.c is a mixture of BSD and MIT licenses.
License:        BSD and Python and MIT and eGenix
URL:            http://numeric.scipy.org/
Source0:        http://downloads.sourceforge.net/numpy/numpy-%{version}.tar.gz
Patch0:         numpy-1.0.1-f2py.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python27-devel
BuildRequires:  gcc-gfortran 
BuildRequires:  atlas-devel python27-nose
Requires:       python(abi) = 2.7
Requires:       atlas

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package devel
Summary:        Header files for creating C extension to Numpy
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
#Requires:       python27-distribute 
Requires:       python27-devel

%description devel
The NumPy-devel package contains header files for creating C module
extensions that can be loaded within python.

%package tests
Summary:        Tests for Numpy distribute
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python27-nose

%description tests
The NumPy-tests package contains tests for checking your
numpy installation. Install this package to allow the
following to work.

python2.7 -c "import pkg_resources, numpy ; numpy.test()"

%package f2py
Summary:        FORTRAN for python interface for numpy
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python27-devel

%description f2py
This package includes a version of f2py that works properly with NumPy.

%package f2py-tests
Summary:        Test suite for FORTRAN for python interface for numpy
Group:          Development/Libraries
Requires:       %{name}-f2py = %{version}-%{release}
Requires:       python27-devel
Requires:       %{name} = %{version}-%{release}

%description f2py-tests
This package includes a test suite for a  version of f2py that works 
properly with NumPy.

%prep
%setup -q -n numpy-%{version}
%patch0 -p1 -b .f2py
# Adapt everything to use a particular python variant.
find . -name '*.py' | xargs sed -i '1s|^#!%{_bindir}.*python$|#!%{__python27}|'
sed -i 's|#!%{_bindir}/env %s|#!%{_bindir}/%s|' numpy/f2py/setup.py \
                                          numpy/f2py/setupscons.py

# Make some files utf8.
for I in FAQ.txt THANKS.txt HISTORY.txt README.txt ; do
  iconv -f iso8859-1 -t utf-8 numpy/f2py/docs/$I > $I.conv && mv -f $I.conv numpy/f2py/docs/$I
done

# Fix the man page.
sed -i 's/TH "F2PY" 1/TH "F2PY27" 1/' numpy/f2py/f2py.1
sed -i 's/ f2py/ f2py2.7/g'            numpy/f2py/f2py.1

%build
# Build with fno-strict-aliasing due to warnings that 
# code breaks strict aliasing rules rhbz#619355.
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
    %{__python27} setup.py build

%install
rm -rf %{buildroot}
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
   %{__python27} setup.py install --root %{buildroot}
rm -rf docs-f2py ; mv %{buildroot}%{python27_sitearch}/numpy/f2py/docs docs-f2py
mv -f %{buildroot}%{python27_sitearch}/numpy/f2py/f2py.1 f2py.1
rm -rf doc ; mv -f %{buildroot}%{python27_sitearch}/numpy/doc .
install -D -p -m 0644 f2py.1 %{buildroot}%{_mandir}/man1/f2py2.7.1

#symlink for includes, BZ 185079
mkdir -p %{buildroot}/usr/include
ln -s %{python27_sitearch}/numpy/core/include/numpy/ %{buildroot}/usr/include/python27-numpy

# Remove doc files. They should be in %%doc
rm -f %{buildroot}%{python27_sitearch}/numpy/COMPATIBILITY
rm -f %{buildroot}%{python27_sitearch}/numpy/DEV_README.txt
rm -f %{buildroot}%{python27_sitearch}/numpy/INSTALL.txt
rm -f %{buildroot}%{python27_sitearch}/numpy/LICENSE.txt
rm -f %{buildroot}%{python27_sitearch}/numpy/README.txt
rm -f %{buildroot}%{python27_sitearch}/numpy/THANKS.txt
rm -f %{buildroot}%{python27_sitearch}/numpy/site.cfg.example

# Remove some hash bangs from libs that don't need to be there.
find %{buildroot}%{python27_sitearch} -name '*.py' |
   xargs sed -i '1s|#!%{__python27}||'

# Set correct permissions on .so files.
find %{buildroot}%{python27_sitearch} -name '*.so' |
   xargs chmod 755

# Some more dodgy #!s where there are not needed.
sed -i '1s|#!.*||' %{buildroot}%{python27_sitearch}/numpy/core/scons_support.py \
                   %{buildroot}%{python27_sitearch}/numpy/ma/bench.py \
                   %{buildroot}%{python27_sitearch}/numpy/distutils/system_info.py

%check
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python27_sitearch}" %{__python27} -c "import pkg_resources, numpy ; numpy.test()"
popd &> /dev/null

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/* LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%dir %{python27_sitearch}/numpy
%{python27_sitearch}/numpy/*.py*
%dir %{python27_sitearch}/numpy/core/
%{python27_sitearch}/numpy/core/*.py*
%{python27_sitearch}/numpy/core/*.so
%dir %{python27_sitearch}/numpy/numarray
%{python27_sitearch}/numpy/numarray/*.py*
%{python27_sitearch}/numpy/numarray/*.so
%dir %{python27_sitearch}/numpy/fft/
%{python27_sitearch}/numpy/fft/*.py*
%{python27_sitearch}/numpy/fft/*.so
%dir %{python27_sitearch}/numpy/lib/
%{python27_sitearch}/numpy/lib/*.py* 
%{python27_sitearch}/numpy/lib/*.so
%dir %{python27_sitearch}/numpy/lib/benchmarks/
%{python27_sitearch}/numpy/lib/benchmarks/*.py*
%dir %{python27_sitearch}/numpy/linalg/
%{python27_sitearch}/numpy/linalg/*.py*
%{python27_sitearch}/numpy/linalg/*.so
%dir %{python27_sitearch}/numpy/ma/
%{python27_sitearch}/numpy/ma/*.py*
%dir %{python27_sitearch}/numpy/oldnumeric/
%{python27_sitearch}/numpy/oldnumeric/*.py*
%dir %{python27_sitearch}/numpy/random/
%{python27_sitearch}/numpy/random/*.py*
%{python27_sitearch}/numpy/random/*.so
%dir %{python27_sitearch}/numpy/testing/
%{python27_sitearch}/numpy/testing/*.py*
%dir %{python27_sitearch}/numpy/tools/
%{python27_sitearch}/numpy/tools/*.py*
%dir %{python27_sitearch}/numpy/compat/
%{python27_sitearch}/numpy/compat/*.py*
%dir %{python27_sitearch}/numpy/matrixlib/
%{python27_sitearch}/numpy/matrixlib/*.py*
%dir %{python27_sitearch}/numpy/polynomial/
%{python27_sitearch}/numpy/polynomial/*.py*
%{python27_sitearch}/numpy-*.egg-info

%files tests
%defattr(-,root,root,-)
%dir %{python27_sitearch}/numpy/core/tests/
%{python27_sitearch}/numpy/core/tests/*.py*
%{python27_sitearch}/numpy/core/tests/data/
%dir %{python27_sitearch}/numpy/fft/tests/
%{python27_sitearch}/numpy/fft/tests/*.py*
%dir %{python27_sitearch}/numpy/lib/tests/
%{python27_sitearch}/numpy/lib/tests/*.py*
%dir %{python27_sitearch}/numpy/linalg/tests/
%{python27_sitearch}/numpy/linalg/tests/*.py*
%dir %{python27_sitearch}/numpy/ma/tests/
%{python27_sitearch}/numpy/ma/tests/*.py*
%dir %{python27_sitearch}/numpy/oldnumeric/tests/
%{python27_sitearch}/numpy/oldnumeric/tests/*.py*
%dir %{python27_sitearch}/numpy/random/tests/
%{python27_sitearch}/numpy/random/tests/*.py*
%dir %{python27_sitearch}/numpy/testing/tests/
%{python27_sitearch}/numpy/testing/tests/*.py*
%dir %{python27_sitearch}/numpy/tests/
%{python27_sitearch}/numpy/tests/*.py*
%dir %{python27_sitearch}/numpy/matrixlib/tests
%{python27_sitearch}/numpy/matrixlib/tests/*.py*
%dir %{python27_sitearch}/numpy/polynomial/tests/
%{python27_sitearch}/numpy/polynomial/tests/*.py*


%files devel
%defattr(-,root,root,-)
%{python27_sitearch}/numpy/distutils
%{_includedir}/python27-numpy
%dir %{python27_sitearch}/numpy/core/include
%dir %{python27_sitearch}/numpy/core/include/numpy
%{python27_sitearch}/numpy/core/include/numpy/*.h
%{python27_sitearch}/numpy/core/include/numpy/*.txt
%{python27_sitearch}/numpy/random/*.h
%{python27_sitearch}/numpy/core/lib
%dir %{python27_sitearch}/numpy/numarray/include
%dir %{python27_sitearch}/numpy/numarray/include/numpy
%{python27_sitearch}/numpy/numarray/include/numpy/*.h

%files f2py
%defattr(-,root,root,-)
%{_mandir}/man*/*
%{_bindir}/f2py2.6
%dir %{python27_sitearch}/numpy/f2py/
%{python27_sitearch}/numpy/f2py/*.py*
%dir %{python27_sitearch}/numpy/f2py/tests/
%{python27_sitearch}/numpy/f2py/tests/*.py*
%{python27_sitearch}/numpy/f2py/src/
%{python27_sitearch}/numpy/f2py/tests/src/
%doc docs-f2py

%files f2py-tests
%defattr(-,root,root,-)
%dir %{python27_sitearch}/numpy/f2py/tests/
%{python27_sitearch}/numpy/f2py/tests/*.py*
%{python27_sitearch}/numpy/f2py/tests/src/

%changelog
* Tue May 21 2013 Brett Taylor <btaylor@wistar.org> - 1.7.1-1
- Update to latest release
- Update to python27

* Thu Jun 16 2011 Steve Traylen <steve.traylen@cern.ch> - 1.5.1-5
- Add eGenix license, rhbz#619355

* Mon May 23 2011 Steve Traylen <steve.traylen@cern.ch> - 1.5.1-4
- Correct license to Python and MIT and BSD.

* Sat Apr 3 2011 Steve Traylen <steve.traylen@cern.ch> - 1.5.1-3
- Add fno-strict-alias to compile - see rhbz#619355.
- Remove BR of lapack - see rhbz#478856.
- Add Requires of atlas - see rhbz#478856.

* Tue Feb 1 2011 Steve Traylen <steve.traylen@cern.ch> - 1.5.1-2
- Move header files and distutils file out to a devel package,
  rhbz#619355.
- Move tests files out to a tests package,
  rhbz#619355.
- Move f2py documents to f2py package.

* Mon Dec 15 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.1-1
- Update to new 1.5.1 upstream.
- Hardcode alternative python as 26 everywhere.

* Thu Jun 24 2010 Steve Traylen <steve.traylen@cern.ch> - 1.4.1-1
- Adapt F14 .spec file to python26 in EPEL5.
- New upstream 1.4.1-1

* Mon Apr 26 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-8
- Moved distutils back to the main package, BZ 572820.

* Thu Apr 08 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-7
- Reverted to 1.3.0 after upstream pulled 1.4.0, BZ 579065.

* Tue Mar 02 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-5
- Linking /usr/include/numpy to .h files, BZ 185079.

* Tue Feb 16 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-4
- Re-enabling atlas BR, dropping lapack Requires.

* Wed Feb 10 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-3
- Since the previous didn't work, Requiring lapack.

* Tue Feb 09 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-2
- Temporarily dropping atlas BR to work around 562577.

* Fri Jan 22 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-1
- 1.4.0.
- Dropped ARM patch, ARM support added upstream.

* Tue Nov 17 2009 Jitesh Shah <jiteshs@marvell.com> - 1.3.0-6.fa1
- Add ARM support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-5
- Fixed atlas BR, BZ 505376.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-4
- EVR bump for pygame chainbuild.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-3
- Moved linalg, fft back to main package.

* Tue Apr 14 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-2
- Split out f2py into subpackage, thanks Peter Robinson pbrobinson@gmail.com.

* Tue Apr 07 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-1
- Update to latest upstream.
- Fixed Source0 URL.

* Thu Apr 02 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-0.rc1
- Update to latest upstream.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 1.2.1-3
- Require python-devel, BZ 488464.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 Jon Ciesla <limb@jcomserv.net> 1.2.1-1
- Update to 1.2.1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.0-2
- Rebuild for Python 2.6

* Tue Oct 07 2008 Jon Ciesla <limb@jcomserv.net> 1.2.0-1
- New upstream release, added python-nose BR. BZ 465999.
- Using atlas blas, not blas-devel. BZ 461472.

* Wed Aug 06 2008 Jon Ciesla <limb@jcomserv.net> 1.1.1-1
- New upstream release

* Thu May 29 2008 Jarod Wilson <jwilson@redhat.com> 1.1.0-1
- New upstream release

* Tue May 06 2008 Jarod Wilson <jwilson@redhat.com> 1.0.4-1
- New upstream release

* Mon Feb 11 2008 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-2
- Add python egg to %%files on f9+

* Wed Aug 22 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-1
- New upstream release

* Wed Jun 06 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3-1
- New upstream release

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Drop BR: atlas-devel, since it just provides binary-compat
  blas and lapack libs. Atlas can still be optionally used
  at runtime. (Note: this is all per the atlas maintainer).

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-1
- New upstream release

* Tue Apr 17 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-4
- Update gfortran patch to recognize latest gfortran f95 support 
- Resolves rhbz#236444

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-3
- Fix up cpuinfo bug (#229753). Upstream bug/change:
  http://projects.scipy.org/scipy/scipy/ticket/349

* Thu Jan 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2
- Per discussion w/Jose Matos, Obsolete/Provide f2py, as the
  stand-alone one is no longer supported/maintained upstream

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.0.1-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.0-2
- Rebuild for python 2.5

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.0-1
- New upstream release

* Tue Sep 06 2006 Jarod Wilson <jwilson@redhat.com> 0.9.8-1
- New upstream release

* Wed Apr 26 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.6-1
- Upstream update

* Thu Feb 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.5-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-2
- Rebuild for Fedora Extras 5

* Thu Feb  2 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-1
- Initial RPM release
- Added gfortran patch from Neal Becker

