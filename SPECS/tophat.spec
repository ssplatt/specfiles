%define debug_package %{nil}

Name:		tophat
Version:	2.0.8b
Release:        1%{?dist}
Summary:	A spliced read mapper for RNA-Seq

Group:		Applications/Engineering
License:	Artistic 2.0
URL:		http://tophat.cbcb.umd.edu/
Source0:	http://tophat.cbcb.umd.edu/downloads/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

BuildRequires:	samtools-devel, boost-devel >= 1.38.0

%description

TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns
RNA-Seq reads to mammalian-sized genomes using the ultra
high-throughput short read aligner Bowtie, and then analyzes the
mapping results to identify splice junctions between exons.

TopHat is a collaborative effort between the University of Maryland
Center for Bioinformatics and Computational Biology and the University
of California, Berkeley Departments of Mathematics and Molecular and
Cell Biology.

%prep
%setup -q -n %{name}-%{version}


%build
#export BAM_ROOT=%{_prefix}
#echo $BAM_ROOT
ls -la /usr/lib/libbam.a
%configure --prefix=%{_prefix} --with-bam=%{_prefix}
%{__make}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bam2fastx %{buildroot}%{_bindir}
install -m 0755 bam_merge %{buildroot}%{_bindir}
install -m 0755 bed_to_juncs %{buildroot}%{_bindir}
install -m 0755 contig_to_chr_coords %{buildroot}%{_bindir}
install -m 0755 fix_map_ordering %{buildroot}%{_bindir}
install -m 0755 gtf_juncs %{buildroot}%{_bindir}
install -m 0755 gtf_to_fasta %{buildroot}%{_bindir}
install -m 0755 juncs_db %{buildroot}%{_bindir}
install -m 0755 long_spanning_reads %{buildroot}%{_bindir}
install -m 0755 map2gtf %{buildroot}%{_bindir}
install -m 0755 prep_reads %{buildroot}%{_bindir}
install -m 0755 sam_juncs %{buildroot}%{_bindir}
install -m 0755 segment_juncs %{buildroot}%{_bindir}
install -m 0755 sra_to_solid %{buildroot}%{_bindir}
install -m 0755 tophat %{buildroot}%{_bindir}
install -m 0755 tophat2 %{buildroot}%{_bindir}
install -m 0755 tophat-fusion-post %{buildroot}%{_bindir}
install -m 0755 tophat_reports %{buildroot}%{_bindir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS
%{_bindir}/*


%changelog
* Thu May 02 2013 Brett Taylor <btaylor@wistar.org> - 2.0.8b-1
- changed to version 2.0.8b

* Thu Jan 28 2013 Brett Taylor <btaylor@wistar.org> - 2.0.7-1
- changed to version 2.0.7

* Thu Aug 11 2011 Adam Huffman <bloch@verdurin.com> - 1.3.1-1
- initial version
