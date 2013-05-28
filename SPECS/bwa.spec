Name:           bwa
Version:        0.7.3a
Release:        1%{?dist}
Summary:        Burrows-Wheeler Aligner

License:        GPLv3
Group:		Other
URL:		http://sourceforge.net/projects/bio-bwa/       
Source0:        %{name}-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

BuildRequires:  zlib-devel


%description 
BWA is a program for aligning sequencing reads against a large reference genome 
(e.g. human genome). It has two major components, one for read shorter than 
150bp and the other for longer reads.

%prep
%setup -q -n %{name}-%{version}

%build
%{__make}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bwa %{buildroot}%{_bindir}
install -m 0755 bwamem-lite %{buildroot}%{_bindir}
install -m 0755 qualfa2fq.pl %{buildroot}%{_bindir}
install -m 0755 xa2multi.pl %{buildroot}%{_bindir}

%files
%doc README COPYING NEWS
%{_bindir}/bwa
%{_bindir}/bwamem-lite
%{_bindir}/qualfa2fq.pl
%{_bindir}/xa2multi.pl


%changelog
* Mon Jan 28 2013 Brett Taylor <btaylor@wistar.org> - 2.0.6
- updated to version 2.0.6
* Mon Jan  9 2012 Adam Huffman <verdurin@fedoraproject.org> - 2.0.0-0.1.beta5%{?dist}
- initial version
