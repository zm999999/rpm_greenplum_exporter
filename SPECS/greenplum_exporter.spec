Name: greenplum_exporter
Version: 1.2
Release: rhel7
License: GPL
Summary: Greenplum database exporter installation package for prometheus.
Group:Development/Tools
%define exporter_user prometheus
%define exporter_dir usr/local/greenplum_exporter/

# 依赖
Requires: /bin/sh

# 描述
%description
This is Greenplum database exporter installation package for prometheus based on go language and write by tang(inrgihc@126.com)
 
# 安装前执行
%pre
rm -rf $RPM_BUILD_ROOT/%{exporter_dir}

grep %{exporter_user} /etc/group > /dev/null
if [ $? != 0 ]; then
   groupadd %{exporter_user}
fi

grep %{exporter_user} /etc/passwd > /dev/null
if [ $? != 0 ]; then 
   useradd -g %{exporter_user} %{exporter_user} -M -s /sbin/nologin
fi

# 安装后执行
%post
chown -R %{exporter_user}.%{exporter_user} %{exporter_dir}

# 卸载前执行
%preun
systemctl stop greenplum_exporter

# 卸载后执行
%postun
userdel %{exporter_user} > /dev/null
rm -f /etc/systemd/system/greenplum_exporter.service
rm -rf %{exporter_dir}

%build 
 
# 安装阶段
%install
mkdir -p $RPM_BUILD_ROOT/%{exporter_dir}/bin/
mkdir -p $RPM_BUILD_ROOT/%{exporter_dir}/etc/
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/
cd $RPM_BUILD_DIR
pwd
cp ../BUILD/greenplum_exporter $RPM_BUILD_ROOT/%{exporter_dir}/bin/
cp ../BUILD/greenplum.conf $RPM_BUILD_ROOT/%{exporter_dir}/etc/
cp ../BUILD/greenplum_exporter.service $RPM_BUILD_ROOT/etc/systemd/system/

# 包含文件
%files
/%{exporter_dir}/bin/greenplum_exporter
/%{exporter_dir}/etc/greenplum.conf
/etc/systemd/system/greenplum_exporter.service

# 变更日志
%changelog 
* Fri Jul 24 2020 tang <inrgihc@126.com> - 1.0-1
- Initial version

# 构建完成后清理
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
