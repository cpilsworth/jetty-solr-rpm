%define _prefix /var/lib/solr
%define _logprefix /var/log
%define _javaprefix /usr/lib/jvm

Name:		jetty-solr
Version:	%{ver}
Release:	2%{?dist}
Summary:	Solr
License:	GPL
URL:		http://lucene.apache.org/solr/
Source: 	http://apache.mirrors.lucidnetworks.net/lucene/solr/%{version}/solr-%{version}.tgz
Source1:        jetty
Source2:        jetty-solr
Source3:        jetty-logging.xml
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre):	shadow-utils
Requires:	java => 1:1.6.0

%description
%{summary}
%prep
%setup -q -n solr-%{version}


%build

%install
rm -rf $RPM_BUILD_ROOT
%__install -d "%{buildroot}%{_prefix}"
cp -p *.txt "%{buildroot}%{_prefix}"
cp -pr contrib "%{buildroot}%{_prefix}"
cp -pr dist "%{buildroot}%{_prefix}"
cp -pr docs "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/jetty-solr"
cp -pr example/* "%{buildroot}%{_prefix}/jetty-solr"
cp -pr licenses "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/data
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/lib
%__install -d "%{buildroot}"/etc/default
%__install -d "%{buildroot}"/etc/init.d
%__install -D -m0644  "%{SOURCE1}" %{buildroot}/etc/default/jetty
%__install -D -m0755  "%{SOURCE2}" %{buildroot}/etc/init.d/jetty-solr
%__install -D -m0644  "%{SOURCE3}" %{buildroot}%{_prefix}/jetty-solr/etc/jetty-logging.xml
sed -i "s|JETTY_HOME_REPLACE|%{_prefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JETTY_LOG_REPLACE|%{_logprefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JAVA_HOME_REPLACE|%{_javaprefix}|g" "%{buildroot}/etc/default/jetty"

%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,solr,solr,-)
%attr(0755,solr,solr) %dir %{_prefix}
%doc
%{_prefix}/contrib
%{_prefix}/dist
%{_prefix}/docs
%{_prefix}/jetty-solr
%{_prefix}/licenses
%{_prefix}/CHANGES.txt
%{_prefix}/LICENSE.txt
%{_prefix}/NOTICE.txt
%{_prefix}/README.txt
%{_prefix}/SYSTEM_REQUIREMENTS.txt
%attr(0755,root,root) /etc/init.d/jetty-solr
%attr(0644,root,root) /etc/default/jetty

%pre
getent group solr >/dev/null || groupadd -r solr
getent passwd solr >/dev/null || \
    useradd -r -g solr -d %{_prefix} -s /sbin/nologin \
    -c "Solr User" solr
exit 0

%post
echo "Installation complete."

%changelog
* Tue Jan 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits for 4.1.0 solr using bundled jetty and zookeeper

* Tue Jan 18 2012 Jean-Francois Roche <jfroche@affinitic.be>
- Initial implementation
