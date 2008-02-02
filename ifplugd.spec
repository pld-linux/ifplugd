Summary:	Detect and perform actions when an ethernet cable is (un)plugged
Summary(pl.UTF-8):	Wykrywanie podłączenia/odłączenia kabla ethernetowego i podejmowanie działań z tym związanych
Name:		ifplugd
Version:	0.28
Release:	6
License:	GPL
Group:		Networking
Source0:	http://0pointer.de/lennart/projects/ifplugd/%{name}-%{version}.tar.gz
# Source0-md5:	df6f4bab52f46ffd6eb1f5912d4ccee3
Patch0:		%{name}-pld.patch
Patch1:		%{name}-headers_fix.patch
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://0pointer.de/lennart/projects/ifplugd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdaemon-devel >= 0.5
BuildRequires:	lynx
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
ifplugd is a Linux daemon which will automatically configure your
ethernet device when a cable is plugged in and automatically
unconfigure it if the cable is pulled. This is useful on laptops with
onboard network adapters, since it will only configure the interface
when a cable is really connected.

%description -l pl.UTF-8
ifplugd jest demonem linuksowym, który automatycznie konfiguruje kartę
sieciową ethernet w chwili podłączenia do niej kabla i automatycznie
usuwa jej konfigurację, gdy kabel jest odłączany. Przydaje się to w
laptopach z kartą sieciową na płycie, gdyż powoduje to skonfigurowanie
interfejsu tylko wtedy, gdy kabel jest rzeczywiście podłączony.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
autoreconf
%configure \
	--disable-subversion \
	--disable-xmltoman \
	--with-initdir=/etc/rc.d/init.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service ifplugd restart

%preun
if [ "$1" = "0" ]; then
	%service ifplugd stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc doc/README doc/NEWS doc/README.html doc/style.css
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ifplugd
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/ifplugd
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ifplugd/ifplugd.action
%{_mandir}/man?/*
