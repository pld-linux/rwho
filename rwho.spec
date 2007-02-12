Summary:	Displays who is logged in to local network machines
Summary(de.UTF-8):   Anzeige von Login-Infos für alle Computer im LAN
Summary(es.UTF-8):   Enseña la información del login para todas las máquinas en red local
Summary(fr.UTF-8):   Affiche les informations de login pour toutes les machines du réseau local
Summary(pl.UTF-8):   Pokazuje kto jest zalogowany na maszynach w sieci lokalnej
Summary(pt_BR.UTF-8):   Mostra a informação do login para todas as máquinas na rede local
Summary(tr.UTF-8):   Ağ üzerindeki makinalardaki kullanıcıları sorgular
Name:		rwho
Version:	0.17
Release:	16
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	0f71620d45d472f89134ba0d74242e75
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Patch0:		%{name}-alpha.patch
Patch1:		%{name}-bug22014.patch
Patch2:		%{name}-fixbcast.patch
Patch3:		%{name}-fixhostname.patch
Patch4:		%{name}-debian-0.17-8.diff
Patch5:		%{name}-flags-fixes.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	rc-scripts
Provides:	group(rwhod)
Provides:	user(rwhod)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

%description -l de.UTF-8
Das rwho-Programm zeigt an, welche Anwender auf den Computern im LAN
eingeloggt sind, die den rwho-Dämon ausführen. Sowohl der rwho-Client
als auch der Dämon werden mitgeliefert.

%description -l es.UTF-8
El programa rwho enseña cual de los usuarios están logados en las
máquinas de la red local que estén ejecutando el servidor rwho. El
cliente y el servidor se ofrecen en este paquete.

%description -l fr.UTF-8
Le programme rwho affiche quels utilisateurs sont connectés sur les
machines du réseau local qui ont lancé le démon rwho. Le client et le
démon rwho sont fournis dans ce package.

%description -l pl.UTF-8
Polecenie rwho pokazuje, w sposób podobny do who, kto jest zalogowany
w sieci lokalnej na wszystkich maszynach, na których działą demon
rwho.

%description -l pt_BR.UTF-8
O programa rwho mostra quais usuários estão logados nas máquinas da
rede local que estejam rodando o servidor rwho. O cliente e o servidor
são fornecidos neste pacote.

%description -l tr.UTF-8
rwho hizmetini sunan bir ağdaki tüm makinalarda çalışan tüm
kullanıcılar bu komutla sıralanabilir. Bu paket hem istemci yazılımını
hem de sunucu yazılımını içermektedir.

%prep
%setup -q -n netkit-%{name}-%{version}
#%patch0 -p1
%patch4 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

%build
CFLAGS="%{rpmcflags} -w"
LDFLAGS="%{rpmldflags}"
export CFLAGS LDFLAGS
./configure \
	--with-c-compiler="%{__cc}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/spool/rwho}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rwhod
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rwhod

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 174 rwhod
%useradd -u 174 -d /usr/share/empty -s /bin/false -c "rwhod User" -g rwhod rwhod

%post
/sbin/chkconfig --add rwhod
%service rwhod restart "rwhod server"

%preun
if [ "$1" = "0" ]; then
	%service rwhod stop
	/sbin/chkconfig --del rwhod
fi

%postun
if [ "$1" = "0" ]; then
	%userremove rwhod
	%groupremove rwhod
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/rwhod
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man[18]/*

%dir /var/spool/rwho
