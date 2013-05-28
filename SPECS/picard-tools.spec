Name:           picard-tools
Version:        1.64
Release:        1%{?dist}
Summary:        A set of tools (in Java) for working with next generation sequencing data in the BAM format.

License:        GPLv3
Group:		Other
URL:		http://picard.sourceforge.net
Source0:        %{name}-%{version}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#BuildRequires:  


%description 
Picard comprises Java-based command-line utilities that manipulate SAM 
files, and a Java API (SAM-JDK) for creating new programs that read and 
write SAM files. Both SAM text format and SAM binary (BAM) format are supported.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/picard-tools
install -m 644 *.jar %{buildroot}%{_bindir}/picard-tools

%files
%{_bindir}/picard-tools/*.jar

%changelog
* Wed Mar 27 2013 Brett Taylor <btaylor@wistar.org> - 1.64
- initial version
