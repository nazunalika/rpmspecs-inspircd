## Define global settings
%global _hardened_build 1
%global major_version 3
%global minor_version 8
%global micro_version 0

## Define conditionals
## Change to "without" if needed
%bcond_without contrib

Name:		inspircd
Version:	%{major_version}.%{minor_version}.%{micro_version}
Release:	1%{?dist}
Summary:	Modular Internet Relay Chat server written in C++

Group:		Applications/Communications
License:	GPLv2
URL:		http://www.inspircd.org
Source0:	https://github.com/inspircd/inspircd/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source3:	%{name}.logrotate
Source4:	%{name}.README
Source7:	%{name}.motd.centos
Source8:	%{name}.rules
Source11:	%{name}.motd.fedora

Patch1:		0001-change-readme.patch

Provides:	%{name} = %{version}-%{release}
Provides:	%{name}3

BuildRequires:	perl
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(LWP::Simple)
BuildRequires:	perl(LWP::Protocol::https)
BuildRequires:	perl(Crypt::SSLeay)
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	tre-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	openldap-devel
BuildRequires:	pcre-devel
BuildRequires:	qrencode-devel
BuildRequires:	git
BuildRequires:	libmaxminddb-devel
BuildRequires:	re2-devel

# Default modules
BuildRequires:	openssl-devel
BuildRequires:	gnutls-devel

# I noticed that calling this in any current RHEL pulls whatever is "natural"
# could be mariadb-devel or mysql-devel. Who knows.
BuildRequires:	mysql-devel

## As far as I'm aware, the other packages can be installed
## when the modules are enabled. This is mentioned in the
## README. Essentially, there's no direct requirement for
## the packages we compiled against. We are requring OpenSSL
## by default, however.
Requires:	openssl
Requires:	perl(Getopt::Long)

# Universal requirements
BuildRequires:	systemd
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd

# OS Specific Requirements
%if 0%{?fedora} > 30
BuildRequires: systemd-rpm-macros
%endif

%description
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux,
 BSD, Windows and Mac OS X systems.

It was created from scratch to be stable, modern and lightweight. It avoids a
number of design flaws and performance issues that plague other more 
established projects, such as UnrealIRCd, while providing the same level of
feature parity.

It provides a tunable number of features through the use of an advanced but well
documented module system. By keeping core functionality to a minimum we hope to
increase the stability, security and speed of Inspircd while also making it
customisable to the needs of many different users.

And after all it's free and open source.

%package	devel
Summary:	Inspircd development headers
Requires:	inspircd = %{version}-%{release}

%description	devel
This package contains the development headers required for developing against
inspircd.

################################################################################
# Modules

%package	modules-openssl
Summary:	OpenSSL Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	openssl-libs

%description	modules-openssl
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the openssl module for inspircd. It is recommended to install this
module to allow secure connections to your irc server.

%package	modules-gnutls
Summary:	GnuTLS Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	gnutls

%description	modules-gnutls
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the gnutls module for inspircd. It is recommended to install this
module to allow secure connections to your irc server.

%package	modules-sqlite3
Summary:	SQLite 3 Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	sqlite-libs

%description	modules-sqlite3
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the sqlite3 module for inspircd.

%package	modules-mysql
Summary:	MySQL Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	mysql-libs

%description	modules-mysql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the mysql module for inspircd.

%package	modules-postgresql
Summary:	Postgresql Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	postgresql-libs

%description	modules-postgresql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the postgresql module for inspircd.

%package	modules-ldap
Summary:	LDAP Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	openldap

%description	modules-ldap
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the ldap module for inspircd.

%package        modules-geomaxmind
Summary:	GeoIP Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	libmaxminddb

%description    modules-geomaxmind
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the geomaxmind module for inspircd.

%if %{with contrib}
%package	contrib
Summary:	Contrib modules for inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}

%description	contrib
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the contrib modules from the inspircd-contrib git repo. These modules
are not directly supported by inspircd.
%endif

%prep
%setup -q
%patch -P 1 -p1

# Using module manager to install extras...
%if %{with contrib}
for x in $(./modulemanager list | awk '{print $1}') ; do
  ./modulemanager install $x
done
%endif

