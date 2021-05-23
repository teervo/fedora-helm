Name:           helm
Version:        0.9.0 
Release:        1%{?dist}
Summary:        Helm is a free polyphonic synth with lots of modulation

License:        GPL-3.0
URL:            http://tytel.org/helm
Source0:        https://github.com/mtytel/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.appdata.xml
Patch0:         00-gcc-9.1.compatibility-fixes.patch

BuildRequires:  lv2-devel libX11-devel alsa-lib-devel libXext-devel libXinerama-devel freetype-devel libcurl-devel mesa-libGL-devel jack-audio-connection-kit-devel libXcursor-devel gcc-c++ libappstream-glib
Requires:       freetype libXext mesa-libGL

%package -n lv2-%{name}
Summary:        Helm LV2 plugin is a free polyphonic synth with lots of modulation
Requires:       lv2 freetype libXext mesa-libGL

%description
Helm is a free, cross-platform, polyphonic synthesizer that runs on GNU/Linux,
Mac, and Windows as a standalone program and as a LV2/VST/AU/AAX plugin.
You can install helm (standalone), or lv2-helm that is LV2 plugin.


%description -n lv2-%{name}
Helm is a free, cross-platform, polyphonic synthesizer that runs on GNU/Linux,
Mac, and Windows as a standalone program and as a LV2/VST/AU/AAX plugin.
This package installs the LV2 plugin.

%prep
%autosetup -p1

%build
%configure
%make_build standalone
%make_build lv2

%install
rm -rf $RPM_BUILD_ROOT
%make_install standalone
%make_install lv2
mkdir -p $RPM_BUILD_ROOT/%{_libdir}

# doesn't need that at this time, maybe later ?
rm -rf $RPM_BUILD_ROOT/usr/lib/debug
rm -rf $RPM_BUILD_ROOT/usr/lib/lxvst

# helm badly installs lv2 in /usr/lib, we prefer /usr/lib64 on x86_64
%ifarch x86_64
cp -ra $RPM_BUILD_ROOT/usr/lib/* $RPM_BUILD_ROOT/%{_libdir}
rm -rf $RPM_BUILD_ROOT/usr/lib
%endif

# install appdata file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml


%files -n lv2-%{name}
%doc %{_mandir}
%{_libdir}/lv2
%{_datadir}/doc
%{_datadir}/helm
%{_datadir}/applications
%{_metainfodir}/%{name}.appdata.xml

%files
%doc %{_mandir}
%{_datadir}/doc
%{_datadir}/helm
%{_datadir}/applications
%{_datadir}/icons
%{_bindir}/helm
%{_metainfodir}/%{name}.appdata.xml



%changelog
* Thu Oct 25 2018 Patrice Ferlet <metal3d_at_gmail.com>
- initial release
- appdata file created
