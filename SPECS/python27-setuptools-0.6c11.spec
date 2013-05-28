%define name python27-setuptools
%define version 0.6c11
%define unmangled_version 0.6c11
%define release milford

Summary: Download, build, install, upgrade, and uninstall Python packages -- easily!
Name: %{name}
Version: %{version}
Release: %{release}
Source0: setuptools-%{unmangled_version}.tar.gz
License: PSF or ZPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Phillip J. Eby <distutils-sig@python.org>
BuildRequires: python27-devel
Requires: python27
Url: http://pypi.python.org/pypi/setuptools
Packager: Nathan Milford <nathan@milford.io> 

%description
Setuptools is similar to a package manager for Python

%prep
%setup -n setuptools-%{unmangled_version}

%build
python2.7 setup.py build

%install
python2.7 setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT 
# --record=INSTALLED_OBJECTS
# Lets not overwrite the default one in CentOS/RHEL
rm -f $RPM_BUILD_ROOT/usr/bin/easy_install

%clean
rm -rf $RPM_BUILD_ROOT

%files 
#-f INSTALLED_OBJECTS
/usr/lib/python2.7/site-packages/easy_install.pyo
/usr/lib/python2.7/site-packages/pkg_resources.pyo
/usr/lib/python2.7/site-packages/site.pyo
/usr/lib/python2.7/site-packages/pkg_resources.py
/usr/lib/python2.7/site-packages/easy_install.py
/usr/lib/python2.7/site-packages/site.py
/usr/lib/python2.7/site-packages/setuptools/
/usr/lib/python2.7/site-packages/pkg_resources.pyc
/usr/lib/python2.7/site-packages/easy_install.pyc
/usr/lib/python2.7/site-packages/site.pyc
/usr/lib/python2.7/site-packages/setuptools/tests/
/usr/lib/python2.7/site-packages/setuptools/command/
/usr/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg-info
/usr/bin/easy_install-2.7
#/usr/bin/easy_install

%defattr(-,root,root)
%doc setuptools.txt EasyInstall.txt pkg_resources.txt README.txt
