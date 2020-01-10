%define evolution_connector_prefix %{_libdir}/evolution-openldap
%define evolution_connector_includedir %{evolution_connector_prefix}/include
%define evolution_connector_libdir %{evolution_connector_prefix}/%{_lib}
%define check_password_version 1.1

Name: openldap
Version: 2.4.40
Release: 16%{?dist}
Summary: LDAP support libraries
Group: System Environment/Daemons
License: OpenLDAP
URL: http://www.openldap.org/
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: ldap.init
Source2: ldap.sysconfig
Source3: README.evolution
Source4: slapd.conf
Source5: slapd.portreserve
Source6: ldap.conf
Source10: ltb-project-openldap-ppolicy-check-password-%{check_password_version}.tar.gz
Source54: libexec-create-certdb.sh
Source55: libexec-generate-server-cert.sh

# patches for 2.4
Patch0: openldap-manpages.patch
Patch1: openldap-security-pie.patch
Patch2: openldap-sql-linking.patch
Patch3: openldap-reentrant-gethostby.patch
Patch4: openldap-ppolicy-loglevels.patch
Patch5: openldap-smbk5pwd-overlay.patch
Patch6: openldap-ldaprc-currentdir.patch
Patch7: openldap-userconfig-setgid.patch
Patch8: openldap-ssl-deadlock-revert.patch
Patch9: openldap-man-sasl-nocanon.patch
Patch10: openldap-memberof-disallow-global.patch
Patch12: openldap-nss-pk11-freeslot.patch
Patch13: openldap-nss-ignore-certdb-type-prefix.patch
Patch14: openldap-nss-certs-from-certdb-fallback-pem.patch
Patch15: openldap-dns-ipv6-queries.patch
Patch16: openldap-nss-hashed-cacertdir-filename-matching.patch
Patch19: openldap-tls-reqcert-client-manpage.patch
Patch20: openldap-support-tlsv1-and-later.patch
Patch21: openldap-ppc64-crash.patch
# this is a temporary fix for #1144294, it should be solved properly
Patch22: openldap-temporary-ssl-thr-init-race.patch
# CVE-2015-6908, ITS#8240
Patch23: openldap-ITS8240-remove-obsolete-assert.patch
# logically revert ITS#7904 for it breaks as in #1257543
Patch24: openldap-remove-slap_writewait_play.patch
Patch25: openldap-bdb_idl_fetch_key-correct-key-pointer.patch
# ITS#8329
Patch26: openldap-ITS8329-back_sql-id_query.patch
Patch27: openldap-manpages-slapd-conf-TLS.patch
Patch28: openldap-nss-cipher-attributes.patch
Patch29: openldap-nss-ciphers-parsing.patch
Patch30: openldap-nss-ciphers-use-nss-defaults.patch
Patch31: openldap-nss-ciphers-definitions.patch
Patch32: openldap-nss-default-breaks-ssf.patch
Patch34: openldap-nss-protocol-version-new-api.patch
Patch35: openldap-ITS8428-init-sc_writewait.patch
Patch36: openldap-nss-unregister-on-unload.patch
# already in upstream (2.4.41), see ITS#8003
Patch37: openldap-ITS8003-fix-off-by-one-in-LDIF-length.patch
# already in upstream, see ITS#8337
Patch38: openldap-ITS8337-fix-missing-olcDbChecksum-config-attr.patch

# upstream ITS#8484
Patch60: openldap-nss-reregister-nss-shutdown-callback.patch

# check-password module specific patches
Patch90: check-password-makefile.patch
Patch91: check-password.patch
Patch92: check-password-loglevels.patch

# patches for the evolution library (see README.evolution)
Patch200: openldap-evolution-ntlm.patch

# provide a shim libldif for compatibility (its symbols have been merged into libldap)
Patch210: openldap-shim-ldif.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cyrus-sasl-devel >= 2.1, nss-devel, krb5-devel, tcp_wrappers-devel, unixODBC-devel
BuildRequires: glibc-devel, libtool, libtool-ltdl-devel, groff, perl
# smbk5pwd overlay:
BuildRequires: openssl-devel
Requires: nss-tools
Requires(post): rpm, coreutils

Obsoletes: compat-openldap < 2.4
# used by migrationtools:
Provides: ldif2ldbm

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Group: Development/Libraries
Requires: openldap = %{version}-%{release}, cyrus-sasl-devel >= 2.1
Provides: openldap-evolution-devel = %{version}-%{release}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package servers
Summary: LDAP server
License: OpenLDAP
Requires: openldap = %{version}-%{release}, openssl, portreserve
Requires(pre): shadow-utils, initscripts
Requires(post): chkconfig, /sbin/runuser, make, initscripts
Requires(preun): chkconfig, initscripts
BuildRequires: db4-devel >= 4.4, db4-devel < 4.9
BuildRequires: cracklib-devel
Group: System Environment/Daemons

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.

%package servers-sql
Summary: SQL support module for OpenLDAP server
Requires: openldap-servers = %{version}-%{release}
Group: System Environment/Daemons

%description servers-sql
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains a loadable module which the
slapd server can use to read data from an RDBMS.

%package clients
Summary: LDAP client utilities
Requires: openldap = %{version}-%{release}
Group: Applications/Internet

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

%prep
%setup -q -c -a 0 -a 10

# setup tree for openldap

pushd openldap-%{version}

%patch0 -p1 -b .manpages
%patch1 -p1 -b .security-pie
%patch2 -p1 -b .sql-linking
%patch3 -p1 -b .reentrant-gethostby
%patch4 -p1 -b .ppolicy-loglevels
%patch5 -p1 -b .smbk5pwd-overlay
%patch6 -p1 -b .ldaprc-currentdir
%patch7 -p1 -b .userconfig-setgid
%patch8 -p1 -b .ssl-deadlock-revert
%patch9 -p1 -b .man-sasl-nocanon
%patch10 -p1 -b .memberof-disallow-global
%patch12 -p1 -b .nss-leak
%patch13 -p1 -b .nss-ignore-certdb-type-prefix
%patch14 -p1 -b .nss-certs-from-certdb-fallback-pem
%patch15 -p1 -b .dns-ipv6-queries
%patch16 -p1 -b .nss-hashed-cacertdir-filename-matching
%patch19 -p1 -b .tls-reqcert
%patch20 -p1 -b .support-tlsv1-and-later
# XXX: until this is properly fixed, apply on ppc64 only
%ifarch ppc64
%patch21 -p1 -b .ppc64-crash
%endif
%patch22 -p1 -b .temporary-ssl-thr-init-race
%patch23 -p1 -b .ITS8240-remove-obsolete-assert
%patch24 -p1 -b .remove-slap_writewait_play
%patch25 -p1 -b .bdb_idl_fetch_key-correct-key-pointer
%patch26 -p1 -b .ITS8329-back_sql-id_query
%patch27 -p1 -b .manpages-slapd-conf-TLS
%patch28 -p1 -b .nss-cipher-attributes
%patch29 -p1 -b .nss-ciphers-parsing
%patch30 -p1 -b .nss-ciphers-use-nss-defaults
%patch31 -p1 -b .nss-ciphers-definitions
%patch32 -p1 -b .nss-default-breaks-ssf
%patch34 -p1 -b .nss-protocol-version-new-api.patch
%patch35 -p1 -b .ITS8428-init-sc_writewait
%patch36 -p1 -b .nss-unregister-on-unload
%patch37 -p1 -b .ITS8003-fix-off-by-one-in-LDIF-length
%patch38 -p1 -b .ITS8337-fix-missing-olcDbChecksum-config-attr

%patch60 -p1 -b .nss-reregister-nss-shutdown-callback

for subdir in build-servers build-clients ; do
	mkdir $subdir
	ln -s ../configure $subdir
done

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd

popd

pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
%patch90 -p1
%patch91 -p1
%patch92 -p1
popd

# setup tree for openldap with evolution-specific patches

if ! cp -al openldap-%{version} evo-openldap-%{version} ; then
	rm -fr evo-openldap-%{version}
	cp -a  openldap-%{version} evo-openldap-%{version}
fi
pushd evo-openldap-%{version}
%patch200 -p1 -b .evolution-ntlm
popd

%patch210 -p1

%build

libtool='%{_bindir}/libtool'
export tagname=CC

%ifarch ia64
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -O0"
%endif

export CPPFLAGS="-I%_includedir/nss3 -I%_includedir/nspr4"
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS -fno-strict-aliasing -fPIC -D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -DHAVE_TLS -DHAVE_MOZNSS -DSLAPD_LMHASH"
export NSS_LIBS="-lssl3 -lsmime3 -lnss3 -lnssutil3 -lplds4 -lplc4 -lnspr4"
export LIBS=""
export LDFLAGS="$LDFLAGS -Wl,-z,relro"