%build
# We're no longer supported :(
./configure --enable-extras=m_mysql.cpp,m_pgsql.cpp,m_sqlite3.cpp,m_geo_maxmind.cpp,m_regex_pcre.cpp,m_regex_posix.cpp,m_regex_tre.cpp,m_regex_re2.cpp,m_regex_stdlib.cpp,m_ssl_openssl.cpp,m_sslrehashsignal.cpp,m_ssl_gnutls.cpp

./configure --disable-interactive \
	--disable-auto-extras \
	--distribution-label %{dist} \
	--prefix=%{_datadir}/%{name} \
	--module-dir=%{_libdir}/%{name}/modules \
	--config-dir=%{_sysconfdir}/%{name} \
	--binary-dir=%{_sbindir} \
	--data-dir=%{_sharedstatedir}/%{name} \
	--log-dir=%{_localstatedir}/log/%{name} \
	--example-dir=%{_docdir}/%{name}-%{version}/examples \
	--system \
	--uid $(id -u) \
	--gid $(id -g)

# have to disable rpath, otherwise problems occur
INSPIRCD_DISABLE_RPATH=1 make %{?_smp_mflags}

# Extra documentation
cp %{SOURCE4} %{_builddir}/%{name}-%{version}/README.info

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_libexecdir}/%{name}

%{__install} -pD -m 0644 %{SOURCE3} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

# Symlinks in our home directory
pushd ${RPM_BUILD_ROOT}%{_datadir}/%{name}
	%{__mkdir} bin
	%{__mv} inspircd bin
	%{__ln_s} %{_sysconfdir}/%{name} conf
	%{__ln_s} %{_localstatedir}/log/%{name} logs
	%{__ln_s} %{_libdir}/%{name}/modules modules
	%{__ln_s} %{_sharedstatedir}/%{name} data
popd

# systemd
%{__install} -pD -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_unitdir}/inspircd.service

# development headers
%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_includedir}/%{name}/{modules,threadengines}
%{__install} -m 0644 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0644 include/modules/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/modules
%{__install} -m 0644 include/threadengines/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/threadengines

# default configurations
%{__install} -m 0660 %{SOURCE8} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.rules

# We only plan on building for Enterprise Linux and Fedora
%if 0%{?rhel}
%{__install} -m 0660 %{SOURCE7} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.motd
%else
%{__install} -m 0660 %{SOURCE11} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.motd
%endif

# Log directory
%{__install} -d -m 0700 ${RPM_BUILD_ROOT}%{_localstatedir}/log/%{name}

