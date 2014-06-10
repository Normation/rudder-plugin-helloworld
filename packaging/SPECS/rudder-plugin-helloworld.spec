#####################################################################################
# Copyright 2011 Normation SAS
#####################################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, Version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#####################################################################################

#=================================================
# Specification file for rudder-plugin-helloworld
#
# Rudder plugin for hello world
#
# Copyright (C) 2011 Normation
#=================================================

#=================================================
# Variables
#=================================================
%define real_name        rudder-plugin-helloworld

%define rudderdir        /opt/rudder
%define ruddervardir     /var/rudder
%define rudderlogdir     /var/log/rudder

#=================================================
# Header
#=================================================
Summary: Configuration management and audit tool - hello world plugin
Name: %{real_name}
Version: %{real_version}
Release: 1%{?dist}
Epoch: 1299256513
License: GPLv3
URL: http://www.rudder-project.org

Group: Applications/System

Source1: settings-external.xml
Source2: settings-internal.xml

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: jdk
Requires: rudder-server-root

%description
Rudder is an open source configuration management and audit solution.

This package contains a plugin for the main webapp (see rudder-webapp package)
that demonstrates how plugins operate, and provides a starting point for every
person that would like to develop their own plugin.


#=================================================
# Source preparation
#=================================================
%prep

cp -rf %{_sourcedir}/rudder-sources %{_builddir}

#=================================================
# Building
#=================================================
%build

cd %{_builddir}/rudder-sources/rudder-parent-pom && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install
cd %{_builddir}/rudder-sources/rudder-commons && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install
cd %{_builddir}/rudder-sources/scala-ldap && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install
cd %{_builddir}/rudder-sources/ldap-inventory && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install
cd %{_builddir}/rudder-sources/cf-clerk && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install
cd %{_builddir}/rudder-sources/rudder && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install package
cd %{_builddir}/rudder-sources/helloworld-plugin && %{_sourcedir}/maven2/bin/mvn -s %{SOURCE1} -Dmaven.test.skip=true install package

# Installation
#=================================================
%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{rudderdir}/jetty7/rudder-plugins/

cp %{_builddir}/rudder-sources/helloworld-plugin/target/hello-world-*-plugin-with-own-dependencies.jar %{buildroot}%{rudderdir}/jetty7/rudder-plugins/hello-world.jar

%post -n rudder-plugin-helloworld
#=================================================
# Post Installation
#=================================================

# Register the plugin
if [ -x /opt/rudder/bin/rudder-plugin ]; then
  /opt/rudder/bin/rudder-plugin register hello-word
else
  echo "******************************************************************"
  echo "* Unable to register the plugin automatically. Please enable it  *"
  echo "* manually by editing your web application container context     *"
  echo "* file, adding /opt/rudder/jetty7/rudder-plugins/hello-world.jar *"
  echo "* to the <extraClasspath> anchor.                                *"
  echo "******************************************************************"
fi

%postun -n rudder-plugin-helloworld
#=================================================
# Post Uninstallation
#=================================================

# Unregister the plugin
if [ -x /opt/rudder/bin/rudder-plugin ]; then
  /opt/rudder/bin/rudder-plugin unregister hello-word
else
  echo "*********************************************************************"
  echo "* Unable to unregister the plugin automatically. Please disable it  *"
  echo "* manually by editing your web application container context        *"
  echo "* file, removing /opt/rudder/jetty7/rudder-plugins/hello-world.jar  *"
  echo "* from the <extraClasspath> anchor.                                 *"
  echo "*********************************************************************"
fi

%clean
#=================================================
# Cleaning
#=================================================

rm -rf %{buildroot}

#================================================d
# Files
#=================================================
%files -n rudder-plugin-helloworld
%defattr(-, root, root, 0755)
%{rudderdir}/jetty7/rudder-plugins/hello-world.jar

#=================================================
# Changelog
#=================================================
%changelog
* Fri Feb 17 2012 - Matthieu CERDA <matthieu.cerda@normation.com> 2.4-alpha5-1
- Initial package
