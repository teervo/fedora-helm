Name:           helm-synth
Version:        0.9.0
Release:        3%{?dist}
Summary:        Helm is a free polyphonic synth with lots of modulation

License:        GPL-3.0
URL:            http://tytel.org/helm
Source0:        https://github.com/mtytel/helm/archive/v%{version}.tar.gz
Source1:        %{name}.appdata.xml
Patch0:         00-gcc-9.1.compatibility-fixes.patch

BuildRequires:  lv2-devel libX11-devel alsa-lib-devel libXext-devel libXinerama-devel freetype-devel libcurl-devel mesa-libGL-devel jack-audio-connection-kit-devel libXcursor-devel gcc-c++ libappstream-glib
Requires:       freetype libXext mesa-libGL

%define debug_package %{nil}
%define _build_id_links none

%package -n lv2-%{name}
Summary:        Helm LV2 plugin is a free polyphonic synth with lots of modulation
Requires:       lv2 freetype libXext mesa-libGL

%package -n vst-%{name}
Summary:        Helm VST plugin is a free polyphonic synth with lots of modulation
Requires:       freetype libXext mesa-libGL

%description
Helm is a free, cross-platform, polyphonic synthesizer that runs on GNU/Linux,
Mac, and Windows as a standalone program and as a LV2/VST/AU/AAX plugin.
You can install helm (standalone), or lv2-helm that is LV2 plugin.

%description -n lv2-%{name}
Helm is a free, cross-platform, polyphonic synthesizer that runs on GNU/Linux,
Mac, and Windows as a standalone program and as a LV2/VST/AU/AAX plugin.
This package installs the LV2 plugin.

%description -n vst-%{name}
Helm is a free, cross-platform, polyphonic synthesizer that runs on GNU/Linux,
Mac, and Windows as a standalone program and as a LV2/VST/AU/AAX plugin.
This package installs the VST plugin.

%prep
%autosetup -p1 -n helm-%{version}
# renaming helm to helm-synth:
sed 's:$(DESKTOP)/helm.desktop:$(DESKTOP)/$(PROGRAM).desktop:' -i Makefile
sed s:Exec=helm:Exec=%{name}: -i standalone/helm.desktop
sed s:/usr/share/helm:/usr/share/helm-synth: -i src/common/load_save.cpp
sed s:/usr/share/helm:/usr/share/helm-synth: -i src/editor_sections/patch_browser.cpp

%build
%make_build JUCE_TARGET_APP=%{name}

%install
rm -rf $RPM_BUILD_ROOT
%make_install PROGRAM=%{name} LIBDIR=%{_libdir} VSTDIR=%{buildroot}%{_libdir}/vst
mv %{buildroot}%{_mandir}/man1/helm.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

# install appdata file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

%files
%{_bindir}/%{name}
%{_datadir}/doc
%{_datadir}/%{name}
%{_datadir}/applications
%{_datadir}/icons
%{_metainfodir}/%{name}.appdata.xml
%doc %{_mandir}

%files -n lv2-%{name}
%{_libdir}/lv2

%files -n vst-%{name}
%{_libdir}/vst

%changelog
* Thu Oct 25 2018 Patrice Ferlet <metal3d_at_gmail.com>
- initial release
- appdata file created
* Mon May 24 2021 teervo <teervo_at_protonmail.com>
- rename package and installed files to helm-synth to avoid conflicts with https://helm.sh/
- include patch from https://github.com/mtytel/helm/pull/233
- generate package for VST plugin
* Wed May 26 2021 teervo <teervo_at_protonmail.com>
- fix issue with patch directory location
