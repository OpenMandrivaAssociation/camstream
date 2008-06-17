Name:		camstream
Version:	0.27
Release:	%mkrel 1
Summary:	A tool for streaming and saving snapshots from a webcam
License:	GPL+
Group:		Video
URL:		http://www.smcc.demon.nl/camstream/

Source0:	%name-%version.tar.gz
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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=Webcam tool
Exec=%{_bindir}/camstream
Icon=video_section
Type=Application
Categories=Qt;AudioVideo;Recorder;
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,755)
%doc docs/*
%defattr(-,root,root)
%_bindir/*
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %_datadir/%name
%_datadir/%name/*

