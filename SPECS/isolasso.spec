Name:           isolasso
Version:        2.6.1
Release:        1%{?dist}
Summary:        IsoLasso is an algorithm to assemble transcripts and estimate their expression levels from RNA-Seq reads.

License:        GPL
Group:		Other
URL:		http://alumni.cs.ucr.edu/~liw/isolasso.html
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

BuildRequires:	gsl-devel
BuildRequires:	CGAL-devel

#Requires:	bwa

%description 
IsoLasso: A LASSO Regression Approach to RNA-Seq Based Transcriptome Assembly

%prep
%setup -q -n %{name}

%build
cd src/
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/* %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Thu Mar 7 2013 Brett Taylor <btaylor@wistar.org> - 2.6.1-1
- initial version
