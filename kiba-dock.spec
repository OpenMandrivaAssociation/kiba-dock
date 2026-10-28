%define svn	1218
%define release 0.%{svn}.3

Name:		kiba-dock
Version:	0.1
Release:	%{release}1
Summary:	Application dock with advanced graphical effects
Group:		System/X11
URL:		https://www.kiba-dock.org/
Source0:	%{name}-%{svn}.tar.xz
# Fix up menu entries for MDV standards - AdamW 2008/03
Patch0:		kiba-dock-0.1-desktop.patch
patch1:		kiba-dock-1218.glibh.patch
License:	GPLv2+
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pango-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	startup-notification-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	intltool gtk-doc
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	gcc-c++, gcc, gcc-cpp

Requires:	kiba-plugins = %{version}
Obsoletes:	%{mklibname kiba-dock 0} <= %{version}-%{release}

%description
Kiba-Dock is an application dock which uses desktop compositing to
provide advanced graphical effects. A variety of plugins is also
available to extend Kiba-Dock's features.

%package devel
Summary:	Development files for %{name}
Group:		Development/X11
Obsoletes:	%{mklibname kiba-dock 0 -d} <= %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}
%patch 0 -p1 -b .desktop
%patch 1 -p1 -b .glibh
# Autoconf rejects a repeated AC_CONFIG_MACRO_DIR.
sed -i '0,/AC_CONFIG_MACRO_DIR(m4)/b; /AC_CONFIG_MACRO_DIR(m4)/d' configure.ac
# gdk-pixbuf no longer ships the xlib helper. GTK init is enough.
sed -i '/gdk_pixbuf_xlib_init/d' src/main.c

%build
export CC=gcc
export CXX=g++
# This tree relies on implicit GObject prototypes and g_return_if_fail
# in functions that return a value. GCC 16 rejects both by default.
export CFLAGS="%{optflags} -std=gnu17 -Wno-error=implicit-function-declaration -Wno-error=return-mismatch -Wno-error=incompatible-pointer-types -Wno-error=int-conversion"

./autogen.sh
%configure LIBS="-lX11 -ldl"
%make LIBTOOL=slibtool-shared

%install
%makeinstall_std LIBTOOL=slibtool-shared
%find_lang %{name}

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,24x24,48x48,64x64,128x128,scalable}/apps
install -m 0644 icons/kiba_16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 0644 icons/kiba_24.png %{buildroot}%{_iconsdir}/hicolor/24x24/apps/%{name}.png
install -m 0644 icons/kiba_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m 0644 icons/kiba_64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -m 0644 icons/kiba_128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
install -m 0644 icons/kiba-dock.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

# We want the main package to own this dir as various other packages
# might put files into it - AdamW 2008/03
mkdir -p %{buildroot}%{_datadir}/%{name}/config_schemas/plugins

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{_bindir}/kiba-settings
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc



