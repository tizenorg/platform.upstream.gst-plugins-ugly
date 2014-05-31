Name:       gst-plugins-ugly
Summary:    GStreamer plugins from the "ugly" set
Version:    0.10.19
Release:    39 
%if 0%{?tizen_profile_wearable}
%else
VCS:        framework/multimedia/gst-plugins-ugly0.10#gst-plugins-ugly0.10_0.10.19-1slp2+27-38-g2a83bca814e481abeeba0bcb243142eaffab2604
%endif
Group:      Applications/Multimedia
License:    LGPLv2+
Source0:    %{name}-%{version}.tar.gz
%if 0%{?tizen_profile_mobile}
Patch0 :    gst-plugins-ugly-disable-gtk-doc-mobile.patch
%else
Patch0 :    gst-plugins-ugly-disable-gtk-doc-wearable.patch
%endif
BuildRequires:  gettext-tools
BuildRequires:  which
BuildRequires:  gst-plugins-base-devel
BuildRequires:  pkgconfig(gstreamer-0.10)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(opencore-amrwb)

%description
 GStreamer is a streaming media framework, based on graphs of filters
 which operate on media data.  Applications using this library can do
 anything from real-time sound processing to playing videos, and just
 about anything else media-related.  Its plugin-based architecture means
 that new data types or processing capabilities can be added simply by
 installing new plug-ins.
 .
 This packages contains plugins from the "ugly" set, a set of
 good-quality plug-ins that might pose distribution problems.



%prep
%setup -q
%patch0 -p1


%build
%if 0%{?tizen_profile_mobile}
cd mobile
%else
cd wearable
%endif

./autogen.sh
%configure --prefix=%{_prefix}\
 --disable-static\
 --disable-nls\
 --with-html-dir=/tmp/dump\
 --disable-examples\
 --disable-dvdlpcmdec\
 --disable-dvdsub\
 --disable-iec958\
 --disable-mpegstream\
 --disable-synaesthesia\
 --disable-a52dec\
 --disable-cdio\
 --disable-dvdread\
 --disable-dvdnav\
 --disable-mad\
 --disable-mpeg2dec\
 --disable-sidplay\
 --disable-twolame\
 --disable-x264



make %{?jobs:-j%jobs}

%install
%if 0%{?tizen_profile_mobile}
cd mobile
%else
cd wearable
%endif

rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}
%make_install




%files
%if 0%{?tizen_profile_mobile}
%manifest mobile/gst-plugins-ugly.manifest
%else
%manifest wearable/gst-plugins-ugly.manifest
%endif
%defattr(-,root,root,-)
%{_libdir}/gstreamer-0.10/libgstmpegaudioparse.so
%{_libdir}/gstreamer-0.10/libgstasf.so
%{_libdir}/gstreamer-0.10/libgstrmdemux.so
%{_libdir}/gstreamer-0.10/libgstamrnb.so
%{_libdir}/gstreamer-0.10/libgstamrwbdec.so
%exclude %{_datadir}/gstreamer-0.10/presets/GstAmrnbEnc.prs
%{_datadir}/license/%{name}