build() {

%configure \
    --enable-rlookups \
    \
    --with-tls=moznss \
    --with-cyrus-sasl \
    \
    --enable-wrappers \
    \
    --enable-passwd \
    \
    --enable-cleartext \
    --enable-crypt \
    --enable-spasswd \
    --disable-lmpasswd \
    --enable-modules \
    --disable-sql \
    \
    --libexecdir=%{_libdir} \
    $@

# allow #include <nss/file.h> and <nspr/file.h>
pushd include
if [ ! -d nss ] ; then
    ln -s %{_includedir}/nss3 nss
fi
if [ ! -d nspr ] ; then
    ln -s %{_includedir}/nspr4 nspr
fi
popd

make %{_smp_mflags} LIBTOOL="$libtool"

}

# build servers
export LIBS="$NSS_LIBS -lpthread"
pushd openldap-%{version}/build-servers
build \
    --enable-dynamic \
    --enable-syslog \
    \
    --enable-bdb \
    --enable-hdb \
    --enable-ldap \
    --enable-mdb \
    --enable-meta \
    --enable-monitor \
    --disable-ndb \
    --enable-null \
    --enable-passwd \
    --disable-perl \
    --enable-relay \
    --enable-shell \
    --enable-sock \
    --enable-sql=mod \
    \
    --enable-overlays=mod \
    \
    --enable-dynamic \
    --enable-shared \
    \
    --with-pic \
    --with-gnu-ld \
    \
    --libexecdir=%{_libdir}

popd

# build clients
export LIBS="$NSS_LIBS"
pushd openldap-%{version}/build-clients
build \
    --disable-slapd \
    --enable-shared \
    --enable-dynamic \
    --with-pic
popd

# build evolution-specific clients
# (specific patch, different installation directory, no shared libraries)
pushd evo-openldap-%{version}
build \
    --disable-slapd \
    --disable-shared \
    --disable-dynamic \
    --enable-static \
    --with-pic \
    --includedir=%{evolution_connector_includedir} \
    --libdir=%{evolution_connector_libdir}
popd

pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
make LDAP_INC="-I../openldap-%{version}/include \
 -I../openldap-%{version}/servers/slapd \
 -I../openldap-%{version}/build-servers/include"
popd

%install
rm -rf %{buildroot}
libtool='%{_bindir}/libtool'
export tagname=CC

mkdir -p %{buildroot}/%{_libdir}/

# install servers
pushd openldap-%{version}/build-servers
make install DESTDIR=%{buildroot} \
	libdir=%{_libdir} \
	LIBTOOL="$libtool" \
	STRIP=""
popd

# install evolution-specific clients (conflicting files will be overwriten by generic version)
pushd evo-openldap-%{version}
make install DESTDIR=%{buildroot} \
    includedir=%{evolution_connector_includedir} \
    libdir=%{evolution_connector_libdir} \
    LIBTOOL="$libtool" \
    STRIP=""
install -m 644 %SOURCE3 \
    %{buildroot}/%{evolution_connector_prefix}/
popd

# install clients
pushd openldap-%{version}/build-clients
make install DESTDIR=%{buildroot} \
	libdir=%{_libdir} \
	LIBTOOL="$libtool" \
	STRIP=""
popd

# install check_password module
pushd ltb-project-openldap-ppolicy-check-password-%{check_password_version}
mv check_password.so check_password.so.%{check_password_version}
ln -s check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/check_password.so
install -m 755 check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/
install -d -m 755 %{buildroot}%{_sysconfdir}/openldap
cat > %{buildroot}%{_sysconfdir}/openldap/check_password.conf <<EOF
# OpenLDAP pwdChecker library configuration

#useCracklib 1
#minPoints 3
#minUpper 0
#minLower 0
#minDigit 0
#minPunct 0
EOF
mv README{,.check_pwd}
popd

# setup directories for TLS certificates
mkdir -p %{buildroot}%{_sysconfdir}/openldap/certs

