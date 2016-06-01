# coding: UTF-8
# grust-gen - Rust binding generator for GObject introspection
#
# Copyright (C) 2016  Jonas Ådahl <jadahl@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA

import os
from ..mapping import sys_crate_name
from ..output import FileOutput

class SysCargoWriter(object):
    """Generator for -sys Cargo build files."""

    def __init__(self, mapper, transformer, tmpl_lookup, path):
        self._mapper = mapper
        self._transformer = transformer
        self._cargo_template = tmpl_lookup.get_template('cargo/cargo.tmpl')
        self._build_rs_template = tmpl_lookup.get_template('cargo/build.rs.tmpl')
        self._cargo_file = os.path.join(path, 'Cargo.toml')
        self._build_rs_file = os.path.join(path, 'build.rs')

    def _write_cargo(self, output):
        pkgname = sys_crate_name(self._transformer.namespace)
        version = self._transformer.namespace.version
        result = self._cargo_template.render_unicode(mapper=self._mapper,
                                                     pkgname=pkgname,
                                                     version=version)
        output.write(result)

    def _write_build_rs(self, output):
        pkgconfig_packages = self._transformer.namespace.exported_packages
        result = self._build_rs_template.render_unicode(packages=pkgconfig_packages)
        output.write(result)

    def write(self):
        cargo_output = FileOutput(self._cargo_file, encoding='utf-8')
        with cargo_output as output:
            try:
                self._write_cargo(output)
            except Exception:
                raise SystemExit(1)

        build_rs_output = FileOutput(self._build_rs_file, encoding='utf-8')
        with build_rs_output as output:
            try:
                self._write_build_rs(output)
            except Exception:
                raise SystemExit(1)
