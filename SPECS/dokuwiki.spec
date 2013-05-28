Name:		dokuwiki
Version:	0
Release:	0.15.20130510%{?dist}
Summary:	Standards compliant simple to use wiki
Group:		Applications/Internet
License:	GPLv2
URL:		http://www.dokuwiki.org/dokuwiki
Source0:	http://www.splitbrain.org/_media/projects/%{name}/%{name}-2013-05-10.tgz
#Fedora specific patches to use fedora packaged libraries
Patch1:		dokuwiki-rm-bundled-libs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	php-gd
Requires:	php-geshi
#Requires:	php-simplepie
Requires:	php-email-address-validation
Requires:	httpd

%description
DokuWiki is a standards compliant, simple to use Wiki, mainly aimed at creating 
documentation of any kind. It has a simple but powerful syntax which makes sure 
the datafiles remain readable outside the Wiki and eases the creation of 
structured texts. 

All data is stored in plain text files no database is required. 

%package selinux
Summary:	SElinux support for dokuwiki
Requires:	%name = %version-%release
Requires:	policycoreutils policycoreutils-python
Group:          Applications/Internet
BuildArch:	noarch

%description selinux
Configures DokuWiki to run in SELinux enabled environments.

%prep
%setup -q -n %{name}-2013-05-10
%patch1 -p1 

chmod a-x inc/lang/az/*.{txt,html}

mv -f conf/mysql.conf.php.example .

sed -i "s:'./data':'%{_localstatedir}/lib/%{name}/data':" conf/%{name}.php
sed -i "s:ALL        8:ALL        1:" conf/acl.auth.php.dist

cat <<EOF >%{name}.httpd
# %{name}
# %{summary}
# %{version}
#

Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
	Options +FollowSymLinks
	Order Allow,Deny
	Allow from 127.0.0.1 ::1
</Directory>

<Directory %{_datadir}/%{name}/inc>
	Order Deny,Allow
	Deny from all
</Directory>

<Directory %{_datadir}/%{name}/inc/lang>
	Order Deny,Allow
	Deny from all
</Directory>

<Directory %{_datadir}/%{name}/lib/_fla>
	## no access to the fla directory
	Order allow,deny
	Deny from all
</Directory>

<Directory %{_sysconfdir}/%{name}>
	Order Deny,Allow
	Deny from all
</Directory>

EOF

cat <<EOF >DOKUWIKI-SELINUX.README
%{name}-selinux
====================

This package configures dokuwiki to run in
SELinux enabled environments

EOF

%build
# nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -d -p $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d -p $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
install -d -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/data/{index,tmp,media,attic,pages,cache,meta,locks,media_attic,media_meta}
rm -f install.php
rm -rf inc/geshi*
rm -f inc/EmailAddressValidator.php
rm -f inc/.htaccess
rm -f inc/lang/.htaccess
rm -f lib/_fla/{.htaccess,README}
rm -f lib/plugins/revert/lang/sk/intro.txt
cp -rp data/pages/* $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/data/pages/
cp -rp conf/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -rp bin/*  $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
cp -rp lib  $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -rp inc  $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -p -m0644 *.php $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m0644 %{name}.httpd $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

pushd $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
for d in *.dist; do
	d0=`basename $d .dist`
	if [ ! -f "$d0" ]; then
		mv -f $d $d0
	fi
done
popd

pushd $RPM_BUILD_ROOT%{_datadir}/%{name}
	ln -sf ../../../etc/%name conf
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post selinux
semanage fcontext -a -t httpd_sys_content_rw_t '%{_sysconfdir}/%{name}(/.*)?' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_content_t '%{_datadir}/%{name}(/.*)?' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_content_rw_t '%{_datadir}/%{name}/lib/plugins(/.*)?' 2>/dev/null || :
restorecon -R '%{_sysconfdir}/%{name}' || :
restorecon -R '%{_datadir}/%{name}' || :
restorecon -R '%{_datadir}/%{name}/lib/plugins' || :

%postun selinux
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_content_rw_t '%{_sysconfdir}/%{name}(/.*)?' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_content_t '%{_datadir}/%{name}(/.*)?' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_content_rw_t '%{_datadir}/%{name}/lib/plugins(/.*)?' 2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING README VERSION mysql.conf.php.example
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %attr(0644,apache,apache) %{_sysconfdir}/%{name}/*
%dir %attr(0755,apache,apache) %{_sysconfdir}/%{name}
%attr(0755,apache,apache) %{_datadir}/%{name}/bin/*.php
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/*.php
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/exe
%{_datadir}/%{name}/lib/images
%{_datadir}/%{name}/lib/index.html
%{_datadir}/%{name}/lib/scripts
%{_datadir}/%{name}/lib/styles
%{_datadir}/%{name}/lib/tpl
#%{_datadir}/%{name}/lib/_fla
%attr(0755,apache,apache) %dir %{_datadir}/%{name}/lib/plugins
%{_datadir}/%{name}/lib/plugins/*
%{_datadir}/%{name}/inc
%dir %{_localstatedir}/lib/%{name}
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/media
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/attic
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/cache
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/meta
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/locks
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/tmp
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/index
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/media_attic
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/media_meta
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/pages
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/pages/playground
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/%{name}/data/pages/wiki
%{_localstatedir}/lib/%{name}/data/pages/*/*

%files selinux
%defattr(-,root,root,-)
%doc DOKUWIKI-SELINUX.README

%changelog
* Tue May 14 2013 Brett Taylor <btaylor@wistar.org> - 0-0.15.20130510
- Latest upstream

* Sat Oct 20 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.14.20121013
- Latest upstream
- Fix Bugzilla bugs #844726, #840255, #795487, #741384, #840686, #835145

* Thu Aug 02 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.13.20120125.b
- Latest upstream
- Fix Bugzilla bugs #844726, #840255, #795487, #741384, #840686, #835145
 
* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.12.20110525.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.11.20110525.a
- Fix CVE-2012-2129
- Fix Bugzilla bugs #815123

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.20110525.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.9.20110525.a
- Upgrade to latest upstream
- Fix Bugzilla bugs #717146, #717149, #717148, #715569

* Sun Mar 13 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.8.20101107.a
- Fix genshi path

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.20101107.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.6.20101107.a
- Fix selinux sub package

* Mon Jan 17 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.5.20101107.a
- Upgrade to latest upstream
- Split package to create selinux package
- Fix Bugzilla bug #668386

* Tue Jan 19 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.4.20091225.c
- Fix CSRF bug Secunia advisory SA38205, dokuwiki bug #1853
- Fix Security ACL bypass bug Secunia advisory SA38183, dokuwiki bug #1847
- Upgrade to the latest upstream
- Fix bugzilla bug #556494

* Tue Dec 15 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.3.20091202.rc
- Fix versioning

* Fri Dec 04 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.1.20091202.rc
- Upgrade to new upstream
- Fix bugzilla bug #544257

* Fri Aug 07 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.2.20090214.b
- Fixes requested by reviewer

* Thu Aug 06 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0-0.1.20090214.b
- Initial package
