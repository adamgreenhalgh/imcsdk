# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nose.tools import assert_equal
from imcsdk.imcmeta import VersionMeta
from imcsdk.imccoremeta import ImcVersion
from ..connection.info import custom_setup, custom_teardown


def setup_module():
    global handle
    handle = custom_setup()


def teardown_module():
    global handle
    custom_teardown(handle)


def test_nightly_version1():
    version1 = ImcVersion("2.0(13aS6)")
    version2 = ImcVersion("3.0(1S10)")
    assert_equal((version1 < version2), True)


def test_nightly_version2():
    version1 = ImcVersion("2.0(13aS6)")
    version2 = ImcVersion("2.0(1S10)")
    assert_equal((version1 > version2), True)


def test_nightly_version3():
    # 2.0(2cS6) will be considered as 2.0(2d) internally
    version1 = ImcVersion("2.0(2cS6)")
    version2 = ImcVersion("2.0(2c)")
    assert_equal((version1 == version2), False)


def test_nightly_version4():
    version1 = ImcVersion("2.0(2cS6)")
    version2 = ImcVersion("2.0(3)")
    assert_equal((version1 < version2), True)


def test_spin_version1():
    # version interpreted as 4.0(2b)
    version1 = ImcVersion("4.0(2aS3)")
    version2 = ImcVersion("4.0(2b)")
    assert_equal((version1 == version2), True)


def test_spin_version2():
    # version interpreted as 4.0(234c)
    version1 = ImcVersion("4.0(234bS3)")
    version2 = ImcVersion("4.0(234c)")
    assert_equal((version1 == version2), True)


def test_spin_version3():
    # version interpreted as 4.0(2z)
    version1 = ImcVersion("4.0(2S3)")
    version2 = ImcVersion("4.0(2z)")
    assert_equal((version1 == version2), True)


def test_spin_version4():
    # version interpreted as 4.0(234z)
    version1 = ImcVersion("4.0(234S3)")
    version2 = ImcVersion("4.0(234z)")
    assert_equal((version1 == version2), True)


def test_patch_version1():
    # version interpreted as 4.0(235a)
    version1 = ImcVersion("4.0(234.5)")
    version2 = ImcVersion("4.0(235a)")
    assert_equal((version1 == version2), True)


def test_gt_same_major_version():
    version1 = VersionMeta.Version151f
    version2 = VersionMeta.Version151x
    assert_equal((version1 < version2), True)


def test_gt_different_major_version():
    version1 = VersionMeta.Version151x
    version2 = VersionMeta.Version202c
    assert_equal((version1 < version2), True)


def test_patch_versions():
    # when we don't see a patch version we use z
    # so 2.0(12) will be considerde as 2.0(12z)
    version1 = ImcVersion("2.0(12b)")
    version2 = ImcVersion("2.0(12)")
    assert_equal((version1 > version2), False)


def test_handle_version():
    global handle
    assert_equal(type(handle.version), ImcVersion)


def test_handle_mo_version():
    global handle
    mos = handle.query_classid("BiosUnit")
    mo_version = mos[0].get_version(platform=handle.platform)
    assert_equal((handle.version < mo_version), False)
