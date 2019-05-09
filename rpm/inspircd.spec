## Define global settings
%global _hardened_build 1
%global major_version 3
%global minor_version 0
%global micro_version 0

## Define conditionals
## Change to "without" if needed
%bcond_without all_plugins
%bcond_without mysql
%bcond_without pgsql
%bcond_without sqlite
%bcond_without regex_engines

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
Source6:	%{name}.conf
Source7:	%{name}.motd.centos
Source8:	%{name}.rules
Source9:	%{name}.modules
Source10:	%{name}.opers
Source11:	%{name}.motd.fedora

Provides:	%{name} = %{version}-%{release}
Provides:	%{name}3

BuildRequires:	perl(LWP::Simple)
BuildRequires:	perl(LWP::Protocol::https)
BuildRequires:	perl(Crypt::SSLeay)
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	tre-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(sqlite3)
#BuildRequires:	libmaxminddb-devel
BuildRequires:	openldap-devel
BuildRequires:	pcre-devel
#BuildRequires:	re2-devel
BuildRequires:	qrencode-devel
BuildRequires:	gnutls-devel
BuildRequires:	git

## As far as I'm aware, the other packages can be installed
## when the modules are enabled. This is mentioned in the
## README. Essentially, there's no direct requirement for
## the packages we compiled against. We are requring OpenSSL
## by default, however.
Requires:	openssl
Requires:	perl(Getopt::Long)

# OS Specific Requirements
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:	systemd
BuildRequires:	mariadb-devel
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	systemd
%else
BuildRequires:	mysql-devel
Requires:	initscripts
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

%if %{with sqlite}
%package	modules-sqlite3
Summary:	SQLite 3 Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	sqlite-libs

%description	modules-sqlite3
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the sqlite3 module for inspircd.
%endif

%if %{with mysql}
%package	modules-mysql
Summary:	MySQL Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	mysql-libs

%description	modules-mysql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the mysql module for inspircd.
%endif

%if %{with pgsql}
%package	modules-postgresql
Summary:	Postgresql Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	postgresql-libs

%description	modules-postgresql
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the postgresql module for inspircd.
%endif

%if %{with ldap}
%package	modules-ldap
Summary:	LDAP Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	openldap

%description	modules-ldap
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the ldap module for inspircd.
%endif

%if %{with geomaxmind}
%package        modules-geomaxmind
Summary:	GeoIP Backend Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	libmaxminddb

%description    modules-geomaxmind
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the geomaxmind module for inspircd.
%endif

%if %{with regex_engines}
%package        modules-pcre
Summary:	pcre Regex Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	pcre

%description    modules-pcre
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the pcre module for inspircd.

%package        modules-tre
Summary:	Tre Regex Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}
Requires:	tre

%description    modules-tre
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the tre module for inspircd.

%package        modules-posix
Summary:	POSIX Regex Module for Inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}

%description    modules-posix
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the posix module for inspircd.
%endif

%package	extras
Summary:	Contrib modules for inspircd
Group:		System Environment/Libraries
Requires:	inspircd = %{version}-%{release}

%description	extras
Inspircd is a modular Internet Relay Chat (IRC) server written in C++ for Linux.

This provides the extras modules from the inspircd-extras git repo. These modules
are not directly supported by inspircd.

%prep
%setup -q

## Enable all extras EXCEPT mssql and stdlib
## Doing symlinks instead of calling the configure script

# Clone extras first - the extras don't have a 'release'
git clone https://github.com/inspircd/inspircd-extras.git

pushd src/modules/

%if %{with mysql}
%{__ln_s} -v extra/m_mysql.cpp .
%endif

%if %{with pgsql}
%{__ln_s} -v extra/m_pgsql.cpp .
%endif

%if %{with sqlite}
%{__ln_s} -v extra/m_sqlite3.cpp .
%endif

%if %{with geomaxmind}
%{__ln_s} -v extra/m_geomaxmind.cpp .
%endif

%if %{with regex_engines}
%{__ln_s} -v extra/m_regex_pcre.cpp .
%{__ln_s} -v extra/m_regex_posix.cpp .
%{__ln_s} -v extra/m_regex_tre.cpp .
%endif

%{__ln_s} -v extra/m_ssl_openssl.cpp .
%{__ln_s} -v extra/m_sslrehashsignal.cpp .
%{__ln_s} -v extra/m_ssl_gnutls.cpp .

