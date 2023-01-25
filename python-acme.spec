#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module  acme
Summary:	Python library for the ACME protocol
Summary(pl.UTF-8):	Biblioteka Pythona do protokołu ACME
Name:		python-%{module}
# keep 1.11.x here for python2 support; see python3-acme.spec for python3 versions
Version:	1.11.0
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/acme/
Source0:	https://files.pythonhosted.org/packages/source/a/acme/%{module}-%{version}.tar.gz
# Source0-md5:	2ea41be3043f0353587274ffbf01032f
URL:		https://pypi.org/project/acme/
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 1:36.2
%if %{with doc} || %{with tests}
BuildRequires:	python-cryptography >= 1.2.3
BuildRequires:	python-josepy >= 1.1
BuildRequires:	python-pyOpenSSL >= 0.15.1
BuildRequires:	python-pyrfc3339
BuildRequires:	python-pytz
BuildRequires:	python-requests >= 2.6
BuildRequires:	python-requests-toolbelt >= 0.3
BuildRequires:	python-six >= 1.9
%endif
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest
%endif
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2 >= 1.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Suggests:	python-acme-doc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python library for use of the Automatic Certificate Management
Environment protocol as defined by the IETF. It's used by the Let's
Encrypt project.

%description -l pl.UTF-8
Biblioteka Pythona do korzystania z protokołu Automatic Certificate
Management Environment (środowiska automatycznego zarządzania
certyfikatami) zdefiniowanego przez IETF. Jest używana przez projekt
Let's Encrypt.

%package doc
Summary:	Documentation for python-acme library
Summary(pl.UTF-8):	Dokumentacja do biblioteki python-acme
Group:		Documentation

%description doc
Documentation for the ACME Python library.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Pythona ACME.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,man,*.html,*.js}
%endif
