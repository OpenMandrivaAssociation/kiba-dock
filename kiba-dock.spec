%define svn	1218
%define release %mkrel 0.%{svn}.2

Name:		kiba-dock
Version:	0.1
Release:	%{release}
Summary:	Application dock with advanced graphical effects
Group:		System/X11
URL:		https://www.kiba-dock.org/
Source0:	%{name}-%{svn}.tar.xz
# Fix up menu entries for MDV standards - AdamW 2008/03
Patch0:		kiba-dock-0.1-desktop.patch
patch1:		kiba-dock-1218.glibh.patch
License:	GPLv2+
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	librsvg-devel
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
%patch0 -p1 -b .desktop
%patch1 -p1 -b .glibh

%build
export CC=gcc
export CXX=g++

./autogen.sh
%configure LIBS="-lX11 -ldl"
%make

%install
%makeinstall_std
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



