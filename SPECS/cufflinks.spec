Name:           cufflinks
Version:        2.1.1
Release:        1%{?dist}
Summary:        Transcript assembly, differential expression, and differential regulation for RNA-Seq

License:        GPLv3
Group:		Other
URL:		http://cufflinks.cbcb.umd.edu/
Source0:        %{name}-%{version}.Linux_x86_64.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

Requires:	zlib >= 1.2.2
#BuildRequires:  
AutoReqProv:	no

%description 

Cufflinks assembles transcripts, estimates their abundances, and tests for 
differential expression and regulation in RNA-Seq samples. It accepts aligned 
RNA-Seq reads and assembles the alignments into a parsimonious set of transcripts. 
Cufflinks then estimates the relative abundances of these transcripts based on 
how many reads support each one, taking into account biases in library preparation protocols. 

%prep
%setup -q -n %{name}-%{version}.Linux_x86_64


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 cuffcompare %{buildroot}%{_bindir}
install -m 0755 cuffdiff %{buildroot}%{_bindir}
install -m 0755 cufflinks %{buildroot}%{_bindir}
install -m 0755 cuffmerge %{buildroot}%{_bindir}
install -m 0755 gffread %{buildroot}%{_bindir}
install -m 0755 gtf_to_sam %{buildroot}%{_bindir}

%files
%doc AUTHORS LICENSE README
%{_bindir}/cuffcompare
%{_bindir}/cuffdiff
%{_bindir}/cufflinks
%{_bindir}/cuffmerge
%{_bindir}/gffread
%{_bindir}/gtf_to_sam


%changelog
* Fri Feb 8 2013 Brett Taylor <btaylor@wistar.org> - 2.0.2
- initial version
