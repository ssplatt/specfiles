Name:           Kibana
Version:        0.2.0
Release:        3%{?dist}
Summary:        Kibana is an interface to Logstash and ElasticSearch

Group:          System Environment/Daemons
License:        MIT
URL:            http://rashidkpc.github.com/Kibana/
Source0:        %{name}-%{version}.tar.gz
Source1:	kibana-httpd.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       ruby,rubygems

%description
Kibana is an open source (MIT License), browser based interface to Logstash and ElasticSearch

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}
%{__mv} * %{buildroot}%{_datadir}/%{name}

%{__install} -Dp -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/kibana.conf

%post
cd %{_datadir}/%{name}
gem install bundler
bundle install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/KibanaConfig.rb
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/httpd/conf.d/kibana.conf

%changelog
* Mon Apr 8 2013 Brett Taylor btaylor@wistar.org 0.2.0
- Updated to version 0.2.0

* Fri May 18 2012 David Castro arimus@gmail.com 0.1.5-1
- Modified spec to work with rpmbuild -ta kibana-0.1.5.tar.gz style builds,
  which only requires that the github-style tarballs are renamed to
  kibana-X.Y.Z.tar.gz

* Fri Apr 06 2012 David Castro arimus@gmail.com 0.1.4
- Initial spec
