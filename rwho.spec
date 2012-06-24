Summary:	Displays who is logged in to local network machines
Summary(de):	Anzeige von Login-Infos f�r alle Computer im LAN
Summary(fr):	Affiche les informations de login pour toutes les machines du r�seau local
Summary(pl):	Pokazuje kto jest zalogowany na mszynach w sieci lokalnej
Summary(tr):	A� �zerindeki makinalardaki kullan�c�lar� sorgular
Name:		rwho
Version:	0.17
Release:	1
Copyright:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	rwhod.init
Source2:	rwhod.sysconfig
Patch0:		netkit-rwho-alpha.patch
Requires:	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

%description -l de
Das rwho-Programm zeigt an, welche Anwender auf den Computern im LAN
eingeloggt sind, die den rwho-D�mon ausf�hren. Sowohl der rwho-Client
als auch der D�mon werden mitgeliefert.

%description -l fr
Le programme rwho affiche quels utilisateurs sont connect�s sur les 
machines du r�seau local qui ont lanc� le d�mon rwho. Le client et le
d�mon rwho sont fournis dans ce package.

%description -l tr
rwho hizmetini sunan bir a�daki t�m makinalarda �al��an t�m kullan�c�lar bu
komutla s�ralanabilir. Bu paket hem istemci yaz�l�m�n� hem de sunucu
yaz�l�m�n� i�ermektedir.

%prep
%setup -q -n netkit-rwho-%{version}
%patch -p1

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS -w"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/{etc/{rc.d/init.d,sysconfig},var/spool/rwho}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwhod
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rwhod

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rwhod
if [ -f /var/lock/subsys/rwhod ]; then
	/etc/rc.d/init.d/rwhod restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rwhod start\" to start rwhod server" 1>&2
fi
	
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rwhod ]; then
		/etc/rc.d/init.d/rwhod stop 1>&2
	fi
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
