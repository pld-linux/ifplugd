Summary:	Detect and perform actions when an ethernet cable is (un)plugged
Summary(pl):	Wykrywanie pod³±czenia/od³±czenia kabla ethernetowego i podejmowanie dzia³añ z tym zwi±zanych
Name:		ifplugd
Version:	0.28
Release:	1
License:	GPL
Group:		Networking
Source0:	http://0pointer.de/lennart/projects/ifplugd/%{name}-%{version}.tar.gz
# Source0-md5:	df6f4bab52f46ffd6eb1f5912d4ccee3
Source1:	%{name}.init
URL:		http://0pointer.de/lennart/projects/ifplugd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdaemon-devel >= 0.5
BuildRequires:	lynx
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
ifplugd is a Linux daemon which will automatically configure your
ethernet device when a cable is plugged in and automatically
unconfigure it if the cable is pulled. This is useful on laptops with
onboard network adapters, since it will only configure the interface
when a cable is really connected.

%description -l pl
ifplugd jest demonem linuksowym, który automatycznie konfiguruje kartê
sieciow± ethernet w chwili pod³±czenia do niej kabla i automatycznie
usuwa jej konfiguracjê, gdy kabel jest od³±czany. Przydaje siê to w
laptopach z kart± sieciow± na p³ycie, gdy¿ powoduje to skonfigurowanie
interfejsu tylko wtedy, gdy kabel jest rzeczywi¶cie pod³±czony.

%prep
%setup -q

%build
autoreconf
%configure \
    --disable-subversion \
    --disable-xmltoman \
    --with-initdir=/etc/rc.d/init.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/ifplugd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ifplugd/ifplugd.conf
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ifplugd/ifplugd.action
