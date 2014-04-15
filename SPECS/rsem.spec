Name:           rsem
Version:        1.2.12
Release:        1%{?dist}
Summary:        RNA-Seq by Expectation-Maximization

License:        GPL
Group:		Other
URL:		http://deweylab.biostat.wisc.edu/rsem/       
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

BuildRequires:	zlib-devel, ncurses-devel

Requires:	bwa
Autoreq:	0

%description 
RSEM is a software package for estimating gene and isoform expression 
levels from RNA-Seq data. The RSEM package provides an user-friendly 
interface, supports threads for parallel computation of the EM algorithm, 
single-end and paired-end read data, quality scores, variable-length reads 
and RSPD estimation. In addition, it provides posterior mean and 95% 
credibility interval estimates for expression levels. For visualization, 
It can generate BAM and Wiggle files in both transcript-coordinate and 
genomic-coordinate. Genomic-coordinate files can be visualized by both 
UCSC Genome browser and Broad Institute’s Integrative Genomics Viewer 
(IGV). Transcript-coordinate files can be visualized by IGV. RSEM also 
has its own scripts to generate transcript read depth plots in pdf 
format. The unique feature of RSEM is, the read depth plots can be stacked, 
with read depth contributed to unique reads shown in black and contributed 
to multi-reads shown in red. In addition, models learned from data can also 
be visualized. Last but not least, RSEM contains a simulator.

%prep
%setup -q -n %{name}-%{version}

%build
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}/sam
install -m 0755 rsem-* %{buildroot}%{_bindir}
install -m 0755 extract-transcript-to-gene-map-from-trinity %{buildroot}%{_bindir}
install -m 0755 convert-sam-for-rsem %{buildroot}%{_bindir}
install -m 0755 sam/samtools %{buildroot}%{_bindir}/sam

%files
%defattr(-,root,root)
%doc WHAT_IS_NEW 
%{_bindir}/rsem-*
%{_bindir}/extract-transcript-to-gene-map-from-trinity
%{_bindir}/convert-sam-for-rsem
%{_bindir}/sam/samtools

%changelog
* Thu Mar 7 2013 Brett Taylor <btaylor@wistar.org> - 1.2.3-2
- including sam/samtools because it's hardcoded
* Thu Mar 7 2013 Brett Taylor <btaylor@wistar.org> - 1.2.3
- initial version