# Extras will be done here as symlinks
# Start with 3.0 extas not part of 3.0.0 base
for x in \
  m_antirandom.cpp \
  m_autodrop.cpp \
  m_autokick.cpp \
  m_blockhighlight.cpp \
  m_blockinvite.cpp \
  m_checkbans.cpp \
  m_close.cpp \
  m_conn_accounts.cpp \
  m_conn_banner.cpp \
  m_conn_matchident.cpp \
  m_conn_require.cpp \
  m_conn_strictsasl.cpp \
  m_conn_vhost.cpp \
  m_custompenalty.cpp \
  m_extbanbanlist.cpp \
  m_extbanregex.cpp \
  m_forceident.cpp \
  m_globalmessageflood.cpp \
  m_groups.cpp \
  m_hideidle.cpp \
  m_identmeta.cpp \
  m_join0.cpp \
  m_joinpartsno.cpp \
  m_joinpartspam.cpp \
  m_jumpserver.cpp \
  m_kill_idle.cpp \
  m_messagelength.cpp \
  m_namedstats.cpp \
  m_nocreate.cpp \
  m_noprivatemode.cpp \
  m_opmoderated.cpp \
  m_qrcode.cpp \
  m_randomnotice.cpp \
  m_require_auth.cpp \
  m_restrictmsg_duration.cpp \
  m_rotatelog.cpp \
  m_shed_users.cpp \
  m_slowmode.cpp \
  m_solvemsg.cpp \
  m_stats_unlinked.cpp \
  m_svsoper.cpp \
  m_timedstaticquit.cpp \
  m_totp.cpp \
  m_xlinetools.cpp ; do
    %{__ln_s} -v ../../%{name}-extras/3.0/$x .
done

popd

%build

# We're no longer supported :(
%configure --disable-interactive \
	--enable-openssl \
	--enable-gnutls \
	--prefix=%{_datadir}/%{name} \
	--module-dir=%{_libdir}/%{name}/modules \
	--config-dir=%{_sysconfdir}/%{name} \
	--binary-dir=%{_sbindir} \
	--data-dir=%{_sharedstatedir}/%{name} \
	--log-dir=%{_var}/log/%{name} \
	--enable-epoll \
	--disable-kqueue

make %{?_smp_mflags}

# Extra documentation
cp %{SOURCE4} %{_builddir}/%{name}-%{version}/README.info

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_libexecdir}/%{name}

%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE3} \
	${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

# Symlinks in our home directory
pushd ${RPM_BUILD_ROOT}%{_datadir}/%{name}
	%{__mkdir} bin
	%{__mv} inspircd bin
	%{__ln_s} %{_sysconfdir}/%{name} conf
	%{__ln_s} %{_var}/log/%{name} logs
	%{__ln_s} %{_libdir}/%{name}/modules modules
	%{__ln_s} %{_sharedstatedir}/%{name} data
popd

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -m 0644 %{SOURCE1} \
	${RPM_BUILD_ROOT}%{_unitdir}/inspircd.service
%else
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initddir}
%{__install} -m 0755 %{SOURCE2} ${RPM_BUILD_ROOT}%{_initddir}/%{name}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}
%endif

