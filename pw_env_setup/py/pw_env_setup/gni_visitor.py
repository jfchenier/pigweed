# Copyright 2022 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Serializes an Environment into a JSON file."""

from __future__ import print_function

import re

# Disable super() warnings since this file must be Python 2 compatible.
# pylint: disable=super-with-arguments


class GNIVisitor(object):  # pylint: disable=useless-object-inheritance
    """Serializes portions of an Environment into a gni file.

    Example gni file:

    declare_args() {
      dir_cipd_default = "<ENVIRONMENT_DIR>/cipd/packages/default"
      dir_cipd_pigweed = "<ENVIRONMENT_DIR>/cipd/packages/pigweed"
      dir_cipd_arm = "<ENVIRONMENT_DIR>/cipd/packages/arm"
      dir_cipd_python = "<ENVIRONMENT_DIR>/cipd/packages/python"
      dir_cipd_bazel = "<ENVIRONMENT_DIR>/cipd/packages/bazel"
      dir_cipd_luci = "<ENVIRONMENT_DIR>/cipd/packages/luci"
      dir_virtual_env = "<ENVIRONMENT_DIR>/pigweed-venv"
    }
    """
    def __init__(self, project_root, *args, **kwargs):
        super(GNIVisitor, self).__init__(*args, **kwargs)
        self._project_root = project_root
        self._lines = []

    def serialize(self, env, outs):
        self._lines.append('declare_args() {')

        env.accept(self)

        self._lines.append('}')

        for line in self._lines:
            print(line, file=outs)
        self._lines = []

    def visit_set(self, set):  # pylint: disable=redefined-builtin
        match = re.search(r'PW_(.*)_CIPD_INSTALL_DIR', set.name)
        if match:
            name = 'dir_cipd_{}'.format(match.group(1).lower())
            self._lines.append('  {} = "{}"'.format(name, set.value))

        if set.name == 'VIRTUAL_ENV':
            self._lines.append('  dir_virtual_env = "{}"'.format(set.value))

    def visit_clear(self, clear):
        pass

    def visit_remove(self, remove):
        pass

    def visit_prepend(self, prepend):
        pass

    def visit_append(self, append):
        pass

    def visit_echo(self, echo):
        pass

    def visit_comment(self, comment):
        pass

    def visit_command(self, command):
        pass

    def visit_doctor(self, doctor):
        pass

    def visit_blank_line(self, blank_line):
        pass

    def visit_function(self, function):
        pass

    def visit_hash(self, hash):  # pylint: disable=redefined-builtin
        pass