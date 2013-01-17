Name:           gap-io
Version:        4.2
Release:        2%{?dist}
Summary:        Unix I/O functionality for GAP

Group:          Sciences/Mathematics
License:        GPLv3+
URL:            http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/io.html
Source0:        http://www-groups.mcs.st-and.ac.uk/~neunhoef/Computer/Software/Gap/io/io-%{version}.tar.gz

BuildRequires:  gap-devel
BuildRequires:  pkgconfig

Requires:       gap-core

Provides:       gap-pkg-io = %{version}-%{release}

%description
This GAP package provides a link to the standard UNIX I/O functionality
that is available through the C library.  This part basically consists
of functions on the GAP level that allow functions in the C library to
be called.

Built on top of this is a layer for buffered input/output which is
implemented completely in the GAP language.  It is intended to be used
by programs for which it is not necessary to have full direct access to
the operating system.

On this level, quite a few convenience functions are implemented for
interprocess communication like starting up pipelines of processes to
filter data through them and to start up processes and then communicate
with them.  There is also support for creating network connections over
TCP/IP and UDP.

Building on this, the package contains an implementation of the client
side of the HTTP protocol making it possible among other things to
access web pages from within GAP.

Another part of the package is a framework for object serialization.
That is, GAP objects can be converted into a platform-independent byte
sequence which can be stored to a file or sent over the network.  The
code takes complete care of arbitrarily self-referential data structures
like lists containing themselves as an entry.  The resulting byte
strings can be read back into GAP and the original objects are rebuilt
with exactly the same self-references.  This works for most of the
standard builtin types of GAP like numbers, permutations, polynomials,
lists, and records and can be extended to nearly arbitrary GAP objects.

%prep
%setup -q -n io

# File file encodings
for fil in PackageInfo.g PackageInfoFor4.5.g; do
  iconv -f iso8859-1 -t utf-8 -o $fil.utf8 $fil
  touch -r $fil $fil.utf8
  mv -f $fil.utf8 $fil
done

%build
%configure --with-gaproot=%{_gap_dir}
make %{?_smp_mflags} io.la

# Remove an unnecessary script and some leftover build artifacts
rm -f doc/clean doc/io.{aux,bbl,blg,idx,ilg,ind,log,pnr,toc}

%install
# make install is broken

# Get the name of the arch-specific subdirectory
source %{_gap_dir}/sysinfo.gap

# Install, but not the libtool archive
mkdir -p %{buildroot}%{_gap_dir}/pkg/io/bin/$GAParch
./libtool --mode=install %{_bindir}/install -c io.la \
  %{buildroot}%{_gap_dir}/pkg/io/bin/$GAParch
rm -f %{buildroot}%{_gap_dir}/pkg/io/bin/$GAParch/io.la
cp -a *.g doc example gap tst %{buildroot}%{_gap_dir}/pkg/io

%post
    %{_bindir}/update-gap-workspace

%postun
    %{_bindir}/update-gap-workspace

%check
# Cannot run the HTTP test, as there is no network access on koji builders
gap -l "/usr/lib/gap;%{buildroot}%{_gap_dir}" tst/platform.g tst/pickle.g \
  tst/buffered.g < /dev/null

%files
%doc CHANGES GPL HISTORY LICENSE README TODO
%{_gap_dir}/pkg/io/

%changelog
* Wed Oct 10 2012 Jerry James <loganjerry@gmail.com> - 4.2-2
- Add a check script

* Mon Sep 17 2012 Jerry James <loganjerry@gmail.com> - 4.2-1
- Initial RPM
