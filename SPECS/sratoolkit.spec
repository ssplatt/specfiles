Name:           sratoolkit
Version:        2.3.5-2
Release:        1%{?dist}
Summary:        The NCBI SRA Toolkit provides for easy reading (dumping) of sequencing files from SRA database and writing (loading) to the SRA database.

License:        GPLv3
Group:		Other
URL:		http://www.ncbi.nlm.nih.gov/Traces/sra/?view=software
Source0:        http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.3.5-2/%{name}.%{version}-centos_linux64.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

%description 

The NCBI SRA Toolkit provides for easy reading (dumping) of sequencing files 
from SRA database and writing (loading) to the SRA database.

%prep
%setup -q -n %{name}.%{version}-centos_linux64

%build


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install abi-dump* %{buildroot}%{_bindir}
install abi-load* %{buildroot}%{_bindir}
install fastq-dump* %{buildroot}%{_bindir}
install fastq-load* %{buildroot}%{_bindir}
install helicos-load* %{buildroot}%{_bindir}
install illumina-dump* %{buildroot}%{_bindir}
install illumina-load* %{buildroot}%{_bindir}
install kar* %{buildroot}%{_bindir}
install kdbmeta* %{buildroot}%{_bindir}
install rcexplain* %{buildroot}%{_bindir}
install sff-dump* %{buildroot}%{_bindir}
install sff-load* %{buildroot}%{_bindir}
install sra-dbcc* %{buildroot}%{_bindir}
install sra-dump* %{buildroot}%{_bindir}
install sra-kar* %{buildroot}%{_bindir}
install sra-stat* %{buildroot}%{_bindir}
install srf-load* %{buildroot}%{_bindir}
install vdb-copy* %{buildroot}%{_bindir}
install vdb-dump* %{buildroot}%{_bindir}

%post

%postun

%files
%defattr(-, root, root)
%doc help/ 
%{_bindir}/abi-dump*
%{_bindir}/abi-load*
%{_bindir}/fastq-dump*
%{_bindir}/fastq-load*
%{_bindir}/helicos-load*
%{_bindir}/illumina-dump*
%{_bindir}/illumina-load*
%{_bindir}/kar*
%{_bindir}/kdbmeta*
%{_bindir}/rcexplain*
%{_bindir}/sff-dump*
%{_bindir}/sff-load*
%{_bindir}/sra-dbcc*
%{_bindir}/sra-dump*
%{_bindir}/sra-kar*
%{_bindir}/sra-stat*
%{_bindir}/srf-load*
%{_bindir}/vdb-copy*
%{_bindir}/vdb-dump*

%changelog
* Thu May 15 2014 Brett Taylor <btaylor@wistar.org> - 2.3.5-2
- version increment
* Fri Mar 22 2013 Brett Taylor <btaylor@wistar.org> - 2.0.1
- initial version
