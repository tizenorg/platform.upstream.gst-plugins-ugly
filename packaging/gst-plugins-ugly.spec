Name:       gst-plugins-ugly
Summary:    GStreamer plugins from the "ugly" set
Version:    1.6.0
Release:    1
Group:      Multimedia/Framework
License:    LGPL-2.0+
Source:     http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz

BuildRequires:  gettext-tools
BuildRequires:  which
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
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
%setup -q -n gst-plugins-ugly-%{version}

%build
export V=1
NOCONFIGURE=1 ./autogen.sh
%configure \
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
 --disable-realmedia\
 --disable-xingmux\
 --disable-x264

make %{?jobs:-j%jobs}

%install
%make_install

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/gstreamer-1.0/libgstasf.so
%{_libdir}/gstreamer-1.0/libgstamrnb.so
%{_libdir}/gstreamer-1.0/libgstamrwbdec.so
%exclude %{_datadir}/gstreamer-1.0/presets/GstAmrnbEnc.prs


