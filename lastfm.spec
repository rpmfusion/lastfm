%define upname last.fm

Name: lastfm
Version: 1.4.0.56102
Release: 3%{?dist}
Summary: Last.fm music client

Group: Applications/Multimedia
License: GPLv2+
URL: http://www.last.fm/tools/downloads/
Source0: http://cdn.last.fm/client/src/%{upname}-%{version}.src.tar.bz2
Source1: lastfm.desktop
Patch0: lastfm-prefix.patch
Patch1: lastfm-gpod-pkgconfig.patch
Patch2: lastfm-gcc43.patch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: qt4-devel alsa-lib-devel zlib-devel
BuildRequires: libsamplerate-devel fftw-devel libmad-devel libgpod-devel
BuildRequires: desktop-file-utils

%description
With Last.fm on your computer you can scrobble your tracks, share your 
music taste, listen to personalised radio streams, and discover new 
music and people.

%prep
%setup -q -n %{upname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure 
%{__make} %{_smp_mflags} libdir=%{_libdir} datadir=%{_datadir}
(cd i18n; lrelease-qt4 *.ts; mkdir ../bin/data/i18n;\
	cp *.qm ../bin/data/i18n; cd ..)

%install
%{__rm} -fr %{buildroot}
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{_libdir}/%{name}
%{__mkdir_p} %{buildroot}/%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps
%{__install} -p -m 755 bin/last.fm %{buildroot}/%{_bindir}/lastfm
%{__cp} -a bin/libLastFmTools.so.* %{buildroot}/%{_libdir}
%{__cp} -a bin/libLastFmFingerprint.so.* %{buildroot}/%{_libdir}
%{__cp} -a bin/libMoose.so.* %{buildroot}/%{_libdir}
%{__cp} -a bin/data %{buildroot}/%{_datadir}/%{name}
%{__cp} -a bin/services %{buildroot}/%{_libdir}/%{name}
%{__cp} -a bin/data/icons/as.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/lastfm.png

desktop-file-install --vendor="rpmfusion" \
  --dir=%{buildroot}/%{_datadir}/applications %{SOURCE1}

%clean
%{__rm} -fr %{buildroot}

%post 
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun 
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%doc COPYING ChangeLog
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/32x32/apps/lastfm.png

%changelog
* Wed Jul 23 2008 Sergio Pascual <sergio.pasra at gmail.com> 1.4.0.56102-3
- Importing into rpmfusion
- Vendor changed to rpmfusion
- libgpod-devel bug #446442 fixed in rawhide 
- Updated desktop file

* Wed May 14 2008 Sergio Pascual <sergio.pasra at gmail.com> 1.4.0.56102-2
- Patch for gcc 4.3 from Michel Salim
- Patch for gpod, using pkgconfig from Michel Salim 

* Wed Dec 12 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.4.0.56102-1
- New upstrean source

* Tue Nov 13 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.3.2.13-2
- Specfile cleanup

* Mon Sep 24 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.3.2.13-1
- New upstrean source

* Sun Aug 26 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.3.1.0-3
- Using native zlib
- Using mp3transcoding from lame (not working, reverted)
- Corrected group tag
- Using disttag

* Fri Aug 24 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.3.1.0-2
- Patch to use libdir

* Mon Aug 20 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.3.1.0-1
- New upstream source

* Thu Apr 12 2007 Sergio Pascual <sergio.pasra at gmail.com> 1.1.3-0.1
- Initial spec file
