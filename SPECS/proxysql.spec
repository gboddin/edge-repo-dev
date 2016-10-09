# spec file for proxysql
#
# License: GPL 
# http://opensource.org/licenses/GPL
#
%global _hardened_build 1

# systemd >= 204 with additional service config
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

# Tests fail in mock, not in local build.
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

# Pre-version are only available in github
#global prever       rc3
%global gh_commit    fe71b9a6089b1ac7100120c0c05cda64f59dc31e 
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sysown
%global gh_project   proxysql

Name:             proxysql
Version:          1.2.4
Release:          1%{?dist} 
Summary:          High-performance MySQL proxy with a GPL license. 

Group:            Applications/Databases
License:          GPL
URL:              http://www.proxysql.com
Source0:          https://github.com/sysown/proxysql/archive/v%{version}.tar.gz 
Source1:          %{name}.logrotate
Source2:          %{name}.init
Source3:          %{name}.service
Source4:          %{name}.tmpfiles
Source5:          %{name}-sentinel.init
Source6:          %{name}-sentinel.service
Source7:          %{name}-shutdown
Source8:          %{name}-limit-systemd
Source9:          %{name}-limit-init

%if 0%{?rhel} == 6
Patch0:           build-fix-el6.patch
%endif

# Update configuration for Fedora

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if !0%{?el5}
#BuildRequires:    tcl >= 8.5
%endif
BuildRequires:     cmake, gcc-c++, bison, lynx, flex, openssl-devel

# Required for proxysql-shutdown
#Requires:         /bin/awk
Requires:         logrotate, openssl
Requires(pre):    shadow-utils
%if %{with_systemd}
BuildRequires:    systemd-units
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%else
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%endif

%description
ProxySQL helps you squeeze the last drop of performance out of your MySQL cluster,
without controlling the applications that generate the queries.

ProxySQL quickly jumps in with its advanced rule engine. Results can also be cached 
for a configurable timespan, in native MySQL packets format.

Based on an advanced matching engine, it is able to route queries transparently 
towards the destination cluster that can execute them most efficiently.

It understands the MySQL protocol and acts accordingly. That's why it can easily serve 
advanced use-cases such as sticky transactions or real-time, in-depth statistics 
generation about the workload.

%prep
%if 0%{?prever:1}
%setup -q -n %{gh_project}-%{gh_commit}
%else
%setup -q -n %{name}-%{version}
%endif
%if 0%{?rhel} == 6
%patch0 -p1
%endif

%build

export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} V=1 \
  DEBUG="" \
  LDFLAGS="%{?__global_ldflags}" \
  CFLAGS="$RPM_OPT_FLAGS" 

%check
%if %{with_tests}
make test
%else
: Test disabled, missing '--with tests' option.
%endif

%install
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 %{name}.conf  %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

%if %{with_systemd}
# Install systemd unit
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-sentinel.service
# Install systemd tmpfiles config, _tmpfilesdir only defined in fedora >= 18
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
# this folder requires systemd >= 204
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-sentinel
install -p -D -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Install proxysql-shutdown
install -pDm755 %{SOURCE7} %{buildroot}%{_bindir}/%{name}-shutdown


%post
%if 0%{?systemd_post:1}
%systemd_post proxysql.service
%else
# Initial installation (always, for new service)
/sbin/chkconfig --add proxysql
%endif

%pre
getent group  proxysql &> /dev/null || \
groupadd -r proxysql &> /dev/null
getent passwd proxysql &> /dev/null || \
useradd -r -g proxysql -d %{_sharedstatedir}/proxysql -s /sbin/nologin \
        -c 'ProxySQL Server' proxysql &> /dev/null
exit 0

%preun
%if 0%{?systemd_preun:1}
%systemd_preun proxysql.service
%else
if [ $1 = 0 ]; then
  # Package removal, not upgrade
  /sbin/service proxysql stop &> /dev/null
  /sbin/chkconfig --del proxysql &> /dev/null
fi
%endif

%postun
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart proxysql.service
%else
if [ $1 -ge 1 ]; then
  /sbin/service proxysql          condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc 00-RELEASENOTES BUGS CONTRIBUTING MANIFESTO README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644, proxysql, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644, proxysql, root) %config(noreplace) %{_sysconfdir}/%{name}-sentinel.conf
%dir %attr(0755, proxysql, proxysql) %{_localstatedir}/lib/%{name}
%dir %attr(0755, proxysql, proxysql) %{_localstatedir}/log/%{name}
%dir %attr(0755, proxysql, proxysql) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%if %{with_systemd}
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service
%dir %{_sysconfdir}/systemd/system/%{name}.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%dir %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else
%{_initrddir}/%{name}
%{_initrddir}/%{name}-sentinel
%config(noreplace) %{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif


%changelog
* Sun Oct  9 2016 Gregory Boddin <gregory@siwhine.net> - 1.2.4-1 
- Initial import 

