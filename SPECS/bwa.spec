Name:           bwa
Version:        0.7.10
Release:        1%{?dist}
Summary:        Burrows-Wheeler Alignment tool

Group:          Applications/Engineering
License:        GPLv3
URL:            http://bio-bwa.sourceforge.net/
Source0:        http://downloads.sourceforge.net/bio-%{name}/%{name}-%{version}.tar.bz2
# 0.7.x versions only build on x86_64
ExclusiveArch:	x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel

%description

BWA is a program for aligning sequencing reads against a large
reference genome (e.g. human genome). It has two major components, one
for read shorter than 150bp and the other for longer reads.

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1

install -m 0755 bwa %{buildroot}/%{_bindir}
install -m 0755 qualfa2fq.pl %{buildroot}/%{_bindir}
install -m 0755 xa2multi.pl %{buildroot}/%{_bindir}

install -m 0644 bwa.1 %{buildroot}/%{_mandir}/man1/bwa.1

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING
%{_mandir}/man1/%{name}.1*
%{_bindir}/bwa
%{_bindir}/qualfa2fq.pl
%{_bindir}/xa2multi.pl


%changelog
* Mon Dec 08 2014 Brett Taylor <btaylor@wistar.org) - 0.7.10
- Update to upstream 0.7.10

* Sun Oct 27 2013 Adam Huffman <bloch@verdurin.com> - 0.7.5a-2
- Remove nosse2 patch because 0.7+ versions only build on x86_64

* Sat Oct 26 2013 Adam Huffman <bloch@verdurin.com> - 0.7.5a-1
- Update to upstream 0.7.5a

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.6.1-6
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Dan Horák <dan[at]danny.cz> - 0.6.1-3
- enable SSE2 on x86_64 only, fixes build on secondary arches

* Sun May 13 2012 Adam Huffman <verdurin@fedoraproject.org> - 0.6.1-2
- add patch to avoid SSE2 on i386

* Wed Jan 11 2012 Adam Huffman <verdurin@fedoraproject.org> - 0.6.1-1
- update to 0.6.1

* Thu Feb 17 2011 Adam Huffman <bloch@verdurin.com> - 0.5.9-1
- new upstream release 0.5.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Adam Huffman <bloch@verdurin.com> - 0.5.8c-1
- upstream bugfix release

* Tue Jul 20 2010 Adam Huffman <bloch@verdurin.com> - 0.5.8a-1
- new upstream release

* Sat May 29 2010 Adam Huffman <bloch@verdurin.com> - 0.5.7-2
- fix source URL
- install manpage
- fix cflags

* Fri May 28 2010 Adam Huffman <bloch@verdurin.com> - 0.5.7-1
- initial version