# Remove some things
rm -f %{buildroot}%{_datadir}/%{name}/.gdbargs

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems that have different package sets.
%{_sbindir}/groupadd -r %{name} 2>/dev/null || :
%{_sbindir}/useradd -r -g %{name} \
	-s /sbin/nologin -d %{_datadir}/inspircd \
	-c 'InspIRCd Service User' inspircd 2>/dev/null || :

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-, root, root, -)
%doc docs/LICENSE.txt docs/Doxyfile docs/sql/* README.md README.info
%doc %{_mandir}/man1/*
%doc %{_docdir}/%{name}-%{version}/examples

# Needs capabilities
%attr(754, %{name}, %{name}) %caps(CAP_NET_BIND_SERVICE=ep) %{_sbindir}/%{name}
%{_sbindir}/%{name}-testssl

%dir %attr(0750,root,inspircd) %{_sysconfdir}/%{name}
%attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/help.txt
# Default configurations
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.motd
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.rules

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%dir %attr(0700,inspircd,inspircd) %{_localstatedir}/log/%{name}
%dir %attr(-,inspircd,inspircd) %{_localstatedir}/lib/%{name}
%dir %{_datadir}/%{name}

%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}/bin
%{_datadir}/%{name}/bin/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/logs
%{_datadir}/%{name}/data
%{_datadir}/%{name}/modules
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}

# All excludes
# Removing some things
%exclude %{_datadir}/%{name}/inspircd.service
%exclude %{_datadir}/%{name}/logrotate
%exclude %{_sbindir}/inspircd-genssl

# Modules
%exclude %{_libdir}/%{name}/modules/m_ssl_*.so
%exclude %{_libdir}/%{name}/modules/m_ldap*.so
%exclude %{_libdir}/%{name}/modules/m_mysql.so
%exclude %{_libdir}/%{name}/modules/m_pgsql.so
%exclude %{_libdir}/%{name}/modules/m_sqlite3.so
%exclude %{_libdir}/%{name}/modules/m_geo_maxmind.so
# Extras
%exclude %{_libdir}/%{name}/modules/m_antirandom.so
%exclude %{_libdir}/%{name}/modules/m_autoaway.so
%exclude %{_libdir}/%{name}/modules/m_autodrop.so
%exclude %{_libdir}/%{name}/modules/m_autokick.so
%exclude %{_libdir}/%{name}/modules/m_bannegate.so
%exclude %{_libdir}/%{name}/modules/m_blockhighlight.so
%exclude %{_libdir}/%{name}/modules/m_blockinvite.so
%exclude %{_libdir}/%{name}/modules/m_checkbans.so
%exclude %{_libdir}/%{name}/modules/m_clientcheck.so
%exclude %{_libdir}/%{name}/modules/m_close.so
%exclude %{_libdir}/%{name}/modules/m_complete.so
%exclude %{_libdir}/%{name}/modules/m_conn_accounts.so
%exclude %{_libdir}/%{name}/modules/m_conn_banner.so
%exclude %{_libdir}/%{name}/modules/m_conn_join_geoip.so
%exclude %{_libdir}/%{name}/modules/m_conn_join_ident.so
%exclude %{_libdir}/%{name}/modules/m_conn_matchident.so
%exclude %{_libdir}/%{name}/modules/m_conn_require.so
%exclude %{_libdir}/%{name}/modules/m_conn_strictsasl.so
%exclude %{_libdir}/%{name}/modules/m_conn_vhost.so
%exclude %{_libdir}/%{name}/modules/m_custompenalty.so
%exclude %{_libdir}/%{name}/modules/m_customtags.so
%exclude %{_libdir}/%{name}/modules/m_discordnick.so
%exclude %{_libdir}/%{name}/modules/m_eventexec.so
%exclude %{_libdir}/%{name}/modules/m_extbanbanlist.so
%exclude %{_libdir}/%{name}/modules/m_extbanredirect.so
%exclude %{_libdir}/%{name}/modules/m_extbanregex.so
%exclude %{_libdir}/%{name}/modules/m_fakelist.so
%exclude %{_libdir}/%{name}/modules/m_forceident.so
%exclude %{_libdir}/%{name}/modules/m_geocmd.so
%exclude %{_libdir}/%{name}/modules/m_globalmessageflood.so
%exclude %{_libdir}/%{name}/modules/m_hideidle.so
%exclude %{_libdir}/%{name}/modules/m_identmeta.so
%exclude %{_libdir}/%{name}/modules/m_join0.so
%exclude %{_libdir}/%{name}/modules/m_joinpartsno.so
%exclude %{_libdir}/%{name}/modules/m_joinpartspam.so
%exclude %{_libdir}/%{name}/modules/m_jumpserver.so
%exclude %{_libdir}/%{name}/modules/m_kill_idle.so
%exclude %{_libdir}/%{name}/modules/m_messagelength.so
%exclude %{_libdir}/%{name}/modules/m_namedstats.so
%exclude %{_libdir}/%{name}/modules/m_nickdelay.so
%exclude %{_libdir}/%{name}/modules/m_nocreate.so
%exclude %{_libdir}/%{name}/modules/m_noidletyping.so
%exclude %{_libdir}/%{name}/modules/m_noprivatemode.so
%exclude %{_libdir}/%{name}/modules/m_nouidnick.so
%exclude %{_libdir}/%{name}/modules/m_opmoderated.so
%exclude %{_libdir}/%{name}/modules/m_qrcode.so
%exclude %{_libdir}/%{name}/modules/m_randomnotice.so
%exclude %{_libdir}/%{name}/modules/m_require_auth.so
%exclude %{_libdir}/%{name}/modules/m_restrictmsg_duration.so
%exclude %{_libdir}/%{name}/modules/m_rotatelog.so
%exclude %{_libdir}/%{name}/modules/m_samove.so
%exclude %{_libdir}/%{name}/modules/m_shed_users.so
%exclude %{_libdir}/%{name}/modules/m_slowmode.so
%exclude %{_libdir}/%{name}/modules/m_solvemsg.so
%exclude %{_libdir}/%{name}/modules/m_stats_unlinked.so
%exclude %{_libdir}/%{name}/modules/m_svsoper.so
%exclude %{_libdir}/%{name}/modules/m_tag_iphost.so
%exclude %{_libdir}/%{name}/modules/m_teams.so
%exclude %{_libdir}/%{name}/modules/m_telegraf.so
%exclude %{_libdir}/%{name}/modules/m_timedstaticquit.so
%exclude %{_libdir}/%{name}/modules/m_totp.so
%exclude %{_libdir}/%{name}/modules/m_xlinetools.so
%exclude %{_libdir}/%{name}/modules/m_zombie.so

# systemd
%{_unitdir}/inspircd.service

# development headers
%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/modules
%dir %{_includedir}/%{name}/threadengines
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/modules/*.h
%{_includedir}/%{name}/threadengines/*.h

%files modules-openssl
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ssl_openssl.so

%files modules-gnutls
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ssl_gnutls.so

%files modules-ldap
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ldapauth.so
%{_libdir}/%{name}/modules/m_ldapoper.so

%files modules-geomaxmind
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_geo_maxmind.so

%files modules-mysql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_mysql.so

%files modules-postgresql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_pgsql.so

%files modules-sqlite3
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_sqlite3.so

%if %{with contrib}
%files contrib
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_antirandom.so
%{_libdir}/%{name}/modules/m_autoaway.so
%{_libdir}/%{name}/modules/m_autodrop.so
%{_libdir}/%{name}/modules/m_autokick.so
%{_libdir}/%{name}/modules/m_bannegate.so
%{_libdir}/%{name}/modules/m_blockhighlight.so
%{_libdir}/%{name}/modules/m_blockinvite.so
%{_libdir}/%{name}/modules/m_checkbans.so
%{_libdir}/%{name}/modules/m_clientcheck.so
%{_libdir}/%{name}/modules/m_close.so
%{_libdir}/%{name}/modules/m_complete.so
%{_libdir}/%{name}/modules/m_conn_accounts.so
%{_libdir}/%{name}/modules/m_conn_banner.so
%{_libdir}/%{name}/modules/m_conn_join_geoip.so
%{_libdir}/%{name}/modules/m_conn_join_ident.so
%{_libdir}/%{name}/modules/m_conn_matchident.so
%{_libdir}/%{name}/modules/m_conn_require.so
%{_libdir}/%{name}/modules/m_conn_strictsasl.so
%{_libdir}/%{name}/modules/m_conn_vhost.so
%{_libdir}/%{name}/modules/m_custompenalty.so
%{_libdir}/%{name}/modules/m_customtags.so
%{_libdir}/%{name}/modules/m_discordnick.so
%{_libdir}/%{name}/modules/m_eventexec.so
%{_libdir}/%{name}/modules/m_extbanbanlist.so
%{_libdir}/%{name}/modules/m_extbanredirect.so
%{_libdir}/%{name}/modules/m_extbanregex.so
%{_libdir}/%{name}/modules/m_fakelist.so
%{_libdir}/%{name}/modules/m_forceident.so
%{_libdir}/%{name}/modules/m_geocmd.so
%{_libdir}/%{name}/modules/m_globalmessageflood.so
%{_libdir}/%{name}/modules/m_hideidle.so
%{_libdir}/%{name}/modules/m_identmeta.so
%{_libdir}/%{name}/modules/m_join0.so
%{_libdir}/%{name}/modules/m_joinpartsno.so
%{_libdir}/%{name}/modules/m_joinpartspam.so
%{_libdir}/%{name}/modules/m_jumpserver.so
%{_libdir}/%{name}/modules/m_kill_idle.so
%{_libdir}/%{name}/modules/m_messagelength.so
%{_libdir}/%{name}/modules/m_namedstats.so
%{_libdir}/%{name}/modules/m_nickdelay.so
%{_libdir}/%{name}/modules/m_nocreate.so
%{_libdir}/%{name}/modules/m_noidletyping.so
%{_libdir}/%{name}/modules/m_noprivatemode.so
%{_libdir}/%{name}/modules/m_nouidnick.so
%{_libdir}/%{name}/modules/m_opmoderated.so
%{_libdir}/%{name}/modules/m_qrcode.so
%{_libdir}/%{name}/modules/m_randomnotice.so
%{_libdir}/%{name}/modules/m_require_auth.so
%{_libdir}/%{name}/modules/m_restrictmsg_duration.so
%{_libdir}/%{name}/modules/m_rotatelog.so
%{_libdir}/%{name}/modules/m_samove.so
%{_libdir}/%{name}/modules/m_shed_users.so
%{_libdir}/%{name}/modules/m_slowmode.so
%{_libdir}/%{name}/modules/m_solvemsg.so
%{_libdir}/%{name}/modules/m_stats_unlinked.so
%{_libdir}/%{name}/modules/m_svsoper.so
%{_libdir}/%{name}/modules/m_tag_iphost.so
%{_libdir}/%{name}/modules/m_teams.so
%{_libdir}/%{name}/modules/m_telegraf.so
%{_libdir}/%{name}/modules/m_timedstaticquit.so
%{_libdir}/%{name}/modules/m_totp.so
%{_libdir}/%{name}/modules/m_xlinetools.so
%{_libdir}/%{name}/modules/m_zombie.so
%endif

%changelog
* Fri Nov 13 2020 Louis Abel <tucklesepk@gmail.com - 3.8.0-1
- Rebuilding to 3.8.0 by request

* Wed Jun 05 2019 Louis Abel <tucklesepk@gmail.com> - 3.1.0-1
- Update to 3.1.0
- Added patches to revert changes that prevented the build

* Mon May 13 2019 Louis Abel <tucklesepk@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Thu May 09 2019 Louis Abel <tucklesepk@gmail.com> - 3.0.0-1
- Rebase to 3.0.0
- Removed modules that are already part of 3.x
- 2.0 modules no longer compiled
- Removed upstream systemd unit
- Moved manual pages

* Mon Feb 25 2019 Louis Abel <tucklesepk@gmail.com> - 2.0.27-3
- Automated webhook build
- Plugin refresh
- Removed extra tar ball, opted for git for extra plugins

* Mon Dec 31 2018 Louis Abel <louis@shootthej.net> - 2.0.27-2
- Added default configs, kept die line to ensure proper config
  is done
- Changed patches to reflect the above change and kept examples
- Redid patches for defaults (examples)

* Thu Nov 08 2018 Louis Abel <louis@shootthej.net> - 2.0.27-1
- Upgrade to 2.0.27

* Fri Nov 02 2018 Louis Abel <louis@shootthej.net> - 2.0.26-3
- Added gnutls support by request
- Updated extras archive

* Thu Nov 01 2018 Louis Abel <louis@shootthej.net> - 2.0.26-2
- Updated modules
- Rebuild for Fedora 29

* Mon May 14 2018 Louis Abel <louis@shootthej.net> - 2.0.26-1
- Rebase to 2.0.26

* Wed May 02 2018 Louis Abel <louis@shootthej.net> - 2.0.25-4
- Rebuild for Fedora 28

* Thu Jan 18 2018 Louis Abel <louis@shootthej.net> - 2.0.25-3
- Separated core modules into separate RPM's
- Fixed logic

* Wed Jan 17 2018 Louis Abel <louis@shootthej.net> - 2.0.25-2
- Rearranged bindir to sbindir
- Rearranged default permissions:
 * Ensured specific files are owned by inspircd
 * All rest owned by root
- Added qrcode support
- Added patches for default config files to remove "conf"

* Sun Nov 12 2017 Louis Abel <louis@shootthej.net> - 2.0.25-1
- Rebase to 2.0.25
- Build for Fedora 27

* Wed Jul 12 2017 Louis Abel <louis@shootthej.net> - 2.0.24-2
- Rebuild for Fedora 26

* Fri May 19 2017 Louis Abel <louis@shootthej.net> - 2.0.24-1
- Rebase to 2.0.24

* Fri Feb 17 2017 Louis Abel <louis@shootthej.net> - 2.0.23-4
- Removed util script
- Changed systemd unit to work with ircd binaries

* Tue Feb 7 2017 Louis Abel <louis@shootthej.net> - 2.0.23-3
- Fixed init script description for EL6

* Tue Nov 1 2016 Louis Abel <louis@shootthej.net> - 2.0.23-2
- Version rebase to 2.0.23
- Combined all compiled modules into a single package
- Removed support for re2 which requires stdlib/c++11

* Sat Apr 9 2016 Louis Abel <louis@shootthej.net> - 2.0.21-2
- Extra plugins package created
- devel package created
- Fixed enable-extras
- Added extra build requirements that were not needed before

* Fri Apr 8 2016 Louis Abel <louis@shootthej.net> - 2.0.21-1
- Initial build for Inspircd 2.0.21

