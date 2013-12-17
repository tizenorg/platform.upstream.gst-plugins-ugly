Name:       gst-plugins-ugly
Summary:    GStreamer plugins from the "ugly" set
Version:    1.2.0
Release:    0
Group:      Multimedia/Audio
License:    LGPL-2.0+
Source0:    %{name}-%{version}.tar.gz
Source100:      common.tar.bz2
Source1001: 	gst-plugins-ugly.manifest
BuildRequires:  gettext-tools
BuildRequires:  which
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) 
BuildRequires:  pkgconfig(gstreamer-1.0) 
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(opencore-amrwb)
BuildRequires:  libmad-devel

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
%setup -q -T -D -a 100
cp %{SOURCE1001} .

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
 --disable-mpeg2dec\
 --disable-sidplay\
 --disable-twolame\
 --disable-x264

make %{?jobs:-j%jobs}

%install
%make_install

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
# check why this one is not being built - Anas
#%{_libdir}/gstreamer-1.0/libgstmpegaudioparse.so
%{_libdir}/gstreamer-1.0/libgstasf.so
%{_libdir}/gstreamer-1.0/libgstxingmux.so
%{_libdir}/gstreamer-1.0/libgstamrnb.so
%{_libdir}/gstreamer-1.0/libgstamrwbdec.so
%{_libdir}/gstreamer-1.0/libgstrmdemux.so
%{_libdir}/gstreamer-1.0/libgstmad.so
%exclude %{_datadir}/gstreamer-1.0/presets/GstAmrnbEnc.prs

