%global _disable_ld_no_undefined 1

%global libname %{mklibname thrift}
%global devname %{mklibname -d thrift}

Name: thrift
Version: 0.22.0
Release: 1
Source0: https://dlcdn.apache.org/thrift/%{version}/thrift-%{version}.tar.gz
#Patch0: thrift-0.18.1-compilerwarnings.patch
#Patch1: thrift-0.18.1-lua-5.2.patch
Summary: Cross-language service deployment
URL: https://thrift.apache.org/
License: Apache-2.0
Group: System/Libraries
BuildRequires: autoconf automake libtool make
BuildRequires: boost-devel
BuildRequires: boost-static-devel
BuildRequires: golang
BuildRequires: rust cargo
BuildRequires: php-cli
BuildRequires: lua
BuildRequires: pkgconfig(lua)
BuildRequires: nodejs
BuildRequires: python
BuildRequires: pkgconfig(python3)
BuildRequires: mono
# FIXME java is not detected even if jdk-current is added as a
# requirement and JAVA_HOME and PATH are set correctly.
# Probably missing another dependency?
#BuildRequires: jdk-current
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libevent)
Requires: %{libname} = %{EVRD}

%description
The Apache Thrift software framework, for scalable cross-language services
development, combines a software stack with a code generation engine to build
services that work efficiently and seamlessly between C++, Java, Python, PHP,
Ruby, Erlang, Perl, Haskell, C#, Cocoa, JavaScript, Node.js, Smalltalk,
OCaml and Delphi and other languages.

%package -n %{libname}
Summary: Basic libraries for the Thrift cross-language framework
Group: System/Libraries

%description -n %{libname}
Basic libraries for the Thrift cross-language framework

%package -n %{devname}
Summary: Development files the the Thrift cross-language framework
Group: Development/Libraries
Requires: %{libname} = %{EVRD}
Requires: %{name} = %{EVRD}

%description -n %{devname}
Development files the the Thrift cross-language framework

%package -n %{devname}-glib
Summary: Development files the the Thrift cross-language framework glib interface
Group: Development/Libraries
Requires: %{devname} = %{EVRD}

%description -n %{devname}-glib
Development files the the Thrift cross-language framework glib interface

%package -n %{devname}-qt
Summary: Development files the the Thrift cross-language framework Qt interface
Group: Development/Libraries
Requires: %{devname} = %{EVRD}

%description -n %{devname}-qt
Development files the the Thrift cross-language framework Qt interface

%package -n %{libname}-glib
Summary: C (glib) support for the Thrift cross-language framework
Group: Development/C and C++
Requires: %{libname} = %{EVRD}

%description -n %{libname}-glib
C (glib) support for the Thrift cross-language framework

%package -n %{libname}-lua
Summary: Lua support for the Thrift cross-language framework
Group: Development/Lua
Requires: %{libname} = %{EVRD}

%description -n %{libname}-lua
Lua support for the Thrift cross-language framework

%package -n %{libname}-qt
Summary: Qt support for the Thrift cross-language framework
Group: Development/C and C++
Requires: %{libname} = %{EVRD}

%description -n %{libname}-qt
Qt support for the Thrift cross-language framework

%package -n python-%{name}
Summary: Python support for the Thrift cross-language framework
Group: Development/Python
Requires: %{libname} = %{EVRD}

%description -n python-%{name}
Python support for the Thrift cross-language framework

%prep
%autosetup -p1
#. %{_sysconfdir}/profile.d/90java.sh
# FIXME ruby is currently disabled because the build process tries
# to download a custom version of rake and install it to system
# directories (which of course fails as non-root).
# When we have some time, we should fix this instead of disabling ruby.

# FIXME php is currently disabled because the build process relies
# on calling "composer". Where is that supposed to come from?

# FIXME rust (rs) is currently disabled because the build fails
# /usr/bin/cargo fmt --all -- --check
# error: no such command: `fmt`

%configure \
	--without-ruby \
	--without-php \
	--without-rs

%build
#. %{_sysconfdir}/profile.d/90java.sh
%make_build

%install
#. %{_sysconfdir}/profile.d/90java.sh
%make_install

%files
%{_bindir}/thrift

%files -n %{libname}
%{_libdir}/libthrift-%{version}.so
%{_libdir}/libthrift.so*
%{_libdir}/libthriftnb*.so*
%{_libdir}/libthriftz*.so*

%files -n %{libname}-glib
%{_libdir}/libthrift_c_glib*.so*

%files -n %{libname}-lua
%{_libdir}/libluabitwise.so*
%{_libdir}/libluabpack.so*
%{_libdir}/liblualongnumber.so*
%{_libdir}/libluasocket.so*

%files -n %{libname}-qt
%{_libdir}/libthriftqt5*.so*

%files -n python-%{name}
%{py_platsitedir}/thrift*.*-info
%{py_platsitedir}/thrift

%files -n %{devname}
# FIXME %{_includedir}/src is a weird location... Is that really intended?
%{_includedir}/src/socket.h
%dir %{_includedir}/thrift
%{_includedir}/thrift/*.h
%{_includedir}/thrift/async
%{_includedir}/thrift/concurrency
%{_includedir}/thrift/processor
%{_includedir}/thrift/protocol
%{_includedir}/thrift/server
%{_includedir}/thrift/transport
%{_libdir}/pkgconfig/thrift-nb.pc
%{_libdir}/pkgconfig/thrift-z.pc
%{_libdir}/pkgconfig/thrift.pc

%files -n %{devname}-glib
%{_includedir}/thrift/c_glib
%{_libdir}/pkgconfig/thrift_c_glib.pc

%files -n %{devname}-qt
%{_includedir}/thrift/qt
%{_libdir}/pkgconfig/thrift-qt5.pc
