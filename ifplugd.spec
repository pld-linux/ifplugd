Summary:	Detect and perform actions when an ethernet cable is (un)plugged
Summary(pl):	Wykrywanie pod��czenia/od��czenia kabla ethernetowego i podejmowanie dzia�a� z tym zwi�zanych
Name:		ifplugd
Version:	0.16
Release:	1
Source0:	http://www.stud.uni-hamburg.de/~lennart/projects/ifplugd/ifplugd-0.16.tar.gz
# Source0-md5:	56b920b51b05949f8a729e8c3e13ba70
Source1:	%{name}.init
License:	GPL
Group:		Networking
URL:		http://www.stud.uni-hamburg.de/users/lennart/projects/ifplugd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libdaemon-devel >= 0.2
BuildRequires:	lynx

%define		_sbindir	/sbin

%description
ifplugd is a Linux daemon which will automatically configure your
ethernet device when a cable is plugged in and automatically
unconfigure it if the cable is pulled. This is useful on laptops with
onboard network adapters, since it will only configure the interface
when a cable is really connected.

%description -l pl
ifplugd jest demonem linuksowym, kt�ry automatycznie konfiguruje kart�
sieciow� ethernet w chwili pod��czenia do niej kabla i automatycznie
usuwa jej konfiguracj�, gdy kabel jest od��czany. Przydaje si� to w
laptopach z kart� sieciow� na p�ycie, gdy� powoduje to skonfigurowanie
interfejsu tylko wtedy, gdy kabel jest rzeczywi�cie pod��czony.

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
%{_sbindir}/*
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}/ifplugd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ifplugd/ifplugd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ifplugd/ifplugd.action

# end of file
