Name:           bowtie
Version:        1.0.1
Release:        1%{?dist}
Summary:        An ultrafast memory-efficient short read aligner

License:        GPLv3
Group:		Other
URL:		http://bowtie-bio.sourceforge.net/       
Source0:        %{name}-%{version}-linux-x86_64.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

#BuildRequires:  


%description 

Bowtie is an ultrafast, memory-efficient short read aligner. It aligns short
DNA sequences (reads) to the human genome at a rate of over 25 million 35-bp 
reads per hour. Bowtie indexes the genome with a Burrows-Wheeler index to keep 
its memory footprint small: typically about 2.2 GB for the human genome 
(2.9 GB for paired-end).

%prep
%setup -q -n %{name}-%{version}


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bowtie* %{buildroot}%{_bindir}

%files
%doc AUTHORS NEWS TUTORIAL VERSION MANUAL MANUAL.markdown doc/
%doc doc genomes indexes reads scripts
%{_bindir}/bowtie*


%changelog
* Thu May 15 2014 Brett Taylor<btaylor@wistar.org> - 1.0.1
- new version
* Fri Feb 8 2013 Brett Taylor <btaylor@wistar.org> - 0.12.9
- initial version
