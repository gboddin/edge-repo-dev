Summary: Tool for generating C-based recognizers from regular expressions
Name: re2c
Version: 0.16
Release: 1%{?dist}
License: Public Domain
Group: Development/Tools
URL: http://re2c.org/
Source: http://downloads.sf.net/re2c/re2c-%{version}.tar.gz

%description
re2c is a tool for writing very fast and very flexible scanners. Unlike any
other such tool, re2c focuses on generating high efficient code for regular
expression matching. As a result this allows a much broader range of use than
any traditional lexer offers. And Last but not least re2c generates warning
free code that is equal to hand-written code in terms of size, speed and
quality.


%prep
%setup -q
# Fix all those executable files, set executable only the ones that need to be
find . -type f -exec chmod -x {} \;
chmod +x configure depcomp install-sh missing


%build
%configure
# Build re2c, then our own scanner.cc, then rebuild the final re2c with it
make %{?_smp_mflags} re2c
rm -f scanner.cc
./re2c -b -o src/scanner.cc src/scanner.re
rm -f re2c src/scanner.o
make %{?_smp_mflags}


%install
install -D -p -m 0755 re2c %{buildroot}%{_bindir}/re2c
install -D -p -m 0644 re2c.1 %{buildroot}%{_mandir}/man1/re2c.1


%files
%doc CHANGELOG README examples/ doc/* lessons/
%{_bindir}/re2c
%{_mandir}/man1/re2c.1*


%changelog
* Wed Apr 13 2016 Ben Boeckel <mathstuf@gmail.com> - 0.16-1
- update to 0.16
- replace %%{__foo} usage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Ben Boeckel <mathstuf@gmail.com> - 0.14.3-1
- update to 0.14.3
- clean out old and unnecessary bits

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.13.5-10
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Matthias Saou <http://freshrpms.net/> 0.13.5-1
- Update to 0.13.5.
- Update URL to the one used in the included spec file.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12.3-2
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Matthias Saou <http://freshrpms.net/> 0.12.3-1
- Update to 0.12.3.

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 0.12.2-1
- Update to 0.12.2.
- Update URL location.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-2
- Fix license tag to "Public Domain".
- Update description with most recent text from the website.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-1
- Spec file changes.

* Wed May 23 2007 Dag Wieers <dag@wieers.com> - 0.12.1-1
- Updated to release 0.12.1.

* Thu May 03 2007 Dag Wieers <dag@wieers.com> - 0.12.0-1
- Initial version.

