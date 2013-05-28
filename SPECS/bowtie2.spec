Name:           bowtie2
Version:        2.0.6
Release:        1%{?dist}
Summary:        Fast and sensitive read alignment

License:        GPLv3
Group:		Other
URL:		http://bowtie-bio.sourceforge.net/%{name}/index.shtml       
Source0:        %{name}-%{version}-linux-x86_64.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

#BuildRequires:  


%description 

Bowtie 2 is an ultrafast and memory-efficient tool for
aligning sequencing reads to long reference sequences. It is
particularly good at aligning reads of about 50 up to 100s or 1,000s
of characters, and particularly good at aligning to relatively long
(e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index
to keep its memory footprint small: for the human genome, its memory
footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local,
and paired-end alignment modes.

%prep
%setup -q -n %{name}-%{version}


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bowtie2* %{buildroot}%{_bindir}

%files
%doc AUTHORS NEWS TUTORIAL VERSION MANUAL MANUAL.markdown doc/
%doc example scripts
%{_bindir}/bowtie2*


%changelog
* Mon Jan 28 2013 Brett Taylor <btaylor@wistar.org> - 2.0.6
- updated to version 2.0.6
* Mon Jan  9 2012 Adam Huffman <verdurin@fedoraproject.org> - 2.0.0-0.1.beta5%{?dist}
- initial version
