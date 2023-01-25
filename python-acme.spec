#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		cryptography_ver	1.2.3
%define		josepy_ver		1.1.0
%define		pyopenssl_ver		0.15.1
%define		requests_ver		2.6.0
%define		requests_toolbelt_ver	0.3.0
%define		six_ver			1.9.0

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
BuildRequires:	python-cryptography >= %{cryptography_ver}
BuildRequires:	python-josepy >= %{josepy_ver}
BuildRequires:	python-pyOpenSSL >= %{pyopenssl_ver}
BuildRequires:	python-pyrfc3339
BuildRequires:	python-pytz
BuildRequires:	python-requests >= %{requests_ver}
BuildRequires:	python-requests-toolbelt >= %{requests_toolbelt_ver}
BuildRequires:	python-six >= %{six_ver}
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
Requires:	python-cryptography >= %{cryptography_ver}
Requires:	python-pyOpenSSL >= %{pyopenssl_ver}
Requires:	python-pyasn1
Requires:	python-pyrfc3339
Requires:	python-pytz
Requires:	python-requests >= %{requests_ver}
Requires:	python-requests-toolbelt >= %{requests_toolbelt_ver}
Requires:	python-six >= %{six_ver}
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
