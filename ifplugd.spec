Summary:	Detect and perform actions when an ethernet cable is (un)plugged
Summary(pl):	Wykrywanie pod³±czenia/od³±czenia kabla ethernetowego i podejmowanie dzia³añ z tym zwi±zanych
Name:		ifplugd
Version:	0.21b
Release:	1
License:	GPL
Group:		Networking
Source0:	http://www.stud.uni-hamburg.de/~lennart/projects/ifplugd/%{name}-%{version}.tar.gz
# Source0-md5:	b2a17cb82eee12153640937d3dc02cb7
Source1:	%{name}.init
URL:		http://www.stud.uni-hamburg.de/users/lennart/projects/ifplugd/
BuildRequires:	libdaemon-devel >= 0.3
BuildRequires:	lynx
PreReq:		rc-scripts
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
%configure
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
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} service."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop 1>&2
        fi
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
