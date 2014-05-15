Name:           sratoolkit
Version:        2.3.5
Release:        1%{?dist}
Summary:        The NCBI SRA Toolkit provides for easy reading (dumping) of sequencing files from SRA database and writing (loading) to the SRA database.

License:        GPLv3
Group:		Other
URL:		http://www.ncbi.nlm.nih.gov/Traces/sra/?view=software
Source0:        http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.3.5-2/%{name}.%{version}-2-centos_linux64.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

%description 

The NCBI SRA Toolkit provides for easy reading (dumping) of sequencing files 
from SRA database and writing (loading) to the SRA database.

%prep
%setup -q -n %{name}.%{version}-2-centos_linux64

%build


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install bin/abi-dump* %{buildroot}%{_bindir}
install bin/abi-load* %{buildroot}%{_bindir}
install bin/align-info* %{buildroot}%{_bindir}
install bin/bam-load* %{buildroot}%{_bindir}
install bin/cache-mgr* %{buildroot}%{_bindir}
install bin/cg-load* %{buildroot}%{_bindir}
install bin/configuration-assistant.perl %{buildroot}%{_bindir}
install bin/fastq-dump* %{buildroot}%{_bindir}
install bin/fastq-load* %{buildroot}%{_bindir}
install bin/helicos-load* %{buildroot}%{_bindir}
install bin/illumina-dump* %{buildroot}%{_bindir}
install bin/illumina-load* %{buildroot}%{_bindir}
install bin/kar* %{buildroot}%{_bindir}
install bin/kdbmeta* %{buildroot}%{_bindir}
install bin/latf-load* %{buildroot}%{_bindir}
install bin/libvdb_jni.so %{buildroot}%{_bindir}
install bin/pacbio-load* %{buildroot}%{_bindir}
install bin/prefetch* %{buildroot}%{_bindir}
install bin/rcexplain* %{buildroot}%{_bindir}
install bin/refseq-load* %{buildroot}%{_bindir}
install bin/sam-dump* %{buildroot}%{_bindir}
install bin/sff-dump* %{buildroot}%{_bindir}
install bin/sff-load* %{buildroot}%{_bindir}
install bin/sra-kar* %{buildroot}%{_bindir}
install bin/srapath* %{buildroot}%{_bindir}
install bin/sra-pileup* %{buildroot}%{_bindir}
install bin/sra-sort* %{buildroot}%{_bindir}
install bin/sra-stat* %{buildroot}%{_bindir}
install bin/srf-load* %{buildroot}%{_bindir}
install bin/test-sra* %{buildroot}%{_bindir}
install bin/vdb-config* %{buildroot}%{_bindir}
install bin/vdb-copy* %{buildroot}%{_bindir}
install bin/vdb-decrypt* %{buildroot}%{_bindir}
install bin/vdb-dump* %{buildroot}%{_bindir}
install bin/vdb-encrypt* %{buildroot}%{_bindir}
install bin/vdb-lock* %{buildroot}%{_bindir}
install bin/vdb-passwd* %{buildroot}%{_bindir}
install bin/vdb-unlock* %{buildroot}%{_bindir}
install bin/vdb-validate* %{buildroot}%{_bindir}
install bin/sratoolkit.jar %{buildroot}%{_bindir}

%post

%postun

%files
%defattr(-, root, root)
%doc help/ 
%{_bindir}/abi-dump*
%{_bindir}/abi-load*
%{_bindir}/align-info*
%{_bindir}/bam-load*
%{_bindir}/cache-mgr*
%{_bindir}/cg-load*
%{_bindir}/configuration-assistant.perl
%{_bindir}/fastq-dump*
%{_bindir}/fastq-load*
%{_bindir}/helicos-load*
%{_bindir}/illumina-dump*
%{_bindir}/illumina-load*
%{_bindir}/kar*
%{_bindir}/kdbmeta*
%{_bindir}/latf-load*
%{_bindir}/libvdb_jni.so
%{_bindir}/pacbio-load*
%{_bindir}/prefetch*
%{_bindir}/rcexplain*
%{_bindir}/sam-dump*
%{_bindir}/sff-dump*
%{_bindir}/sff-load*
%{_bindir}/sra-kar*
%{_bindir}/srapath*
%{_bindir}/sra-pileup*
%{_bindir}/sra-sort*
%{_bindir}/sra-stat*
%{_bindir}/srf-load*
%{_bindir}/test-sra*
%{_bindir}/vdb-config*
%{_bindir}/vdb-copy*
%{_bindir}/vdb-decrypt*
%{_bindir}/vdb-dump*
%{_bindir}/vdb-encrypt*
%{_bindir}/vdb-lock*
%{_bindir}/vdb-passwd*
%{_bindir}/vdb-unlock*
%{_bindir}/vdb-validate*
%{_bindir}//sratoolkit.jar
%{_bindir}/sratoolkit.jar

%changelog
* Thu May 15 2014 Brett Taylor <btaylor@wistar.org> - 2.3.5-2
- version increment
* Fri Mar 22 2013 Brett Taylor <btaylor@wistar.org> - 2.0.1
- initial version
