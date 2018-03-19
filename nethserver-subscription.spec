Summary: NethServer Subscriptions
Name: nethserver-subscription
Version: 3.0.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Provides: nethserver-inventory = %{version}
Obsoletes: nethserver-inventory < %{version}
Provides: nethserver-alerts = %{version} 
Obsoletes: nethserver-alerts < %{version}

BuildRequires: nethserver-devtools
BuildRequires: gettext
BuildRequires: python2-devel

Requires: nethserver-base
Requires: nethserver-yum-cron
Requires: nethserver-collectd
Requires: nethserver-lib
Requires: python-requests
Requires: curl
Requires: puppet-agent

%description
NethServer Subscriptions

%prep
%setup -q

%build
%{makedocs}
perl createlinks
mkdir -p root%{python2_sitelib}
cp -a lib/nethserver_alerts.py root%{python2_sitelib}

%install
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > filelist

# 1. Split UI parts from core package
grep -E ^%{_nsuidir}/ filelist > filelist-ui
grep -vE ^%{_nsuidir}/ filelist > filelist-core

# 2. Move Alerts UI back to core:
grep -F Alerts filelist-ui >> filelist-core
sed -i '/Alerts/ d' filelist-ui

%files -f filelist-core
%defattr(-,root,root)
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-update

%package ui
Summary: NethServer Subscriptions UI
Requires: %{name} = %{version}-%{release}
%description ui
NethServer Subscriptions UI
%files ui -f filelist-ui
%defattr(-,root,root)
%doc COPYING
%doc README.rst

%changelog
* Mon Mar 19 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 3.0.0-1
- Implement clients for NethServer Subscriptions - NethServer/dev#5425

* Tue Mar 13 2018 Davide Principi <davide.principi@nethesis.it> - 3.0.0-0.1
- Development version (merge nethserver-alerts)