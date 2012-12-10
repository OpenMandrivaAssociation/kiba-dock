%define svn	1218
%define release %mkrel 0.%{svn}.2

Name:		kiba-dock
Version:	0.1
Release:	%{release}
Summary:	Application dock with advanced graphical effects
Group:		System/X11
URL:		http://www.kiba-dock.org/
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
buildrequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
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
./autogen.sh
%configure2_5x LIBS="-lX11 -ldl"
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



%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.1218.2mdv2011.0
+ Revision: 612602
- the mass rebuild of 2010.1 packages

* Sun Jan 31 2010 Funda Wang <fwang@mandriva.org> 0.1-0.1218.1mdv2010.1
+ Revision: 498700
- New snapshot
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Aug 15 2008 Adam Williamson <awilliamson@mandriva.org> 0.1-0.862.1mdv2009.0
+ Revision: 272467
- drop pthread.patch (merged upstream)
- new snapshot 862

* Thu Mar 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.1-0.722.1mdv2008.1
+ Revision: 180268
- add desktop.patch (fix up menu entries)
- add pthread.patch (need to add -lpthread to build options)
- drop old fix-python.patch (no longer relevant)
- basically rip and replace entire spec file as everything's changed
- update to latest svn, bump version to 0.1 (arbitrary)

* Wed Mar 05 2008 Adam Williamson <awilliamson@mandriva.org> 0-0.20070201.7mdv2008.1
+ Revision: 180201
- don't provide and obsolete %%name-devel anymore, as I'm about to upload a new and improved version which uses %%name-devel again

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0-0.20070201.6mdv2008.1
+ Revision: 136523
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Tue Mar 27 2007 Colin Guthrie <cguthrie@mandriva.org> 0-0.20070201.6mdv2007.1
+ Revision: 149039
- Make sure the main package requires it plugins/libraries

* Wed Feb 07 2007 Colin Guthrie <cguthrie@mandriva.org> 0-0.20070201.5mdv2007.1
+ Revision: 117258
- Fix usage on x86_64

* Wed Feb 07 2007 Lev Givon <lev@mandriva.org> 0-0.20070201.4mdv2007.1
+ Revision: 117250
- Rebuild.
- Change devel(libgtop-2.0) buildreq to libgtop2.0-devel so that the
  package can build on x86_64.
- Add librsvg-devel buildreq.
  Check Python version before patching so that the package can build on 2007.0.

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Add patch0: fix python installation

  + Sébastien Savarin <plouf@mandriva.org>
    - realy add macro for python
    - add macro for python
    - Add deps on gconf-editor
    - Sync with cvs 20070201

  + Colin Guthrie <cguthrie@mandriva.org>
    - Rebuild
    - Fix version number.
    - Import kiba-dock