# development headers
%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_includedir}/%{name}/{commands,modules,threadengines}
%{__install} -m 0644 include/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}
%{__install} -m 0644 include/commands/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/commands
%{__install} -m 0644 include/modules/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/modules
%{__install} -m 0644 include/threadengines/*.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}/threadengines

# default configurations
%{__install} -m 0660 %{SOURCE6} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 0660 %{SOURCE8} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.rules
%{__install} -m 0660 %{SOURCE9} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.modules
%{__install} -m 0660 %{SOURCE10} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.opers

# We only plan on building for Enterprise Linux and Fedora
%if 0%{?rhel}
%{__install} -m 0660 %{SOURCE7} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.motd
%else
%{__install} -m 0660 %{SOURCE11} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/%{name}.motd
%endif

%pre
# Since we are not an official Fedora build, we don't get an
# assigned uid/gid. This may make it difficult when installed
# on multiple systems that have different package sets.
%{_sbindir}/groupadd -r %{name} 2>/dev/null || :
%{_sbindir}/useradd -r -g %{name} \
	-s /sbin/nologin -d %{_datadir}/inspircd \
	-c 'Inspircd Server' inspircd 2>/dev/null || :

%preun
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_preun %{name}.service
%else
if [ $1 = 0 ]; then
	[ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} stop
	[ -f %{_initddir}/%{name} ] && chkconfig --del %{name}
fi
%endif

%post
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} >= 7
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge "1" ]; then
	[ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} restart >/dev/null 2>&1
fi
%endif

%files
%defattr(-, root, root, -)
%doc docs/LICENSE.txt docs/Doxyfile docs/sql/* README.md README.info

%{_sbindir}/%{name}
%dir %attr(0750,root,inspircd) %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/examples
%{_sysconfdir}/%{name}/examples/*.example
%dir %{_sysconfdir}/%{name}/examples/services
%{_sysconfdir}/%{name}/examples/services/*.example
%dir %{_sysconfdir}/%{name}/examples/sql
%{_sysconfdir}/%{name}/examples/sql/*.sql

# Default configurations
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.motd
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.rules
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.opers
%config(noreplace) %attr(-,inspircd,inspircd) %{_sysconfdir}/%{name}/%{name}.modules

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*
%dir %attr(0700,inspircd,inspircd) %{_var}/log/%{name}
%dir %attr(-,inspircd,inspircd) %{_var}/lib/%{name}
%dir %{_datadir}/%{name}

# Do I need perms on the symlinks?
%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}/bin
%{_datadir}/%{name}/bin/%{name}
%{_datadir}/%{name}/conf
%{_datadir}/%{name}/logs
%{_datadir}/%{name}/data
%{_datadir}/%{name}/modules
%attr(-,inspircd,inspircd) %{_datadir}/%{name}/.gdbargs
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}

# All excludes
%exclude %{_libdir}/%{name}/modules/m_ssl_gnutls.so
%exclude %{_libdir}/%{name}/modules/m_ssl_openssl.so
%exclude %{_libdir}/%{name}/modules/m_sslrehashsignal.so
%exclude %{_libdir}/%{name}/modules/m_ldap*.so
%exclude %{_libdir}/%{name}/modules/m_regex_*.so
#%exclude %{_libdir}/%{name}/modules/m_geomaxmind.so
%exclude %{_libdir}/%{name}/modules/m_mysql.so
%exclude %{_libdir}/%{name}/modules/m_pgsql.so
%exclude %{_libdir}/%{name}/modules/m_sqlite3.so
# Extras
%exclude %{_libdir}/%{name}/modules/m_antirandom.cpp
%exclude %{_libdir}/%{name}/modules/m_autodrop.cpp
%exclude %{_libdir}/%{name}/modules/m_autokick.cpp
%exclude %{_libdir}/%{name}/modules/m_blockhighlight.cpp
%exclude %{_libdir}/%{name}/modules/m_blockinvite.cpp
%exclude %{_libdir}/%{name}/modules/m_checkbans.cpp
%exclude %{_libdir}/%{name}/modules/m_close.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_accounts.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_banner.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_matchident.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_require.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_strictsasl.cpp
%exclude %{_libdir}/%{name}/modules/m_conn_vhost.cpp
%exclude %{_libdir}/%{name}/modules/m_custompenalty.cpp
%exclude %{_libdir}/%{name}/modules/m_extbanbanlist.cpp
%exclude %{_libdir}/%{name}/modules/m_extbanregex.cpp
%exclude %{_libdir}/%{name}/modules/m_forceident.cpp
%exclude %{_libdir}/%{name}/modules/m_globalmessageflood.cpp
%exclude %{_libdir}/%{name}/modules/m_groups.cpp
%exclude %{_libdir}/%{name}/modules/m_hideidle.cpp
%exclude %{_libdir}/%{name}/modules/m_identmeta.cpp
%exclude %{_libdir}/%{name}/modules/m_join0.cpp
%exclude %{_libdir}/%{name}/modules/m_joinpartsno.cpp
%exclude %{_libdir}/%{name}/modules/m_joinpartspam.cpp
%exclude %{_libdir}/%{name}/modules/m_jumpserver.cpp
%exclude %{_libdir}/%{name}/modules/m_kill_idle.cpp
%exclude %{_libdir}/%{name}/modules/m_messagelength.cpp
%exclude %{_libdir}/%{name}/modules/m_namedstats.cpp
%exclude %{_libdir}/%{name}/modules/m_nocreate.cpp
%exclude %{_libdir}/%{name}/modules/m_noprivatemode.cpp
%exclude %{_libdir}/%{name}/modules/m_opmoderated.cpp
%exclude %{_libdir}/%{name}/modules/m_qrcode.cpp
%exclude %{_libdir}/%{name}/modules/m_randomnotice.cpp
%exclude %{_libdir}/%{name}/modules/m_require_auth.cpp
%exclude %{_libdir}/%{name}/modules/m_restrictmsg_duration.cpp
%exclude %{_libdir}/%{name}/modules/m_rotatelog.cpp
%exclude %{_libdir}/%{name}/modules/m_shed_users.cpp
%exclude %{_libdir}/%{name}/modules/m_slowmode.cpp
%exclude %{_libdir}/%{name}/modules/m_solvemsg.cpp
%exclude %{_libdir}/%{name}/modules/m_stats_unlinked.cpp
%exclude %{_libdir}/%{name}/modules/m_svsoper.cpp
%exclude %{_libdir}/%{name}/modules/m_timedstaticquit.cpp
%exclude %{_libdir}/%{name}/modules/m_totp.cpp
%exclude %{_libdir}/%{name}/modules/m_xlinetools.cpp

# OS Specific
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/inspircd.service
%else
%{_initddir}/inspircd
%{_var}/run/%{name}
%endif

# development headers
%files devel
%defattr (0644,root,root,0755)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/commands
%dir %{_includedir}/%{name}/modules
%dir %{_includedir}/%{name}/threadengines
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/commands/*.h
%{_includedir}/%{name}/modules/*.h
%{_includedir}/%{name}/threadengines/*.h

%files modules-openssl
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ssl_openssl.so
%{_libdir}/%{name}/modules/m_sslrehashsignal.so

%files modules-gnutls
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ssl_gnutls.so

%if %{with ldap}
%files modules-ldap
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_ldapauth.so
%{_libdir}/%{name}/modules/m_ldapoper.so
%endif

%if %{with regex_engines}
%files modules-pcre
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_pcre.so

%files modules-posix
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_posix.so

%files modules-tre
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_regex_tre.so
%endif

%if %{with geomaxmind}
%files modules-geomaxmind
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_geomaxmind.so
%endif

%if %{with mysql}
%files modules-mysql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_mysql.so
%endif

%if %{with pgsql}
%files modules-postgresql
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_pgsql.so
%endif

%if %{with sqlite}
%files modules-sqlite3
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_sqlite3.so
%endif

%files extras
%defattr(-, root, root, -)
%{_libdir}/%{name}/modules/m_antirandom.cpp
%{_libdir}/%{name}/modules/m_autodrop.cpp
%{_libdir}/%{name}/modules/m_autokick.cpp
%{_libdir}/%{name}/modules/m_blockhighlight.cpp
%{_libdir}/%{name}/modules/m_blockinvite.cpp
%{_libdir}/%{name}/modules/m_checkbans.cpp
%{_libdir}/%{name}/modules/m_close.cpp
%{_libdir}/%{name}/modules/m_conn_accounts.cpp
%{_libdir}/%{name}/modules/m_conn_banner.cpp
%{_libdir}/%{name}/modules/m_conn_matchident.cpp
%{_libdir}/%{name}/modules/m_conn_require.cpp
%{_libdir}/%{name}/modules/m_conn_strictsasl.cpp
%{_libdir}/%{name}/modules/m_conn_vhost.cpp
%{_libdir}/%{name}/modules/m_custompenalty.cpp
%{_libdir}/%{name}/modules/m_extbanbanlist.cpp
%{_libdir}/%{name}/modules/m_extbanregex.cpp
%{_libdir}/%{name}/modules/m_forceident.cpp
%{_libdir}/%{name}/modules/m_globalmessageflood.cpp
%{_libdir}/%{name}/modules/m_groups.cpp
%{_libdir}/%{name}/modules/m_hideidle.cpp
%{_libdir}/%{name}/modules/m_identmeta.cpp
%{_libdir}/%{name}/modules/m_join0.cpp
%{_libdir}/%{name}/modules/m_joinpartsno.cpp
%{_libdir}/%{name}/modules/m_joinpartspam.cpp
%{_libdir}/%{name}/modules/m_jumpserver.cpp
%{_libdir}/%{name}/modules/m_kill_idle.cpp
%{_libdir}/%{name}/modules/m_messagelength.cpp
%{_libdir}/%{name}/modules/m_namedstats.cpp
%{_libdir}/%{name}/modules/m_nocreate.cpp
%{_libdir}/%{name}/modules/m_noprivatemode.cpp
%{_libdir}/%{name}/modules/m_opmoderated.cpp
%{_libdir}/%{name}/modules/m_qrcode.cpp
%{_libdir}/%{name}/modules/m_randomnotice.cpp
%{_libdir}/%{name}/modules/m_require_auth.cpp
%{_libdir}/%{name}/modules/m_restrictmsg_duration.cpp
%{_libdir}/%{name}/modules/m_rotatelog.cpp
%{_libdir}/%{name}/modules/m_shed_users.cpp
%{_libdir}/%{name}/modules/m_slowmode.cpp
%{_libdir}/%{name}/modules/m_solvemsg.cpp
%{_libdir}/%{name}/modules/m_stats_unlinked.cpp
%{_libdir}/%{name}/modules/m_svsoper.cpp
%{_libdir}/%{name}/modules/m_timedstaticquit.cpp
%{_libdir}/%{name}/modules/m_totp.cpp
%{_libdir}/%{name}/modules/m_xlinetools.cpp

%changelog
* Thu May 09 2019 Louis Abel <tucklesepk@gmail.com> - 3.0.0-1
- Rebase to 3.0.0
- Removed symlinked modules that are already built in to 3.x
- Created extras package to separate contrib from builtin
  modules
- 2.0 modules no longer compiled

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

