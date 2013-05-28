%define debug_package %{nil}

Name:           IReckon
Version:        1.0.7
Release:        1%{?dist}
Summary:        iReckon is an algorithm for the simultaneous isoform reconstruction and abundance estimation.

Group:          misc
License:        GPLv2
URL:            http://compbio.cs.toronto.edu/ireckon/
Source0:        IReckon-1.0.7.jar

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       java-1.6.0-openjdk
#Requires:       java

# disable jar repackaging
%define __os_install_post %{nil}

%description
iReckon is an algorithm for the simultaneous isoform reconstruction and 
abundance estimation. In addition to modelling novel isoforms, multi-mapped 
reads and read duplicates, this method takes into account the possible 
presence of unspliced pre-mRNA and intron retention. iReckon only requires a 
set of transcription start and end sites, but can use known full isoforms to 
improve sensitivity. Starting from the set of nearly all possible isoforms, 
iReckon uses a regularized EM algorithm to determine those actually present 
in the sequenced sample, together with their abundances. iReckon is 
multi-threaded to increase efficiency in all its time consuming steps. 

%prep
cp -p %SOURCE0 .

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 644 -t "%{buildroot}%{_bindir}" *.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*.jar

%changelog
* Mon Mar 7 2013 Brett Taylor <btaylor@wistar.org> - 1.0.7
- initial version
