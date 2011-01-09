Summary:	Program Database Toolkit - source code analysis tools
Summary(pl.UTF-8):	Program Database Toolkit - narzędzia do analizy kodu źródłowego
Name:		pdtoolkit
Version:	3.16
Release:	0.1
License:	BSD-like (DUCTAPE), GPL v2+ (modified gfortran compiler), other (C++/F9x frontends)
Group:		Development/Tools
# "pdtoolkit" tarball contains more (not needed) precompiled binaries than "pdt"
Source0:	http://www.cs.uoregon.edu/research/paracomp/pdtoolkit/Download/pdt-%{version}.tar.gz
# Source0-md5:	3f528e18d569bcefe46ed3aa83c6c608
URL:		http://www.cs.uoregon.edu/research/paracomp/pdtoolkit/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pdtroot	%{_libdir}/pdtoolkit

%description
The Program Database Toolkit (PDT) is a tool infrastructure that
provides access to the high-level interface of source code for
analysis tools and applications. Currently, the toolkit consists of
the C/C++ and Fortran 77/90/95 IL (Intermediate Language) Analyzers,
and DUCTAPE (C++ program Database Utilities and Conversion Tools
APplication Environment) library and applications. The EDG C++ (or
Mutek Fortran 90) Front End first parses a source file, and produces
an intermediate language file. The appropriate IL Analyzer processes
this IL file, and creates a "program database" (PDB) file consisting
of the high-level interface of the original source.  Use of the 
DUCTAPE library then makes the contents of the PDB file accessible to
applications. This release also includes the Flint F95 parser from
Cleanscape Inc.

The main package contains DUCTAPE utilities.

%description -l pl.UTF-8
Program Database Toolkit (PDT) to zestaw narzędzi dających dostęp dla
narzędzi i aplikacji analizujących do interfejsu wysokiego poziomu
kodu źródłowego. Obecnie zestaw składa się z analizatorów IL
(Intermediate Language tj. języka pośredniego) dla C/C++ i Fortrana
77/90/95 oraz biblioteki i aplikacji DUCTAPE (C++ program Database
Utilities and Conversion Tools APplication Environment - środowiska
aplikacji narzędzi do bazy danych i konwersji programów w C++).
Najpierw frontend EDG C++ (lub Mutek Fortran 90) analizuje plik
źródłowy i tworzy plik w języku pośrednim. Odpowiedni analizator IL
przetwarza ten plik IL i tworzy plik "bazy danych programu" (PDB)
zawierający interfejs wysokiego poziomu oryginalnych źródeł. Przy
użyciu biblioteki DUCTAPE zawartość pliku PDB jest dostępna dla
aplikacji. Dostępny jest także analizator Flint F95 firmy Cleanscape
Inc.

Główny pakiet zawiera narzędzia DUCTAPE.

%package parser-c++
Summary:	EDG C++ frontend and analyzer for PDToolkit
Summary(pl.UTF-8):	Frontend i analizator EDG C++ dla PDToolkitu
License:	proprietary
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description parser-c++
EDG C++ frontend and analyzer for PDToolkit.

%description parser-c++ -l pl.UTF-8
Frontend i analizator EDG C++ dla PDToolkitu.

%package parser-fortran
Summary:	Fortran 90/95 frontends and analyzers for PDToolkit
Summary(pl.UTF-8):	Frontendy i analizatory Fortrana 90/95 dla PDToolkitu
License:	proprietary
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description parser-fortran
Mutek Fortran 90 and Cleanscape Flint F95 frontends and analyzers for
PDToolkit.

%description parser-fortran -l pl.UTF-8
Frontend i analizator Mutek Fortran 90 oraz Flint F95 dla PDToolkitu.

%package parser-gfortran
Summary:	GNU Fortran frontend for PDToolkit
Summary(pl.UTF-8):	Frontend GNU Fortran dla PDToolkitu
License:	BSD-like
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	pdtoolkit-gfortran >= 4.0

%description parser-gfortran
GNU Fortran frontend for PDToolkit.

%description parser-gfortran -l pl.UTF-8
Frontend GNU Fortran dla PDToolkitu.

%package devel
Summary:	Header files and static DUCTAPE library
Summary(pl.UTF-8):	Pliki nagłówkowe i statyczna biblioteka DUCTAPE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and static DUCTAPE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe i statyczna biblioteka DUCTAPE.

%prep
%setup -q

%build
install -d build/linux/bin
path_gxx="%{__cxx}" \
./configure \
	-gnu \
	-prefix=$(pwd)/build \
	-useropt="%{rpmcflags}"
%{__make} \
	PDT_GXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{pdtroot}/etc,%{_bindir},%{_libdir},%{_includedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} build/linux/bin/pdt_gfortran/*
cp -a build/linux/{bin,lib} $RPM_BUILD_ROOT%{pdtroot}
cp -a build/include $RPM_BUILD_ROOT%{pdtroot}
cp -a build/etc/flint.* $RPM_BUILD_ROOT%{pdtroot}/etc
ln -sf %{pdtroot}/lib/libpdb.a $RPM_BUILD_ROOT%{_libdir}/libpdb.a
ln -sf %{pdtroot}/include $RPM_BUILD_ROOT%{_includedir}/pdtoolkit

for f in cparse cxxparse f90parse f95parse gfparse ; do
	sed -i -e "s,^BINDIR=.*,BINDIR=%{pdtroot}/bin,;
		   s,^PDTDIR=.*,PDTDIR=%{pdtroot}," $RPM_BUILD_ROOT%{pdtroot}/bin/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS LICENSE README
%dir %{pdtroot}
%dir %{pdtroot}/bin
%attr(755,root,root) %{pdtroot}/bin/pdbcomment
%attr(755,root,root) %{pdtroot}/bin/pdbconv
%attr(755,root,root) %{pdtroot}/bin/pdbhtml
%attr(755,root,root) %{pdtroot}/bin/pdbmerge
%attr(755,root,root) %{pdtroot}/bin/pdbstmt
%attr(755,root,root) %{pdtroot}/bin/pdbtree
%attr(755,root,root) %{pdtroot}/bin/tau_instrumentor
%attr(755,root,root) %{pdtroot}/bin/xmlgen
%dir %{pdtroot}/etc
%dir %{pdtroot}/include
%{pdtroot}/include/kai

%files parser-c++
%defattr(644,root,root,755)
%attr(755,root,root) %{pdtroot}/bin/cparse
%attr(755,root,root) %{pdtroot}/bin/cxxparse
%attr(755,root,root) %{pdtroot}/bin/edgcpfe
%attr(755,root,root) %{pdtroot}/bin/taucpdisp

%files parser-fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{pdtroot}/bin/f90fe
%attr(755,root,root) %{pdtroot}/bin/f90parse
%attr(755,root,root) %{pdtroot}/bin/f95parse
%attr(755,root,root) %{pdtroot}/bin/pdtf90disp
%attr(755,root,root) %{pdtroot}/bin/pdtflint
%{pdtroot}/etc/flint.cfg
%{pdtroot}/etc/flint.err
%{pdtroot}/etc/flint.hls

%files parser-gfortran
%defattr(644,root,root,755)
%attr(755,root,root) %{pdtroot}/bin/gfparse
%dir %{pdtroot}/bin/pdt_gfortran

%files devel
%defattr(644,root,root,755)
%{_libdir}/libpdb.a
%{_includedir}/pdtoolkit
%{pdtroot}/include/pdb*.h
%{pdtroot}/include/pdb*.inl
%{pdtroot}/lib
