Name:		hydra-sv
Version:	0.5.3
Release:	1%{?dist}
Summary:	Hydra detects structural variation breakpoints in both unique and duplicated genomic regions.

Group:		Applications/Biology
License:	MIT
URL:		https://code.google.com/p/hydra-sv/
Source0:	Hydra.v%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	zlib-devel

%description

Hydra detects structural variation (SV) breakpoints by clustering discordant paired-end alignments whose
"signatures" corroborate the same putative breakpoint. Hydra can detect breakpoints caused by all classes
of structural variation. Moreover, it was designed to detect variation in both unique and duplicated
genomic regions; therefore, it will examine paired-end reads having multiple discordant alignments.

%prep
%setup -q -n Hydra-Version-%{version}

%build
make clean
make all %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

install -m 0755 bin/bamToFastq %{buildroot}%{_bindir}
install -m 0755 bin/hydra %{buildroot}%{_bindir}
install -m 0755 scripts/dedupDiscordants.py %{buildroot}%{_bindir}
install -m 0755 scripts/pairDiscordants.py %{buildroot}%{_bindir}

%files
%{_bindir}/bamToFastq
%{_bindir}/hydra
%{_bindir}/dedupDiscordants.py
%{_bindir}/pairDiscordants.py

%defattr(-,root,root,-)

%doc

%changelog
* Mon Dec 08 2014 Brett Taylor <btaylor@wistar.org> - 0.5.3-1
- initial version