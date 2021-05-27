%global         debug_package %{nil}
%global         _build_id_links none

Name:           helm-synth
Version:        0.9.0
Release:        7%{?dist}
Summary:        Helm is a free polyphonic synth with lots of modulation

License:        GPLv3
URL:            http://tytel.org/helm
Source0:        https://github.com/mtytel/helm/archive/v%{version}.tar.gz
Source1:        %{name}.appdata.xml
Patch0:         00-gcc-9.1.compatibility-fixes.patch

BuildRequires:  lv2-devel libX11-devel alsa-lib-devel libXext-devel
BuildRequires:  libXinerama-devel freetype-devel libcurl-devel
BuildRequires:  mesa-libGL-devel jack-audio-connection-kit-devel
BuildRequires:  libXcursor-devel gcc-c++ libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       %{name}-common freetype mesa-libGL

%package -n %{name}-common
Summary:        Presets and documentation for the Helm polyphonic synth

%package -n lv2-%{name}
Summary:        Helm LV2 plugin is a free polyphonic synth with lots of modulation
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-common lv2 freetype mesa-libGL

%package -n vst-%{name}
Summary:        Helm VST plugin is a free polyphonic synth with lots of modulation
Requires:       %{name}-common freetype mesa-libGL


%description
Helm is a free, cross-platform, polyphonic synthesizer that runs on
GNU/Linux, Mac, and Windows as a standalone program and as a
LV2/VST/AU/AAX plugin. You can install %{name} (standalone), lv2-%{name}
(LV2 plugin) or vst-%{name} (VST plugin).

%description -n %{name}-common
Helm is a free, cross-platform, polyphonic synthesizer that runs on
GNU/Linux, Mac, and Windows as a standalone program and as a
LV2/VST/AU/AAX plugin. This package contains presets and documentation.

%description -n lv2-%{name}
Helm is a free, cross-platform, polyphonic synthesizer that runs on
GNU/Linux, Mac, and Windows as a standalone program and as a
LV2/VST/AU/AAX plugin. This package installs the LV2 plugin.

%description -n vst-%{name}
Helm is a free, cross-platform, polyphonic synthesizer that runs on
GNU/Linux, Mac, and Windows as a standalone program and as a
LV2/VST/AU/AAX plugin. This package installs the VST plugin.

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
rm -rf ${buildroot}
%make_install PROGRAM=%{name} LIBDIR=%{_libdir} VSTDIR=%{buildroot}%{_libdir}/vst
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# Documentation
install -m 0644 docs/helm_manual.pdf %{buildroot}%{_datadir}/doc/%{name}
mv %{buildroot}%{_mandir}/man1/helm.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

# install appdata file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

%files
%{_bindir}/%{name}
%{_datadir}/applications
%{_datadir}/icons/hicolor/16x16/apps/helm-synth.png
%{_datadir}/icons/hicolor/22x22/apps/helm-synth.png
%{_datadir}/icons/hicolor/24x24/apps/helm-synth.png
%{_datadir}/icons/hicolor/32x32/apps/helm-synth.png
%{_datadir}/icons/hicolor/48x48/apps/helm-synth.png
%{_datadir}/icons/hicolor/64x64/apps/helm-synth.png
%{_datadir}/icons/hicolor/128x128/apps/helm-synth.png
%{_datadir}/icons/hicolor/256x256/apps/helm-synth.png
%{_metainfodir}/%{name}.appdata.xml
%doc %{_mandir}/man1/helm-synth.1.gz

%files -n %{name}-common
%doc %{_datadir}/doc/%{name}
%{_datadir}/%{name}

%files -n lv2-%{name}
%{_libdir}/lv2

%files -n vst-%{name}
%{_libdir}/vst

%changelog
* Wed May 26 2021 teervo <teervo_at_protonmail.com>
- fix issue with patch directory location
- split patches and documentation into their own package
- install PDF manual
- fix some rpmlint warnings and errors
* Mon May 24 2021 teervo <teervo_at_protonmail.com>
- rename package and installed files to helm-synth to avoid conflicts with https://helm.sh/
- include patch from https://github.com/mtytel/helm/pull/233
- generate package for VST plugin
* Thu Oct 25 2018 Patrice Ferlet <metal3d_at_gmail.com>
- initial release
- appdata file created
