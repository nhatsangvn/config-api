#
# Copyright (c) 2019 Juniper Networks, Inc. All rights reserved.
#

from builtins import str
import logging
import uuid

from cfgm_common.exceptions import NoIdError
import mock
from vnc_api.vnc_api import ApplicationPolicySet
from vnc_api.vnc_api import Project

from vnc_cfg_api_server.tests import test_case

logger = logging.getLogger(__name__)


class TestProjectBase(test_case.ApiServerTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.console_handler = logging.StreamHandler()
        cls.console_handler.setLevel(logging.DEBUG)
        logger.addHandler(cls.console_handler)
        super(TestProjectBase, cls).setUpClass(*args, **kwargs)

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        logger.removeHandler(cls.console_handler)
        super(TestProjectBase, cls).tearDownClass(*args, **kwargs)

    @property
    def api(self):
        return self._vnc_lib


class TestProject(TestProjectBase):
    def test_parallel_project_cassandra_create_read(self):
        project = Project('project-%s' % self.id())
        project.uuid = str(uuid.uuid4())
        default_aps_name = 'default-%s' % ApplicationPolicySet.resource_type
        aps_fq_name = project.fq_name + [default_aps_name]
        original_fq_name_to_uuid = self._api_server._db_conn.fq_name_to_uuid
        inoked = []

        def mock_fq_name_to_uuid(obj_type, fq_name):
            if not inoked and obj_type == 'application_policy_set'\
                    and fq_name == aps_fq_name:
                inoked.append(True)
                raise NoIdError('')
            return original_fq_name_to_uuid(obj_type, fq_name)

        self.api.project_create(project)
        with mock.patch.object(self._api_server._db_conn, 'fq_name_to_uuid',
                               side_effect=mock_fq_name_to_uuid):
            self.api.project_read(id=project.uuid)

    def test_parallel_project_zk_create_read(self):
        project = Project('project-%s' % self.id())
        project.uuid = str(uuid.uuid4())
        default_aps_name = 'default-%s' % ApplicationPolicySet.resource_type
        aps_fq_name = project.fq_name + [default_aps_name]
        original_fq_name_to_uuid = self._api_server._db_conn.fq_name_to_uuid
        invoked = []

        def mock_fq_name_to_uuid(obj_type, fq_name):
            #  fq_name_to_uuid will return NoIdError  from locate
            #  and post_common which results create_fq_name_to_uuid_mapping
            #  to be called for default aps again.

            if len(invoked) < 2 and obj_type == 'application_policy_set' \
                    and fq_name == aps_fq_name:
                invoked.append(True)
                raise NoIdError('')
            return original_fq_name_to_uuid(obj_type, fq_name)

        self.api.project_create(project)
        with mock.patch.object(self._api_server._db_conn, 'fq_name_to_uuid',
                               side_effect=mock_fq_name_to_uuid):
            self.api.project_read(id=project.uuid)

    def test_allocate_mtu_value(self):
        # Create a project with MTU
        # Test case passes if project is created with defined MTU
        project = Project('project-%s' % self.id())
        project.set_mtu(8000)
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)
        mtu_id = project.get_mtu()

        self.assertIn(mtu_id, range(64, 9216))
        self.assertEqual(mtu_id, 8000)
        # end test_allocate_mtu_value

    def test_update_mtu_value(self):
        # Create a project with MTU then update MTU value
        # Test case passes if MTU value is updated properly
        project = Project('project-%s' % self.id())
        project.set_mtu(1800)
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        mtu_id = project.get_mtu()
        self.assertEqual(mtu_id, 1800)

        project.set_mtu(1600)
        self._vnc_lib.project_update(project)
        mtu_id = project.get_mtu()

        self.assertIn(mtu_id, range(64, 9216))
        self.assertEqual(mtu_id, 1600)
        # end test_update_mtu_value

    def test_deallocate_mtu_value_to_none_range(self):
        # Create a project with MTU and delete MTU value
        # Test case passes if MTU is set to None
        project = Project('project-%s' % self.id())
        project.set_mtu(1800)
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        mtu_id = project.get_mtu()
        self.assertEqual(mtu_id, 1800)

        project.set_mtu(None)
        self._vnc_lib.project_update(project)

        mtu_id = project.get_mtu()
        self.assertEqual(mtu_id, None)
        # end test_deallocate_mtu_value_to_none_range
