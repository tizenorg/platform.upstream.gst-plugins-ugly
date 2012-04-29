Name:       gst-plugins-ugly
Summary:    GStreamer plugins from the "ugly" set
Version:    0.10.18
Release:    2
Group:      TO_BE/FILLED_IN
License:    LGPLv2+
Source0:    %{name}-%{version}.tar.gz
Patch0 :    gst-plugins-ugly-disable-gtk-doc.patch
BuildRequires:  gettext-tools
BuildRequires:  which
BuildRequires:  gst-plugins-base-devel
BuildRequires:  pkgconfig(gstreamer-0.10) 
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(liboil-0.3)
BuildRequires:  pkgconfig(drm-service)
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
%ifarch %{arm}
CFLAGS=" %{optflags} \
       -DGST_EXT_TIME_ANALYSIS         \
       -DGST_EXT_TA_UNIT_MEXT          \
       -DGST_EXT_PAD_LINK_UNCHECKED        \
       -DGST_EXT_REDUCE_PLUGIN_NUM         \
       -DGST_EXT_USE_PDP_NETWORK       \
       -DGST_EXT_VOLUME_WITHOUT_LIBOIL     \
       -DGST_EXT_AUDIOSINK_MUTE        \
       -DEXT_AUDIO_FILTER_EFFECT       \
       -DGST_EXT_NONBLOCKDQUE          \
       -DGST_EXT_RENEGOTIATION         \
       -DGST_EXT_MOBILECAMERA          \
       -DGST_EXT_ASYNC_DEV         \
       -DGST_EXT_AV_RECORDING          \
       -DGST_EXT_SWITCH_CAMERA         \
       -DGST_EXT_OVERLAYSINK_SQVGA         \
       -DGST_EXT_FFMUX_ADD_PROPERTY        \
       -DGST_EXT_I_LIKE_DSP            \
       -DGST_EXT_FFMUX_ENHANCEMENT         \
       -DGST_EXT_CAMCORDER_IPP \
       -DGST_EXT_PROCESS_DRMCHUNK  \
	" ; export CFLAGS
%else
CFLAGS=" %{optflags} \
       -DGST_EXT_TIME_ANALYSIS         \
       -DGST_EXT_PAD_LINK_UNCHECKED        \
       -DGST_EXT_DFBVIDEOSINK_IPP      \
       -DGST_EXT_REDUCE_PLUGIN_NUM     \
       -DGST_EXT_VOLUME_WITHOUT_LIBOIL     \
       -DGST_EXT_TA_UNIT_MEXT          \
       -DGST_EXT_AUDIOSINK_MUTE        \
       -DGST_EXT_GST_SYNC_MODE         \
       -DGST_EXT_NONBLOCKDQUE          \
       -DGST_EXT_RENEGOTIATION         \
       -DGST_EXT_MOBILECAMERA          \
       -DGST_EXT_ASYNC_DEV             \
       -DGST_EXT_AV_RECORDING          \
       -DGST_EXT_SWITCH_CAMERA         \
       -DGST_EXT_FFMUX_ADD_PROPERTY        \
       -DGST_EXT_FFMUX_ENHANCEMENT \
	" ; export CFLAGS
%endif

./autogen.sh 
%configure  --disable-static \
	--prefix=%{_prefix} \
	--disable-nls \
	--with-html-dir=/tmp/dump \
	--disable-examples \
	--disable-dvdlpcmdec   \
	--disable-dvdsub       \
	--disable-iec958       \
	--disable-mpegstream   \
	--disable-realmedia    \
	--disable-synaesthesia \
	--disable-a52dec       \
	--disable-cdio \
	--disable-dvdread      \
	--disable-dvdnav       \
	--disable-mad  \
	--disable-mpeg2dec     \
	--disable-sidplay      \
	--disable-twolame      \
	--disable-x264



make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install




%files
%defattr(-,root,root,-)
%{_libdir}/gstreamer-0.10/libgstmpegaudioparse.so
%{_libdir}/gstreamer-0.10/libgstasf.so
%{_libdir}/gstreamer-0.10/libgstamrnb.so
%{_libdir}/gstreamer-0.10/libgstamrwbdec.so
%exclude %{_datadir}/gstreamer-0.10/presets/GstAmrnbEnc.prs