# setup data and runtime directories
mkdir -p %{buildroot}/var/lib/ldap
mkdir -p %{buildroot}/var/run/openldap

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}/%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# we don't need the default files -- RPM handles changes
rm -f %{buildroot}/%{_sysconfdir}/openldap/*.default
rm -f %{buildroot}/%{_sysconfdir}/openldap/schema/*.default

# install an init script for the servers
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 %SOURCE1 %{buildroot}%{_sysconfdir}/rc.d/init.d/slapd

# install syconfig/ldap
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/ldap

# install portreserve config
mkdir -p %{buildroot}%{_sysconfdir}/portreserve
install -m 644 %SOURCE5 %{buildroot}%{_sysconfdir}/portreserve/slapd

# install default ldap.conf (customized)
rm -f %{buildroot}%{_sysconfdir}/openldap/ldap.conf
install -m 0644 %SOURCE6 %{buildroot}%{_sysconfdir}/openldap/ldap.conf

# setup maintainance scripts
mkdir -p %{buildroot}%{_libexecdir}
install -m 0755 -d %{buildroot}%{_libexecdir}/openldap
install -m 0755 %SOURCE54 %{buildroot}%{_libexecdir}/openldap/create-certdb.sh
install -m 0755 %SOURCE55 %{buildroot}%{_libexecdir}/openldap/generate-server-cert.sh

# move slapd out of _libdir
mv %{buildroot}/%{_libdir}/slapd %{buildroot}/%{_sbindir}/

# setup tools as symlinks to slapd
rm -f %{buildroot}/%{_sbindir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
rm -f %{buildroot}/%{_libdir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
for X in acl add auth cat dn index passwd test schema; do ln -s slapd %{buildroot}/%{_sbindir}/slap$X ; done

# tweak permissions on the libraries to make sure they're correct
chmod 755 %{buildroot}/%{_libdir}/lib*.so*
chmod 644 %{buildroot}/%{_libdir}/lib*.*a

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
# new configuration will be generated in %post
mkdir -p %{buildroot}/%{_datadir}/openldap-servers
mkdir %{buildroot}/%{_sysconfdir}/openldap/slapd.d
rm -f %{buildroot}/%{_sysconfdir}/openldap/slapd.conf
install -m 644 %SOURCE4 %{buildroot}/%{_datadir}/openldap-servers/slapd.conf.obsolete

# move example configuration
mv %{buildroot}/%{_sysconfdir}/openldap/slapd.ldif %{buildroot}/%{_datadir}/openldap-servers/slapd.ldif.example

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema
mv %{buildroot}%{_sysconfdir}/openldap/DB_CONFIG.example %{buildroot}/%{_datadir}/openldap-servers/DB_CONFIG.example
chmod 0644 openldap-%{version}/servers/slapd/back-sql/rdbms_depend/timesten/*.sh
chmod 0644 %{buildroot}/%{_datadir}/openldap-servers/DB_CONFIG.example

# move all libraries from /usr/lib to /lib for disk-less booting
# devel symlinks will be left in the original location
mkdir -p %{buildroot}/%{_lib}
pushd %{buildroot}/%{_libdir}
# versioned libraries
mv {libldap,libldap_r,liblber,libldif}-*.so* %{buildroot}/%{_lib}
# update devel symlinks
for library in {libldap,libldap_r,liblber,libldif}.so; do
	[ -h $library ] || exit 1
	ln -sf /%{_lib}/$(readlink $library) $library
done
popd

# remove files which we don't want packaged
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{evolution_connector_libdir}/*.la
rm -f %{buildroot}/%{evolution_connector_libdir}/*.so*
rm -f %{buildroot}/%{_libdir}/openldap/*.a
mv %{buildroot}%{_libdir}/openldap/check_password.so{,.tmp}
rm -f %{buildroot}/%{_libdir}/openldap/*.so
mv %{buildroot}%{_libdir}/openldap/check_password.so{.tmp,}

rm -f %{buildroot}%{_localstatedir}/openldap-data/DB_CONFIG.example
rmdir %{buildroot}%{_localstatedir}/openldap-data

%clean 
rm -rf %{buildroot}

%post
/sbin/ldconfig
# create certificate database
%{_libexecdir}/openldap/create-certdb.sh >&/dev/null || :

%postun -p /sbin/ldconfig

%pre servers

# create ldap user and group
getent group ldap >/dev/null || groupadd -r -g 55 ldap
if ! getent passwd ldap >/dev/null; then
	useradd -r -g ldap -u 55 -d %{_sharedstatedir}/ldap -s /sbin/nologin -c "LDAP User" ldap
	# setup ownership of database files
	if [ -d /var/lib/ldap ] ; then
		for dbfile in /var/lib/ldap/* ; do
			if [ -f $dbfile ] ; then
				chown ldap:ldap $dbfile
			fi
		done
	fi
fi

# upgrade
if [ $1 -eq 2 ]; then
	# safe way to migrate the database if version number changed
	# http://www.openldap.org/doc/admin24/maintenance.html

	old_version=$(rpm -q --qf=%%{version} openldap-servers)
	new_version=%{version}

	if [ "$old_version" != "$new_version" ]; then
		pushd %{_sharedstatedir}/ldap &>/dev/null

		# stop the service
		if /sbin/service slapd status &>/dev/null; then
			touch need_start
			/sbin/service slapd stop
		else
			rm -f need_start
		fi

		if ls *.bdb &>/dev/null; then
			# symlink to last backup
			rm -f upgrade.ldif

			# backup location
			backupdir=backup.$(date +%%s)
			backupfile=${backupdir}/backup.ldif
			backupcmd="cp -a"

			mkdir -p ${backupdir}

			# database recovery tool
			# (this is necessary to handle upgrade from old openldap, which had embedded db4)
			if [ -f /usr/sbin/slapd_db_recover ]; then
				db_recover=/usr/sbin/slapd_db_recover
			else
				db_recover=/usr/bin/db_recover
			fi

			# make sure the database is consistent
			runuser -m -s $db_recover -- "ldap" -h %{_sharedstatedir}/ldap &>/dev/null

			# export the database if possible
			if [ $? -eq 0 ]; then
				if [ -f %{_sysconfdir}/openldap/slapd.conf ]; then
					slapcat -f %{_sysconfdir}/openldap/slapd.conf -l $backupfile &>/dev/null
				else
					slapcat -F %{_sysconfdir}/openldap/slapd.d -l $backupfile &>/dev/null
				fi

				if [ $? -eq 0 ]; then
					chmod 0400 $backupfile
					ln -sf $backupfile upgrade.ldif
					backupcmd=mv
				fi
			fi

			# move or copy to backup directory
			find -maxdepth 1 -type f \( -name alock -o -name "*.bdb" -o -name "__db.*" -o -name "log.*" \) \
				| xargs -I '{}' $backupcmd '{}' $backupdir
			cp -af DB_CONFIG $backupdir &>/dev/null

			# show warning
			echo "Check the following directory for database backup location:"
			echo "$(pwd)/$backupdir"

			# fix permissions
			chown -R ldap: $backupdir
			chmod -R a-w $backupdir
		fi

		popd &>/dev/null
	fi
fi

exit 0

%post servers

/sbin/ldconfig
/sbin/chkconfig --add slapd

# generate sample TLS certificates for server (will not replace)
%{_libexecdir}/openldap/generate-server-cert.sh -o &>/dev/null || :

# generate configuration in slapd.d
if ! ls -d %{_sysconfdir}/openldap/slapd.d/* &>/dev/null; then

	# fresh installation
	if [ ! -f %{_sysconfdir}/openldap/slapd.conf ]; then
		# convert from old style config slapd.conf
		mkdir -p %{_sysconfdir}/openldap/slapd.d/
		slaptest -f %{_datadir}/openldap-servers/slapd.conf.obsolete -F %{_sysconfdir}/openldap/slapd.d &>/dev/null
		chown -R ldap:ldap %{_sysconfdir}/openldap/slapd.d
		chmod -R 000 %{_sysconfdir}/openldap/slapd.d
		chmod -R u+rwX,g+rX %{_sysconfdir}/openldap/slapd.d
		rm -f %{_sharedstatedir}/ldap/__db* %{_sharedstatedir}/ldap/alock
	fi
fi

# finish database migration (see %pre)
if [ -f %{_sharedstatedir}/ldap/upgrade.ldif ]; then
	if [ -f %{_sysconfdir}/openldap/slapd.conf ]; then
		runuser -m -s /usr/sbin/slapadd -- ldap -q -f %{_sysconfdir}/openldap/slapd.conf -l %{_sharedstatedir}/ldap/upgrade.ldif &>/dev/null
	else
		runuser -m -s /usr/sbin/slapadd -- ldap -q -F %{_sysconfdir}/openldap/slapd.d -l %{_sharedstatedir}/ldap/upgrade.ldif &>/dev/null
	fi
	rm -f %{_sharedstatedir}/ldap/upgrade.ldif
fi

# restart after upgrade
if [ $1 -ge 1 ]; then
	if [ -f %{_sharedstatedir}/ldap/need_start ]; then
		/sbin/service slapd start
		rm -f %{_sharedstatedir}/ldap/need_start
	else
		/sbin/service slapd condrestart
	fi
fi

exit 0

%preun servers
if [ $1 -eq 0 ] ; then
	/sbin/service slapd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del slapd

	# openldap-servers are being removed from system
	# do not touch the database!
fi

%postun servers
/sbin/ldconfig

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%triggerin servers -- db4

# db4 upgrade (see %triggerun)
if [ $2 -eq 2 ]; then
	pushd %{_sharedstatedir}/ldap &>/dev/null

	# we are interested in minor version changes (both versions of db4 are installed at this moment)
	if [ "$(rpm -q --qf="%%{version}\n" db4 | sed 's/\.[0-9]*$//' | sort -u | wc -l)" != "1" ]; then
		# stop the service
		if /sbin/service slapd status &>/dev/null; then
			touch need_start
			/sbin/service slapd stop
		fi

		# ensure the database is consistent
		runuser -m -s /usr/bin/db_recover -- "ldap" -h %{_sharedstatedir}/ldap &>/dev/null

		# upgrade will be performed after removing old db4
		touch upgrade_db4
	else
		rm -f upgrade_db4
	fi

	popd &>/dev/null
fi

exit 0

%triggerun servers -- db4

# db4 upgrade (see %triggerin)
if [ -f %{_sharedstatedir}/ldap/upgrade_db4 ]; then
	pushd %{_sharedstatedir}/ldap &>/dev/null

	# perform the upgrade
	if ls *.bdb &>/dev/null; then
		runuser -m -s /usr/bin/db_upgrade -- "ldap" -h %{_sharedstatedir}/ldap %{_sharedstatedir}/ldap/*.bdb
		runuser -m -s /usr/bin/db_checkpoint -- "ldap" -h %{_sharedstatedir}/ldap -1
	fi

	# start the service
	if [ -f need_start ]; then
		/sbin/service slapd start
		rm -f need_start
	fi

	rm -f upgrade_db4
	popd &>/dev/null
fi

exit 0

%files
%defattr(-,root,root)
%doc openldap-%{version}/ANNOUNCEMENT
%doc openldap-%{version}/CHANGES
%doc openldap-%{version}/COPYRIGHT
%doc openldap-%{version}/LICENSE
%doc openldap-%{version}/README
%attr(0755,root,root) %dir %{_sysconfdir}/openldap
%attr(0755,root,root) %dir %{_sysconfdir}/openldap/certs
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/ldap*.conf
%attr(0755,root,root) /%{_lib}/libl*-2.4*.so.*
%attr(0644,root,root) %{_mandir}/man5/ldif.5*
%attr(0644,root,root) %{_mandir}/man5/ldap.conf.5*
%{_libexecdir}/openldap/create-certdb.sh

%files servers
%defattr(-,root,root)
%doc openldap-%{version}/contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%doc openldap-%{version}/doc/guide/admin/*.html
%doc openldap-%{version}/doc/guide/admin/*.png
%doc README.schema
%doc ltb-project-openldap-ppolicy-check-password-%{check_password_version}/README.check_pwd
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/slapd
%attr(0750,ldap,ldap) %dir %config(noreplace) %{_sysconfdir}/openldap/slapd.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ldap
%attr(0755,root,root) %dir %config(noreplace) %{_sysconfdir}/openldap/schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.schema*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.ldif
%attr(0644,root,root) %{_sysconfdir}/portreserve/slapd
%attr(0755,root,root) %{_sbindir}/sl*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %{_mandir}/man5/slapd*.5*
%attr(0644,root,root) %{_mandir}/man5/slapo-*.5*
%attr(0700,ldap,ldap) %dir /var/lib/ldap
%attr(0755,ldap,ldap) %dir /var/run/openldap
%attr(0755,root,root) %dir %{_libdir}/openldap
%attr(0755,root,root) %{_libdir}/openldap/[^b]*
%attr(0755,root,root) %dir %{_datadir}/openldap-servers
%attr(0644,root,root) %{_datadir}/openldap-servers/*
%attr(0755,root,root) %{_libdir}/openldap/check_password*
%attr(0640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/check_password.conf
# obsolete configuration
%attr(0640,ldap,ldap) %ghost %config(noreplace,missingok) %{_sysconfdir}/openldap/slapd.conf
%attr(0640,ldap,ldap) %ghost %config(noreplace,missingok) %{_sysconfdir}/openldap/slapd.conf.bak
%{_libexecdir}/openldap/generate-server-cert.sh

%files servers-sql
%defattr(-,root,root)
%doc openldap-%{version}/servers/slapd/back-sql/docs/*
%doc openldap-%{version}/servers/slapd/back-sql/rdbms_depend
%attr(0755,root,root) %{_libdir}/openldap/back_sql*.so.*
%attr(0755,root,root) %{_libdir}/openldap/back_sql.la

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc openldap-%{version}/doc/drafts openldap-%{version}/doc/rfc
%attr(0755,root,root) %{_libdir}/libl*.so
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0755,root,root) %dir %{evolution_connector_prefix}
%attr(0644,root,root)      %{evolution_connector_prefix}/README*
%attr(0755,root,root) %dir %{evolution_connector_includedir}
%attr(0644,root,root)      %{evolution_connector_includedir}/*.h
%attr(0755,root,root) %dir %{evolution_connector_libdir}
%attr(0644,root,root)      %{evolution_connector_libdir}/*.a

%changelog
* Tue Dec  6 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-16
- NSS: re-register NSS_Shutdown callback (#1071520)

* Wed Nov 30 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-15
- ITS#8337 fix missing olcDbChecksum config attr (#1397961)
- ITS#8003 fix off-by-one in LDIF length (#1397949)

* Tue Nov  8 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-14
- NSS: use a hex number for some ciphersuite definitions (#1372357)
- NSS: fix OpenLDAP crash in NSS shutdown handling (#1373222)
- fix: rpm -V openldap-servers complains after a clean install (#1263220)

* Tue Nov  1 2016 Matus Honek <mhonek@redhat.com> - 2.4.40-13
- NSS: fix setting olcTLSProtocolMin (#1249092)
- fix slapd crash in do_search (sc_writewait) (#1340861)
- NSS: fix parsing code (#1372349)
  + refactor ciphers-related patches
  + fix cipherstring parsing
- NSS: fix cipher suites' definitions (#1372357)
  + fix some ciphers' flags
  + add new ciphers to match the current NSS
  + add PSK and CHACHA20POLY1305 cipher strings

* Mon Mar 21 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-12
- fix regression: Including AESGCM ciphers in DEFAULT cipher string breaks SSF (#1300701)

* Tue Mar  8 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-11
- fix: OpenLDAP doesn't use sane (or default) cipher order (#1300701)
  + Add support for TLSv1.2, and SHA256 and SHA384 ciphers
  + Use what NSS considers default for DEFAULT cipher string.
  + Drop unnecessary hardcoded cipher suites' default flags
  + Update with TLSv1.2 ciphers
- revert: check_password minPoints parameter useless (#1255063)

* Wed Jan 20 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-10
- fix: update description in slapd.conf for NSS database related options (#1131094)
- fix: check_password minPoints parameter useless (#1255063)

* Wed Jan 20 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-9
- fix: Bad log levels in check_password module (#1255046)
- [rfe] add informational message about database backup when openldap is updated (#1261651)
- fix: id_query option is not available after rebasing openldap to 2.4.39 (#1288545)
- fix: We can't search expected entries from LDAP server (#1212283)

* Tue Jan 19 2016 Matúš Honěk <mhonek@redhat.com> - 2.4.40-8
- fix: slapd crash in do_search (#1257543)
- Fix: Cannot build the package after libtool rebase (#1296129)

* Tue Sep 29 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-7
- fix: regression: deadlock during SSL_ForceHandshake when getting connection to replica (#1263477)
  + apply (and modify a little) the patch from commit 1eeaeeb7

* Thu Sep 17 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.40-6
- CVE-2015-6908 openldap: ber_get_next denial of service vulnerability (#1263172)

* Thu May 21 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-5
- fix: nslcd segfaults due to incorrect mutex initialization (#1144294)

* Tue Mar 24 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-4
- fix: Updating openldap deletes database if slapd.conf is used (#1193519)

* Fri Mar 20 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-3
- fix: ppc64: slaptest segfault in openldap-2.4.40 (#1202696)

* Mon Mar  9 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-2
- fix: bring back accidentaly removed patch (#1147983)

* Mon Mar  2 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-1
- rebase to 2.4.40 (#1147983)

* Wed Feb 25 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.39-11
- fix: make /etc/openldap/check_password.conf readable by ldap (#1155390)

* Mon Feb  2 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.39-10
- revert previous patch (#1172296)
- fix: crash in ldap_domain2hostlist when processing SRV record (#1164369)
- support TLS 1.1 and later (#1160467)
- enhancement: add ppolicy-check-password (#1155390)

* Mon Jan  5 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.39-9
- fix: prevent freed memory reuse (#1172296)

* Wed Jun 18 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-8
- fix: provide a shim libldif.so (#1110382)

* Wed Jun  4 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-7
- fix: remove correct tmp file when generating server cert (#1102083)

* Tue Apr 22 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-6
- remove unapplied patches

* Tue Apr 22 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-5
- fix: TLS_REQCERT documentation in client manpage (#1027796)

* Thu Mar 27 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-4
- review %%configure and remove nonexistent options

* Mon Mar 24 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-3
- add another missing patch forgotten during the rebase
- fix: enable dynamic linking - unresolved symbols in the smbk5pwd module

* Tue Mar 18 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-2
- add missing patches that were removed by mistake during the rebase

* Thu Mar 13 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-1
- rebase to 2.4.39 (#923680)
  + drop a lot of upstreamed patches, backport the rest
  + compile in mdb
  + remove automatic slapd.conf -> slapd-config conversion

* Thu Jan 23 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.23-35
- fix: segfault on certain queries with rwm overlay (#1003038)

* Tue Jan 21 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.23-34
- fix: deadlock during SSL_ForceHandshake (#996373)
  + revert nss-handshake-threadsafe.patch

* Tue Feb 26 2013 Jan Synáček <jsynacek@redhat.com> 2.4.23-32
- fix: segfault in syncprov overlay (#910241)
- fix: NSS related resource leak (#929358)

* Wed Oct 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-31
- fix update: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#859858)

* Fri Oct 12 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-30
- fix: slapd with rwm overlay segfault following ldapmodify (#864913)

* Tue Sep 25 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-29
- fix: invalid order of TLS shutdown operations (#818572)
- fix: TLS error messages overwriting in tlsm_verify_cert() (#828787)
- fix: reading pin from file can make all TLS connections hang (#829319)
- fix: replication with TLS does not work (#707599)
- fix: some TLS ciphers cannot be enabled (#852339)
- fix: connection hangs after fallback to second server when certificate hostname verification fails (#843056)
- fix: not all certificates in OpenSSL compatible CA certificate directory format are loaded (#811468)
- fix: MozNSS certificate database in SQL format cannot be used (#857390)
- fix: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#859858)
- fix: do not send IPv6 DNS queries when IPv6 is disabled on the host (#835012)
- fix: modification of olcSyncrepl attribute takes server out of MirrorMode (#821848)

* Tue Jul 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-28
- CVE-2012-2668 (#825875)
  + cipher suite selection by name can be ignored
  + default cipher suite is always selected

* Mon Jul 30 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-27
- fix: smbk5pwd module computes invalid LM hashes (#820278)

* Mon May 07 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-26
- fix: MozNSS CA cert dir does not work together with PEM CA cert file (#818844)
- fix: memory leak: def_urlpre is not freed (#816168)
- fix update: Default SSL certificate bundle is not found by openldap library (#742023)

* Wed May 02 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-25
- fix update: Default SSL certificate bundle is not found by openldap library (#742023)

* Mon Apr 30 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-24
- fix update: Default SSL certificate bundle is not found by openldap library (#742023)
- fix: memberof overlay on the frontend database causes server segfault (#730745)

* Fri Apr 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-23
- security fix: CVE-2012-1164: assertion failure by processing search queries
  requesting only attributes for particular entry (#813162)

* Tue Apr 10 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-22
- fix: libraries leak memory when following referrals (#807363)

* Thu Mar 01 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.23-21
- fix: ldapsearch crashes with invalid parameters (#743781)
- fix: replication (syncrepl) with TLS causes segfault (#783445)
- fix: openldap server in MirrorMode sometimes fails to resync via syncrepl (#784211)
- use portreserve to reserve LDAPS port (636/tcp+udp) (#790687)
- fix: missing options in manual pages of client tools (#745470)
- fix: SASL_NOCANON option missing in ldap.conf manual page (#732916)
- fix: slapd segfaults when certificate key cannot be loaded (#796808)
- Jan Synáček <jsynacek@redhat.com>
  + fix: overlay constraint with count option work bad with modify operation (#742163)
  + fix: Default SSL certificate bundle is not found by openldap library (#742023)
  + fix: Duplicate close() calls in OpenLDAP (#784203)

* Tue Oct 04 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-20
- new feature update: honor priority/weight with ldap_domain2hostlist (#730311)
- fix regression: openldap built without tcp_wrappers (#742592)

* Tue Sep 13 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-19
- fix: SSL_ForceHandshake function is not thread safe (#709407)

* Fri Aug 26 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-18
- fix: overlay refint option refint_nothing doesn't function correctly (#725479)
- fix: Unwanted slash printed when installing openldap-servers (#732001)
- manpage fix: TLS options in documentation are not valid for MozNSS (#684810)
- fix: NSS_Init* functions are not thread safe (#731168)
- manpage fix: errors in manual page slapo-unique (#723521) 
- new feature: honor priority/weight with ldap_domain2hostlist (#730311)

* Mon Aug 15 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-17
- fix: strict aliasing warnings during package build (#723487)
- add partial RELRO support for libraries (#723999)
- fix: incorrect behavior of allow/try options of VerifyCert and TLS_REQCERT (#729095)
- fix: memleak - free the return of tlsm_find_and_verify_cert_key (#729087)
- fix: TLS_REQCERT=never ignored when the certificate is expired (#722959)
- fix: matching wildcard hostnames in certificate Subject field does not work (#726984)
- fix: OpenLDAP server segfaults when using back-sql (#727533)
- fix: conversion of constraint overlay settings to cn=config is incorrect (#722923)
- fix: DDS overlay tolerance parametr doesn't function and breakes default TTL (#723514)

* Mon Jul 18 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-16
- fix: memleak in tlsm_auth_cert_handler (#717738)
- fix: segmentation fault of client tool when LDIF input file is not terminated
  by a new line character (#698921)
- fix: segmentation fault of client tool when input line in LDIF file
  is splitted but indented incorrectly (#701227)
- fix: server scriptlets require initscripts package (#712358)
- enable ldapi:/// interface by default
- set cn=config management ACLs for root user, SASL external schema (#712494)
- fix: ldapsearch fails if no CA certificate is available (#713525)

* Wed Apr 13 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-15
- fix: rpm -V fail when upgrading with openldap-devel installed (#693716)
  (remove devel *.so symlinks from /lib and leave them in /usr/lib)

* Fri Mar 18 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-14
- fix update: openldap startup script ignores ulimit settings (#679356)
- fix update: openldap-servers upgrade hangs or do not upgrade the database (#685119)

* Mon Mar 14 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-13
- fix update: openldap can't use TLS after a fork() (#671553)
- fix: possible NULL pointer dereferences in NSS non-blocking patch (#684035)
- fix: move libldif to /lib for consistency (#548475)
- fix: openldap-servers upgrade hangs or do not upgrade the database (#685119)

* Tue Mar 01 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-12
- fix: security - DoS when submitting special MODRDN request (#680975)

* Mon Feb 28 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-11
- fix: CVE-2011-1024 ppolicy forwarded bind failure messages cause success
- fix: CVE-2011-1025 rootpw is not verified for ndb backend
- fix: openldap startup script ignores ulimit settings (#679356)
- fix: add symlinks into /usr/lib*/ (#680139)

* Mon Feb 21 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-10
- fix: add symlinks for libraries moved in 2.4.23-5 to allow building
  packages which require these libraries in the old location (#678105)

* Wed Feb 02 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-9
- fix update: openldap can't use TLS after a fork() (#671553)

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-8
- fix: openldap can't use TLS after a fork() (#671553)

* Thu Jan 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-7
- fix: some server certificates refused with inadequate type error (#669846)
- fix: default encryption strength dropped in switch to using NSS (#669845)

* Thu Jan 13 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-6
- fix update: openldap-devel symlinks to libraries were not moved correctly (#548475)

* Thu Jan 13 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-5
- initscript: slaptest with '-u' to skip database opening (#613966)
- removed slurpd options from sysconfig/ldap
- fix: verification of self issued certificates (#667795)
- fix: move libraries from /usr/lib to /lib (#548475)

* Sat Dec 04 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-4
- rebase to 2.4.23 (Fedora 14) (#644077)
- uses Mozilla NSS instead of OpenSSL for TLS/SSL
- added LDIF (ldif.h) to the public API
- removed embeded Berkeley DB
- removed autofs schema (use up-to-date version from autofs package instead)
- removed compat-openldap subpackage (use separate package instead)
- fixes: ldapsearch -Z hangs server if starttls fails (#652823)
- fixes: improve SSL/TLS log messages (#652819)
- fixes: crash when TLS_CACERTDIR contains a subdirectory (#652817)
- fixes: TLS_CACERTDIR takes precedence over TLS_CACERT (#652816)
- fixes: openldap should ignore files not in the openssl c_hash format in cacertdir (#652814)
- fixes: slapd init script gets stuck in an infinite loop (#644399)
- fixes: Remove lastmod.la from default slapd.conf.bak (#630637)
- fixes: Mozilla NSS - delay token auth until needed (#616558)
- fixes: Mozilla NSS - support use of self signed CA certs as server certs (#616554)

* Fri Jun 25 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-15
- fixed regression caused by tls accept patch (#608112)

* Tue Jun 22 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-14
- fixed segfault issue in modrdn (#606369)

* Fri Jun 18 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.19-13
- implementation of ulimit settings for slapd (#602458)

* Wed May 26 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-12
- updated man pages - only slaptest can convert configuration schema
  (#584787)
- openldap compiled with -fno-strict-aliasing (#596193)

* Thu May 06 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-11
- added compat package

* Tue Apr 27 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-10
- updated overlay list in config file (#586143)
- config dir slapd.d added to package payload (#585276)
- init script now creates only symlink, not harldink, in /var/run (#584870)

* Mon Apr 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-9
- fixed broken link /usr/sbin/slapschema (#583568)
- removed some static libraries from openldap-devel (#583575)

* Fri Apr 16 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-8
- updated spec file - clean files generated by configuration conversion
  (#582327)

* Mon Mar 22 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-7
- updated usage line in init script
- changed return code when calling init script with bad arguments

* Mon Mar 22 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-6
- fixed segfault when using hdb backend (#575403)

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-5
- minor corrections of init script (fedora bugs #571235, #570057, #573804)

* Wed Feb 10 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-4
- removed syncprov.la from config file (#563472)

* Wed Feb 03 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-3
- updated post scriptlet (#561352)

* Mon Nov 23 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-2
- minor changes in init script

* Wed Nov 18 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-1
- fixed tls connection accepting when TLSVerifyClient = allow
- /etc/openldap/ldap.conf removed from files owned by openldap-servers
- minor changes in spec file to supress warnings
- some changes in init script, so it would be possible to use it when
  using old configuration style
- rebased openldap to 2.4.19
- rebased bdb to 4.8.24

* Wed Oct 07 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-5
- updated smbk5pwd patch to be linked with libldap (#526500)

* Wed Sep 30 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-4
- buffer overflow patch from upstream
- added /etc/openldap/slapd.d and /etc/openldap/slapd.conf.bak
  to files owned by openldap-servers

* Thu Sep 24 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-3
- cleanup of previous patch fixing buffer overflow

* Tue Sep 22 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-2
- changed configuration approach. Instead od slapd.conf slapd
  is using slapd.d directory now
- fix of some issues caused by renaming of init script
- fix of buffer overflow issue in ldif.c pointed out by new glibc

* Fri Sep 18 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-1
- rebase of openldap to 2.4.18

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-7
- updated documentation (hashing the cacert dir)

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-6
- updated init script to be LSB-compliant (#523434)
- init script renamed to slapd

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.4.16-5
- rebuilt with new openssl

* Tue Aug 25 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-4
- updated %pre script to correctly install openldap group

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-1
- rebase of openldap to 2.4.16
- fixed minor issue in spec file (output looking interactive
  when installing servers)

* Tue Jun 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-4
- added $SLAPD_URLS variable to init script (#504504)

* Thu Apr 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-3
- extended previous patch (#481310) to remove options cfMP
  from some client tools
- correction of patch setugid (#494330)

* Thu Mar 26 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-2
- removed -f option from some client tools (#481310)

* Wed Feb 25 2009 Jan Safranek <jsafranek@redhat.com> 2.4.15-1
- new upstream release

* Tue Feb 17 2009 Jan Safranek <jsafranek@redhat.com> 2.4.14-1
- new upstream release
- upgraded to db-4.7.25

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.4.12-3
- rebuild with new openssl

* Mon Dec 15 2008 Caolán McNamara <caolanm@redhat.com> 2.4.12-2
- rebuild for libltdl, i.e. copy config.sub|guess from new location

* Wed Oct 15 2008 Jan Safranek <jsafranek@redhat.com> 2.4.12-1
- new upstream release

* Mon Oct 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-3
- add SLAPD_SHUTDOWN_TIMEOUT to /etc/sysconfig/ldap, allowing admins
  to set non-default slapd shutdown timeout
- add checkpoint to default slapd.conf file (#458679)

* Mon Sep  1 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-2
- provide ldif2ldbm functionality for migrationtools
- rediff all patches to get rid of patch fuzz

* Mon Jul 21 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-1
- new upstream release
- apply official bdb-4.6.21 patches

* Wed Jul  2 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-2
- fix CVE-2008-2952 (#453728)

* Thu Jun 12 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-1
- new upstream release

* Wed May 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-5
- use /sbin/nologin as shell of ldap user (#447919)

* Tue May 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-4
- new upstream release
- removed unnecessary MigrationTools patches

* Thu Apr 10 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-4
- bdb upgraded to 4.6.21
- reworked upgrade logic again to run db_upgrade when bdb version
  changes

* Wed Mar  5 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-3
- reworked the upgrade logic, slapcat/slapadd of the whole database
  is needed only if minor version changes (2.3.x -> 2.4.y)
- do not try to save database in LDIF format, if openldap-servers package 
  is  being removed (it's up to the admin to do so manually)

* Thu Feb 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-2
- migration tools carved out to standalone package "migrationtools"
  (#236697)

* Fri Feb 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-1
- new upstream release

* Fri Feb  8 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-7
- fix CVE-2008-0658 (#432014)

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-6
- init script fixes

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-5
- init script made LSB-compliant (#247012)

* Fri Jan 25 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-4
- fixed rpmlint warnings and errors
  - /etc/openldap/schema/README moved to /usr/share/doc/openldap

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-3
- obsoleting compat-openldap properly again :)

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-2
- obsoleting compat-openldap properly (#429591)

* Mon Jan 14 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-1
- new upstream version (openldap-2.4.7)

* Mon Dec  3 2007 Jan Safranek <jsafranek@redhat.com> 2.4.6-1
- new upstream version (openldap-2.4)
- deprecating compat- package

* Mon Nov  5 2007 Jan Safranek <jsafranek@redhat.com> 2.3.39-1
- new upstream release

* Tue Oct 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-4
- fixed multilib issues - all platform independent files have the
  same content now (#342791)

* Thu Oct  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-3
- BDB downgraded back to 4.4.20 because 4.6.18 is not supported by 
  openldap (#314821)

* Mon Sep 17 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-2
- skeleton /etc/sysconfig/ldap added
- new SLAPD_LDAP option to turn off listening on ldap:/// (#292591)
- fixed checking of SSL (#292611)
- fixed upgrade with empty database

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-1
- new upstream version
- added images to the guide.html (#273581)

* Wed Aug 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-3
- just rebuild

* Thu Aug  2 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-2
- do not use specific automake and autoconf
- do not distinguish between NPTL and non-NPTL platforms, we have NPTL
  everywhere
- db-4.6.18 integrated
- updated openldap-servers License: field to reference BDB license

* Tue Jul 31 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-1
- new upstream version

* Fri Jul 20 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-7
- MigrationTools-47 integrated

* Wed Jul  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-6
- fix compat-slapcat compilation. Now it can be found in 
  /usr/lib/compat-openldap/slapcat, because the tool checks argv[0]
  (#246581)

* Fri Jun 29 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-5
- smbk5pwd added (#220895)
- correctly distribute modules between servers and servers-sql packages

* Mon Jun 25 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-4
- Fix initscript return codes (#242667)
- Provide overlays (as modules; #246036, #245896)
- Add available modules to config file

* Tue May 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-3
- do not create script in /tmp on startup (bz#188298)
- add compat-slapcat to openldap-compat (bz#179378)
- do not import ddp services with migrate_services.pl
  (bz#201183)
- sort the hosts by adders, preventing duplicities
  in migrate*nis*.pl (bz#201540)
- start slupd for each replicated database (bz#210155)
- add ldconfig to devel post/postun (bz#240253)
- include misc.schema in default slapd.conf (bz#147805)

* Mon Apr 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-2
- slapadd during package update is now quiet (bz#224581)
- use _localstatedir instead of var/ during build (bz#220970)
- bind-libbind-devel removed from BuildRequires (bz#216851)
- slaptest is now quiet during service ldap start, if
  there is no error/warning (bz#143697)
- libldap_r.so now links with pthread (bz#198226)
- do not strip binaries to produce correct .debuginfo packages
  (bz#152516)

* Mon Feb 19 2007 Jay Fenlason <fenlason<redhat.com> 2.3.34-1
- New upstream release
- Upgrade the scripts for migrating the database so that they might
  actually work.
- change bind-libbind-devel to bind-devel in BuildPreReq

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 2.3.30-1.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Wed Nov 15 2006 Jay Fenlason <fenlason@redhat.com> 2.3.30-1
- New upstream version

* Wed Oct 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.28-1
- New upstream version

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.3.27-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-3
- Include --enable-multimaster to close
  bz#185821: adding slapd_multimaster to the configure options
- Upgade guide.html to the correct one for openladp-2.3.27, closing
  bz#190383: openldap 2.3 packages contain the administrator's guide for 2.2
- Remove the quotes from around the slaptestflags in ldap.init
  This closes one part of
  bz#204593: service ldap fails after having added entries to ldap
- include __db.* in the list of files to check ownership of in
  ldap.init, as suggested in
  bz#199322: RFE: perform cleanup in ldap.init

* Fri Aug 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-2
- New upstream release
- Include the gethostbyname_r patch so that nss_ldap won't hang
  on recursive attemts to ldap_initialize.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.24-2.1
- rebuild

* Wed Jun 7 2006 Jay Fenlason <fenlason@redhat.com> 2.3.24-2
- New upstream version

* Thu Apr 27 2006 Jay Fenlason <fenlason@redhat.com> 2.3.21-2
- Upgrade to 2.3.21
- Add two upstream patches for db-4.4.20

* Mon Feb 13 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-4
- Re-fix ldap.init

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 9 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-3
- Modify the ldap.init script to call runuser correctly.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-2
- Upgrade to 2.3.19, which upstream now considers stable
- Modify the -config.patch, ldap.init, and this spec file to put the
  pid file and args file in an ldap-owned openldap subdirectory under
  /var/run.
- Move back_sql* out of _sbindir/openldap , which requires
  hand-moving slapd and slurpd to _sbindir, and recreating symlinks
  by hand.
- Retire openldap-2.3.11-ads.patch, which went upstream.
- Update the ldap.init script to run slaptest as the ldap user rather
  than as root.  This solves
  bz#150172 Startup failure after database problem
- Add to the servers post and preun scriptlets so that on preun, the
  database is slapcatted to /var/lib/ldap/upgrade.ldif and the
  database files are saved to /var/lib/ldap/rpmorig.  On post, if
  /var/lib/ldap/upgrade.ldif exists, it is slapadded.  This means that
  on upgrades from 2.3.16-2 to higher versions, the database files may
  be automatically upgraded.  Unfortunatly, because of the changes to
  the preun scriptlet, users have to do the slapcat, etc by hand when
  upgrading to 2.3.16-2.  Also note that the /var/lib/ldap/rpmorig
  files need to be removed by hand because automatically removing your
  emergency fallback files is a bad idea.
- Upgrade internal bdb to db-4.4.20.  For a clean upgrade, this will
  require that users slapcat their databases into a temp file, move
  /var/lib/ldap someplace safe, upgrade the openldap rpms, then
  slapadd the temp file.


* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-3
- Remove Requires: cyrus-sasl and cyrus-sasl-md5 from openldap- and
  compat-openldap- to close
  bz#173313 Remove exlicit 'Requires: cyrus-sasl" + 'Requires: cyrus-sasl-md5'

* Thu Nov 10 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-2
- Upgrade to 2.3.11, which upstream now considers stable.
- Switch compat-openldap to 2.2.29
- remove references to nss_ldap_build from the spec file
- remove references to 2.0 and 2.1 from the spec file.
- reorganize the build() function slightly in the spec file to limit the
  number of redundant and conflicting options passedto configure.
- Remove the attempt to hardlink ldapmodify and ldapadd together, since
  the current make install make ldapadd a symlink to ldapmodify.
- Include the -ads patches to allow SASL binds to an Active Directory
  server to work.  Nalin <nalin@redhat.com> wrote the patch, based on my
  broken first attempt.

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.2.29-3
- rebuilt against new openssl

* Mon Oct 10 2005 Jay Fenlason <fenlason@redhat.com> 2.2.29-2
- New upstream version.

* Thu Sep 29 2005 Jay Fenlason <fenlason@redhat.com> 2.2.28-2
- Upgrade to nev upstream version.  This makes the 2.2.*-hop patch obsolete.

* Mon Aug 22 2005 Jay Fenlason <fenlason@redhat.com> 2.2.26-2
- Move the slapd.pem file to /etc/pki/tls/certs
  and edit the -config patch to match to close
  bz#143393  Creates certificates + keys at an insecure/bad place
- also use _sysconfdir instead of hard-coding /etc

* Thu Aug 11 2005 Jay Fenlason <fenlason@redhat.com> 
- Add the tls-fix-connection-test patch to close
  bz#161991 openldap password disclosure issue
- add the hop patches to prevent infinite looping when chasing referrals.
  OpenLDAP ITS #3578

* Fri Aug  5 2005 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in ldap.init (call $klist instead of klist, from Charles Lopes)

* Thu May 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.26-1
- run slaptest with the -u flag if no id2entry db files are found, because
  you can't check for read-write access to a non-existent database (#156787)
- add _sysconfdir/openldap/cacerts, which authconfig sets as the
  TLS_CACERTDIR path in /etc/openldap/ldap.conf now
- use a temporary wrapper script to launch slapd, in case we have arguments
  with embedded whitespace (#158111)

* Wed May  4 2005 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.26 (stable 20050429)
- enable the lmpasswd scheme
- print a warning if slaptest fails, slaptest -u succeeds, and one of the
  directories listed as the storage location for a given suffix in slapd.conf
  contains a readable file named __db.001 (#118678)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.25-1
- update to 2.2.25 (release)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.24-1
- update to 2.2.24 (stable 20050318)
- export KRB5_KTNAME in the init script, in case it was set in the sysconfig
  file but not exported

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-4
- prefer libresolv to libbind

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-3
- add bind-libbind-devel and libtool-ltdl-devel buildprereqs

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 2.2.23-2
- rebuild with openssl-0.9.7e

* Mon Jan 31 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-1
- update to 2.2.23 (stable-20050125)
- update notes on upgrading from earlier versions
- drop slapcat variations for 2.0/2.1, which choke on 2.2's config files

* Tue Jan  4 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.20-1
- update to 2.2.20 (stable-20050103)
- warn about unreadable krb5 keytab files containing "ldap" keys
- warn about unreadable TLS-related files
- own a ref to subdirectories which we create under _libdir/tls

* Tue Nov  2 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.17-0
- rebuild

* Thu Sep 30 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.17 (stable-20040923) (#135188)
- move nptl libraries into arch-specific subdirectories on x86 boxes
- require a newer glibc which can provide nptl libpthread on i486/i586

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com>
- move slapd startup to earlier in the boot sequence (#103160)
- update to 2.2.15 (stable-20040822)
- change version number on compat-openldap to include the non-compat version
  from which it's compiled, otherwise would have to start 2.2.15 at release 3
  so that it upgrades correctly

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-2
- build a separate, static set of libraries for openldap-devel with the
  non-standard ntlm bind patch applied, for use by the evolution-connector
  package (#125579), and installing them under
  evolution_connector_prefix)
- provide openldap-evolution-devel = version-release in openldap-devel
  so that evolution-connector's source package can require a version of
  openldap-devel which provides what it wants

* Mon Jul 26 2004 Nalin Dahyabhai <nalin@redhat.com>
- update administrator guide

* Wed Jun 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-1
- add compat-openldap subpackage
- default to bdb, as upstream does, gambling that we're only going to be
  on systems with nptl now

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-0
- preliminary 2.2.13 update
- move ucdata to the -servers subpackage where it belongs

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-1
- build experimental sql backend as a loadable module

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-0
- update to 2.1.30

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.29-3
- removed rpath
- added pie patch: slapd and slurpd are now pie
- requires libtool >= 1.5.6-2 (PIC libltdl.a)

* Fri Apr 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-2
- move rfc documentation from main to -devel (#121025)

* Wed Apr 14 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-1
- rebuild

* Tue Apr  6 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-0
- update to 2.1.29 (stable 20040329)

* Mon Mar 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- don't build servers with --with-kpasswd, that option hasn't been recognized
  since 2.1.23

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.25-5.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 2.1.25-5
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-4
- remove 'reload' from the init script -- it never worked as intended (#115310)

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-3
- commit that last fix correctly this time

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-2
- fix incorrect use of find when attempting to detect a common permissions
  error in the init script (#114866)

* Fri Jan 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- add bug fix patch for DB 4.2.52

* Thu Jan  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-1
- change logging facility used from daemon to local4 (#112730, reversing #11047)
  BEHAVIOR CHANGE - SHOULD BE MENTIONED IN THE RELEASE NOTES.

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fix for logic quasi-bug in slapd's SASL auxprop code (Dave Jones)

* Thu Dec 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.25, now marked STABLE

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-9
- update to db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-8
- add another section to the ABI note for the TLS libdb so that it's marked as
  not needing an executable stack (from Arjan Van de Ven)

* Thu Oct 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-7
- force bundled libdb to not use O_DIRECT by making it forget that we have it

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- build bundled libdb for slapd dynamically to make the package smaller,
  among other things
- on tls-capable arches, build libdb both with and without shared posix
  mutexes, otherwise just without
- disable posix mutexes unconditionally for db 4.0, which shouldn't need
  them for the migration cases where it's used
- update to MigrationTools 45

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-6.1
- upgrade db-4.1.25 to db-4.2.42.

* Fri Sep 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- drop rfc822-MailMember.schema, merged into upstream misc.schema at some point

* Wed Aug 27 2003 Nalin Dahyabhai <nalin@redhat.com>
- actually require newer libtool, as was intended back in 2.1.22-0, noted as
  missed by Jim Richardson

* Fri Jul 25 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- enable rlookups, they don't cost anything unless also enabled in slapd's
  configuration file

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- build

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-0
- 2.1.22 now badged stable
- be more aggressive in what we index by default
- use/require libtool 1.5

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.22

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- enable ldap, meta, monitor, null, rewrite in slapd

* Mon May 19 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- update to 2.1.20

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- update to 2.1.19

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- switch to db with crypto

* Fri May  2 2003 Nalin Dahyabhai <nalin@redhat.com>
- install the db utils for the bundled libdb as %%{_sbindir}/slapd_db_*
- install slapcat/slapadd from 2.0.x for migration purposes

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17
- disable the shell backend, not expected to work well with threads
- drop the kerberosSecurityObject schema, the krbName attribute it
  contains is only used if slapd is built with v2 kbind support

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-8
- back down to db 4.0.x, which 2.0.x can compile with in ldbm-over-db setups
- tweak SuSE patch to fix a few copy-paste errors and a NULL dereference

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-6
- rebuild

* Mon Dec 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-5
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-4
- check for setgid as well

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fixes from SuSE's security audit, except for fixes to ITS 1963,
  1936, 2007, 2009, which were included in 2.0.26.
- add two more patches for db 4.1.24 from sleepycat's updates page
- use openssl pkgconfig data, if any is available

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-2
- add patches for db 4.1.24 from sleepycat's updates page

* Mon Nov  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- add a sample TLSCACertificateFile directive to the default slapd.conf

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-1
- update to 2.0.27

* Fri Sep 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.26-1
- update to 2.0.26, db 4.1.24.NC

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-2
- change LD_FLAGS to refer to /usr/kerberos/_libdir instead of
  /usr/kerberos/lib, which might not be right on some arches

* Mon Aug 26 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-1
- update to 2.0.25 "stable", ldbm-over-gdbm (putting off migration of LDBM
  slapd databases until we move to 2.1.x)
- use %%{_smp_mflags} when running make
- update to MigrationTools 44
- enable dynamic module support in slapd

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-5
- rebuild in new environment

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-3
- use the gdbm backend again

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-2
- make slapd.conf read/write by root, read by ldap

* Sun Feb 17 2002 Nalin Dahyabhai <nalin@redhat.com>
- fix corner case in sendbuf fix
- 2.0.23 now marked "stable"

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-1
- update to 2.0.23

* Fri Feb  8 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-2
- switch to an internalized Berkeley DB as the ldbm back-end  (NOTE: this breaks
  access to existing on-disk directory data)
- add slapcat/slapadd with gdbm for migration purposes
- remove Kerberos dependency in client libs (the direct Kerberos dependency
  is used by the server for checking {kerberos} passwords)

* Fri Feb  1 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-1
- update to 2.0.22

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.0.21-5
- prereq chkconfig for server subpackage

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-4
- update migration tools to version 40

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-3
- free ride through the build system

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-2
- update to 2.0.21, now earmarked as STABLE

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-2
- temporarily disable optimizations for ia64 arches
- specify pthreads at configure-time instead of letting configure guess

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- and one for Raw Hide

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-0.7
- build for RHL 7/7.1

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-1
- update to 2.0.20 (security errata)

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.19-1
- update to 2.0.19

* Tue Nov  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-2
- fix the commented-out replication example in slapd.conf

* Fri Oct 26 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-1
- update to 2.0.18

* Mon Oct 15 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.17-1
- update to 2.0.17

* Wed Oct 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable kbind support (deprecated, and I suspect unused)
- configure with --with-kerberos=k5only instead of --with-kerberos=k5
- build slapd with threads

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-2
- rebuild, 2.0.15 is now designated stable

* Fri Sep 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-1
- update to 2.0.15

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.14-1
- update to 2.0.14

* Fri Aug 31 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.12-1
- update to 2.0.12 to pull in fixes for setting of default TLS options, among
  other things
- update to migration tools 39
- drop tls patch, which was fixed better in this release

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.11-13
- install saucer correctly

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to fix ldap_set_options not being able to set global options related
  to TLS correctly

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't attempt to create a cert at install-time, it's usually going
  to get the wrong CN (#51352)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a build-time requirement on pam-devel
- add a build-time requirement on a sufficiently-new libtool to link
  shared libraries to other shared libraries (which is needed in order
  for prelinking to work)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- require cyrus-sasl-md5 (support for DIGEST-MD5 is required for RFC
  compliance) by name (follows from #43079, which split cyrus-sasl's
  cram-md5 and digest-md5 modules out into cyrus-sasl-md5)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable passwd back-end (noted by Alan Sparks and Sergio Kessler)

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- start to prep for errata release

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- link libldap with liblber

* Wed Jul  4 2001 Than Ngo <than@redhat.com> 2.0.11-6
- add symlink liblber.so libldap.so and libldap_r.so in /usr/lib

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib
- redo init script for better internationalization (#26154)
- don't use ldaprc files in the current directory (#38402) (patch from
  hps@intermeta.de)
- add BuildPrereq on tcp wrappers since we configure with
  --enable-wrappers (#43707)
- don't overflow debug buffer in mail500 (#41751)
- don't call krb5_free_creds instead of krb5_free_cred_contents any
  more (#43159)

* Mon Jul  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- make config files noreplace (#42831)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually change the default config to use the dummy cert
- update to MigrationTools 38

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- build dummy certificate in %%post, use it in default config
- configure-time shenanigans to help a confused configure script

* Wed Jun 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak migrate_automount and friends so that they can be run from anywhere

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.11

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.10

* Mon May 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.9

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.8
- drop patch which came from upstream

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- back out pidfile patches, which interact weirdly with Linux threads
- mark non-standard schema as such by moving them to a different directory

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to MigrationTools 36, adds netgroup support

* Mon Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix thinko in that last patch

* Thu Jan 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to work around some buffering problems

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Fri Jan 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- move the RFCs to the base package (#21701)
- update to MigrationTools 34

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- add support for additional OPTIONS, SLAPD_OPTIONS, and SLURPD_OPTIONS in
  a /etc/sysconfig/ldap file (#23549)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object OID from 1.3.6.1.1.1.2.9 to 1.3.6.1.1.1.2.13,
  per mail from the ldap-nis mailing list

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC so that shared libraries don't fall over

* Mon Dec  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Norbert Klasen's patch (via Del) to fix searches using ldaps URLs
  (OpenLDAP ITS #889)
- add "-h ldaps:///" to server init when TLS is enabled, in order to support
  ldaps in addition to the regular STARTTLS (suggested by Del)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- correct mismatched-dn-cn bug in migrate_automount.pl

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the correct OIDs for automount and automountInformation
- add notes on upgrading

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.7
- drop chdir patch (went mainstream)

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object classes from auxiliary to structural

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to Migration Tools 27
- change the sense of the last simple patch

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- reorganize the patch list to separate MigrationTools and OpenLDAP patches
- switch to Luke Howard's rfc822MailMember schema instead of the aliases.schema
- configure slapd to run as the non-root user "ldap" (#19370)
- chdir() before chroot() (we don't use chroot, though) (#19369)
- disable saving of the pid file because the parent thread which saves it and
  the child thread which listens have different pids

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add missing required attributes to conversion scripts to comply with schema
- add schema for mail aliases, autofs, and kerberosSecurityObject rooted in
  our own OID tree to define attributes and classes migration scripts expect
- tweak automounter migration script

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- try adding the suffix first when doing online migrations
- force ldapadd to use simple authentication in migration scripts
- add indexing of a few attributes to the default configuration
- add commented-out section on using TLS to default configuration

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.6
- add buildprereq on cyrus-sasl-devel, krb5-devel, openssl-devel
- take the -s flag off of slapadd invocations in migration tools
- add the cosine.schema to the default server config, needed by inetorgperson

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the nis.schema and inetorgperson.schema to the default server config
- make ldapadd a hard link to ldapmodify because they're identical binaries

* Fri Sep 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.4

* Fri Sep 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove prereq on /etc/init.d (#17531)
- update to 2.0.3
- add saucer to the included clients

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.1

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.0
- patch to build against MIT Kerberos 1.1 and later instead of 1.0.x

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove that pesky default password
- change "Copyright:" to "License:"

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- adjust permissions in files lists
- move libexecdir from %%{_prefix}/sbin to %%{_sbindir}

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add migrate_automount.pl to the migration scripts set

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- build a semistatic slurpd with threads, everything else without
- disable reverse lookups, per email on OpenLDAP mailing lists
- make sure the execute bits are set on the shared libraries

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- change logging facility used from local4 to daemon (#11047)

* Thu Jul 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off clients and servers to shrink down the package and remove the
  base package's dependency on Perl
- make certain that the binaries have sane permissions

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the init script back

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the init script to only source /etc/sysconfig/network if it's found

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to gdbm; I'm getting off the db merry-go-round
- tweak the init script some more
- add instdir to @INC in migration scripts

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak init script to return error codes properly
- change initscripts dependency to one on /etc/init.d

* Tue Jul  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- prereq initscripts
- make migration scripts use mktemp

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- do condrestart in post and stop in preun
- move init script to /etc/init.d

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.11
- add condrestart logic to init script
- munge migration scripts so that you don't have to be 
  /usr/share/openldap/migration to run them
- add code to create pid files in /var/run

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS tweaks
- fix for compiling with libdb2

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- minor tweak so it builds on ia64

* Wed May  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- more minimalistic fix for bug #11111 after consultation with OpenLDAP team
- backport replacement for the ldapuser patch

* Tue May  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix segfaults from queries with commas in them in in.xfingerd (bug #11111)

* Tue Apr 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.10
- add revamped version of patch from kos@bastard.net to allow execution as
  any non-root user
- remove test suite from %%build because of weirdness in the build system

* Wed Apr 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the defaults for databases and whatnot to /var/lib/ldap (bug #10714)
- fix some possible string-handling problems

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- start earlier, stop later.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- auto rebuild in new environment (release 4)

* Tue Feb  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add -D_REENTRANT to make threaded stuff more stable, even though it looks
  like the sources define it, too
- mark *.ph files in migration tools as config files

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.9

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- update to 1.2.7
- fix some bugs from bugzilla (#4885, #4887, #4888, #4967)
- take include files out of base package

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- missing ;; in init script reload) (#4734).

* Tue Aug 24 1999 Cristian Gafton <gafton@redhat.com>
- move stuff from /usr/libexec to /usr/sbin
- relocate config dirs to /etc/openldap

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- add the migration tools to the package

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- upgrade to 1.2.6
- add rc.d script
- split -devel package

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to latest stable (1.1.4), it now uses configure macro.

* Fri Jan 15 1999 Bill Nottingham <notting@redhat.com>
- build on arm, glibc2.1

* Wed Oct 28 1998 Preston Brown <pbrown@redhat.com>
- initial cut.
- patches for signal handling on the alpha
