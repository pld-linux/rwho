Summary:	Displays who is logged in to local network machines.
Summary(pl):	Pokazuje kto jest zalogowany na mszynach w sieci lokalnej.
Name:		rwho
Version:	0.10
Release:	25
Copyright:	BSD
Group:		Daemons
Group(pl):	Serwery
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons
Source0:	netkit-rwho-0.10.tar.gz
Source1:	rwhod.init
Source2:	ruptime.tar.gz
Source3:	rwhod.sysconfig
Patch0:		netkit-rwho-misc.patch
Requires:	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

Install the rwho command if you need to keep track of the users who
are logged in to your local network.

%prep
%setup -q -n netkit-rwho-0.10 -a 2
%patch -p1

%build
make OPT_FLAGS="$RPM_OPT_FLAGS -w"
make OPT_FLAGS="$RPM_OPT_FLAGS -w" -C ruptime

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/{bin,sbin}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,8}
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/spool/rwho}

make INSTALLROOT=$RPM_BUILD_ROOT install
make INSTALLROOT=$RPM_BUILD_ROOT install -C ruptime

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwhod
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rwhod

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rwhod

%postun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rwhod
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/rwhod
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man[18]/*

%dir /var/spool/rwho
