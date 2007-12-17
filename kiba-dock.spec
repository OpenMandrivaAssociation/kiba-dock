%define name kiba-dock
%define version 0
%define cvs 20070201
%define release %mkrel 0.%{cvs}.6

%define lib_major 0
%define lib_name %mklibname %{name} %lib_major

Name: %name
Version: %version
Release: %release
Summary: Funky application dock for X11
Group: System/X11
URL: http://forums.beryl-project.org/
Source: %{name}-%{cvs}.tar.bz2 
patch0: kiba-dock-fix-python.patch
License: GPL

BuildRequires: libx11-devel >= 1.0.0
BuildRequires: libsvg-cairo-devel
BuildRequires: librsvg-devel
BuildRequires: cairo-devel
BuildRequires: glitz-devel
BuildRequires: pango-devel
BuildRequires: gtk2-devel
BuildRequires: libglade2.0-devel
BuildRequires: glib2-devel
BuildRequires: libpng-devel
BuildRequires: libgnome-desktop-2-devel
BuildRequires: intltool
BuildRequires: libgtop2.0-devel
Requires: gconf-editor
Requires: %{lib_name} = %{version}-%{release}
%description
Funky dock for X11

%files
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/kiba.schemas
%{_bindir}/%{name}
%{_bindir}/akamaru
%{_bindir}/gset-kiba
%{_bindir}/kiba-icon-editor.py
%{_bindir}/kiba-systray.py
%{_bindir}/populate-dock.sh
%py_puresitedir/SimpleGladeApp.py
%{_datadir}/icons/hicolor/*/apps/kiba*.png
%{_datadir}/kiba-dock/*


%package -n %lib_name
Summary: Library files for %{name}
Group: System/X11
Provides: %lib_name = %version

%description -n %lib_name
Library files for %{name}

%post -n %lib_name -p /sbin/ldconfig

%postun -n %lib_name -p /sbin/ldconfig

%files -n %lib_name
%defattr(-,root,root)
%{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/*.la*

#------------------------------------------------------------------------------

%package -n %lib_name-devel
Summary: Development files for %name
Group: Development/X11
Requires: %lib_name = %version

Provides: %{name}-devel
Obsoletes: %{name}-devel

%description -n %lib_name-devel
Development files for %name

%files -n %lib_name-devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/kiba-dock.pc
%{_libdir}/%{name}/*.a

#------------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{cvs}

%if "%py_ver" == "2.5"
%patch0 -p0
%endif

# Fix x86_64 issue
sed -i "s,/usr/lib,%_libdir,g" dock/kiba-dock.c

%build
# This is a CVS snapshot, so we need to generate makefiles.
sh autogen.sh -V

%configure2_5x

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%define schemas kiba
%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%clean
rm -rf %{buildroot}



