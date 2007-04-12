Name:		camstream
Version:	0.26.3
Release:	%mkrel 6
Summary:	A tool for streaming and saving snapshots from a webcam
License:	GPL
Group:		Video
Url:		http://www.smcc.demon.nl/camstream/

Source:		%name-%version.tar.bz2
Patch0:		camstream_lib64.patch
Patch1:		camstream-0.26.3-x86_64-asm.patch

BuildRoot:	%_tmppath/%name-%version-%release-root
ExcludeArch:	ppc

Buildrequires:  jpeg-devel png-devel zlib1-devel libqt-devel

%description
CamStream is a tool for Webcams and TV grabber cards that allows for streaming 
video from multiple video sources. It can save and/or upload (FTP) timed 
snapshots. It provides a GUI frontend to control the Webcam(s).

%prep

%setup -q

%patch0 -p1

%ifarch x86_64
%patch1 -p1
%endif

%build
export QTDIR=%_prefix/lib/qt3
export KDEDIR=%_prefix
export LD_LIBRARY_PATH=$QTDIR/lib:$KDEDIR/lib:$LD_LIBRARY_PATH
export PATH=$QTDIR/bin:$KDEDIR/bin:$PATH
export UIC=$QTDIR/bin/uic
export MOC=$QTDIR/bin/moc

export CFLAGS="%optflags" CXXFLAGS="%optflags"
./configure --prefix=%_prefix \
	--enable-mt \
	--with-qt-dir=%_prefix/lib/qt3/%_lib/ \
	--disable-rpath \
	--disable-debug

%make

%install
%makeinstall

(cd $RPM_BUILD_ROOT
mkdir -p ./usr/lib/menu
cat > ./usr/lib/menu/%{name} <<EOF
?package(camstream):\
command="/usr/bin/camstream" \
icon="video_section.png" \
needs="X11" \
section="Multimedia/Video" \
title="Camstream" \
longtitle="Webcam tool"\
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=Webcam tool
Exec=%{_bindir}/camstream
Icon=video_section.png
Type=Application
Categories=Qt;X-MandrivaLinux-Multimedia-Video;AudioVideo;Recorder;
EOF
)

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,755)
%doc docs/*
%defattr(-,root,root)
%_bindir/*
%_menudir/*
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %_datadir/%name
%_datadir/%name/*

