Name: spdylay
Version: 1.4.0
Release: 1%{?dist}
Summary: The experimental SPDY protocol version 2 and 3 implementation in C

Group: System Environment/Libraries
License: MIT
URL: http://sourceforge.net/projects/spdylay/
Source0: https://github.com/tatsuhiro-t/spdylay/releases/download/v%{version}/spdylay-%{version}.tar.bz2 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig >= 0.20, zlib >= 1.2.3, gcc, gcc-c++, make
BuildRequires: openssl-devel
%if 0%{?rhel} >= 6
BuildRequires: CUnit-devel
%endif

%description
This is an experimental implementation of Google's SPDY protocol in C.
This library provides SPDY version 2 and 3 framing layer implementation. It does not
perform any I/O operations. When the library needs them, it calls the callback functions
provided by the application. It also does not include any event polling mechanism,
so the application can freely choose the way of handling events. This library code does
not depend on any particular SSL library (except for example programs which depend on
OpenSSL 1.0.1 or later).

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n spdylay-%{version}

%build
%configure --disable-static --enable-examples --disable-xmltest
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la
%if 0%{?rhel} >= 6 
%{_bindir}/shrpx
%{_bindir}/spdycat
%{_bindir}/spdyd
%endif
%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 27 2012 Raul Gutierrez Segales <rgs@itevenworks.net> 0.3.7-DEV
- Initial RPM release.
