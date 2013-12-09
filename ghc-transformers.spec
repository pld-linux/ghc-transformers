#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	transformers
Summary:	Concrete functor and monad transformers
Summary(pl.UTF-8):	Funktory konkretne i przekształcenia monad
Name:		ghc-%{pkgname}
Version:	0.3.0.0
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/transformers
Source0:	http://hackage.haskell.org/package/transformers-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	852dc0b79cc2bcb39136287d3dd385e5
URL:		http://hackage.haskell.org/package/transformers/
BuildRequires:	ghc >= 6.12.3
%{?with_prof:BuildRequires:	ghc-prof >= 6.12.3}
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
This package contains the monad transformer class, the concrete monad
transformers, operations and liftings. It can be used on its own in
Haskell 98 code, or with the monad classes in the monads-fd or
monads-tf packages, which automatically lift operations introduced by
monad transformers through other transformers.

%description -l pl.UTF-8
Ten pakiet zawiera klasę przekształceń monad, konkretne
przekształcenia monad, operacje oraz podniesienia. Może być używana
samodzielnie w kodzie Haskella 98 albo z klasami monad z pakietów
monads-fd lub monads-tf, które automatycznie podnoszą operacje
wprowadzone przez przekształcenia monad poprzez inne przekształcenia.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HStransformers-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/IO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/IO/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/RWS
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/RWS/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/State
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/State/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Writer
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Writer/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStransformers-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/IO/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/RWS/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/State/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Writer/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Functor/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
