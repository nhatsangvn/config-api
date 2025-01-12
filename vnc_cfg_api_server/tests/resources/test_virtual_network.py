#
# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.
#
import logging

from cfgm_common import get_bgp_rtgt_min_id
from cfgm_common import VNID_MIN_ALLOC
from cfgm_common.exceptions import BadRequest
from cfgm_common.exceptions import HttpError
from cfgm_common.exceptions import PermissionDenied
from cfgm_common.exceptions import RefsExistError
from cfgm_common.tests import test_common
from testtools import ExpectedException
from vnc_api.vnc_api import GlobalSystemConfig
from vnc_api.vnc_api import Project
from vnc_api.vnc_api import ProviderDetails
from vnc_api.vnc_api import RouteTargetList
from vnc_api.vnc_api import VirtualMachineInterface
from vnc_api.vnc_api import VirtualNetwork
from vnc_api.vnc_api import VirtualNetworkType

from vnc_cfg_api_server.tests import test_case

logger = logging.getLogger(__name__)


class TestVirtualNetwork(test_case.ApiServerTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        cls.console_handler = logging.StreamHandler()
        cls.console_handler.setLevel(logging.DEBUG)
        logger.addHandler(cls.console_handler)
        super(TestVirtualNetwork, cls).setUpClass(*args, **kwargs)

    @classmethod
    def tearDownClass(cls, *args, **kwargs):
        logger.removeHandler(cls.console_handler)
        super(TestVirtualNetwork, cls).tearDownClass(*args, **kwargs)

    @property
    def api(self):
        return self._vnc_lib

    def test_allocate_vn_id(self):
        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        self.api.virtual_network_create(vn_obj)

        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_id = vn_obj.virtual_network_network_id
        self.assertEqual(vn_obj.get_fq_name_str(),
                         mock_zk.get_vn_from_id(vn_id))
        self.assertGreaterEqual(vn_id, VNID_MIN_ALLOC)

    def test_deallocate_vn_id(self):
        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())
        self.api.virtual_network_create(vn_obj)
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_id = vn_obj.virtual_network_network_id

        self.api.virtual_network_delete(id=vn_obj.uuid)

        self.assertNotEqual(mock_zk.get_vn_from_id(vn_id),
                            vn_obj.get_fq_name_str())

    def test_not_deallocate_vn_id_if_fq_name_does_not_correspond(self):
        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())
        self.api.virtual_network_create(vn_obj)
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_id = vn_obj.virtual_network_network_id

        fake_fq_name = "fake fq_name"
        mock_zk._vn_id_allocator.delete(vn_id - VNID_MIN_ALLOC)
        mock_zk._vn_id_allocator.reserve(vn_id - VNID_MIN_ALLOC, fake_fq_name)
        self.api.virtual_network_delete(id=vn_obj.uuid)

        self.assertIsNotNone(mock_zk.get_vn_from_id(vn_id))
        self.assertEqual(fake_fq_name, mock_zk.get_vn_from_id(vn_id))

    def test_cannot_set_vn_id(self):
        vn_obj = VirtualNetwork('%s-vn' % self.id())
        vn_obj.set_virtual_network_network_id(42)

        with ExpectedException(PermissionDenied):
            self.api.virtual_network_create(vn_obj)

    def test_cannot_update_vn_id(self):
        vn_obj = VirtualNetwork('%s-vn' % self.id())
        self.api.virtual_network_create(vn_obj)
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)

        vn_obj.set_virtual_network_network_id(42)
        with ExpectedException(PermissionDenied):
            self.api.virtual_network_update(vn_obj)

        # test can update with same value, needed internally
        # TODO(ethuleau): not sure why it's needed
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj.set_virtual_network_network_id(
            vn_obj.virtual_network_network_id)
        self.api.virtual_network_update(vn_obj)

    def test_create_vn_with_configured_rt_in_system_range(self):
        gsc = self.api.global_system_config_read(GlobalSystemConfig().fq_name)
        vn = VirtualNetwork('%s-vn' % self.id())
        rt_name = 'target:%d:%d' % (gsc.autonomous_system,
                                    get_bgp_rtgt_min_id(
                                        gsc.autonomous_system) + 1000)
        vn.set_route_target_list(RouteTargetList([rt_name]))

        self.assertRaises(BadRequest, self.api.virtual_network_create, vn)

    def test_update_vn_with_configured_rt_in_system_range(self):
        gsc = self.api.global_system_config_read(GlobalSystemConfig().fq_name)
        vn = VirtualNetwork('%s-vn' % self.id())
        self.api.virtual_network_create(vn)

        rt_name = 'target:%d:%d' % (gsc.autonomous_system,
                                    get_bgp_rtgt_min_id(
                                        gsc.autonomous_system) + 1000)
        vn.set_route_target_list(RouteTargetList([rt_name]))
        self.assertRaises(BadRequest, self.api.virtual_network_update, vn)

    def test_allocate_vxlan_id(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(6000)
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if vxlan_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties = vn_obj.get_virtual_network_properties()
        if not vn_obj_properties:
            self.fail("VN properties are not set")
        vxlan_id = vn_obj_properties.get_vxlan_network_identifier()
        self.assertEqual(vxlan_id, 6000)
        self.assertEqual(vn_obj.get_fq_name_str() + "_vxlan",
                         mock_zk.get_vn_from_id(vxlan_id))
        self.assertGreaterEqual(vxlan_id, VNID_MIN_ALLOC)

        self.api.virtual_network_delete(id=vn_obj.uuid)
        logger.debug('PASS - test_allocate_vxlan_id')

    def test_cannot_allocate_vxlan_id(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn1_obj = VirtualNetwork('%s-vn' % self.id())

        vn1_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn1_obj_properties.set_vxlan_network_identifier(6001)
        vn1_obj_properties.set_forwarding_mode('l2_l3')
        vn1_obj.set_virtual_network_properties(vn1_obj_properties)

        self.api.virtual_network_create(vn1_obj)

        # VN created, now read back the VN data to check if vxlan_id is set
        vn1_obj = self.api.virtual_network_read(id=vn1_obj.uuid)
        vn1_obj_properties = vn1_obj.get_virtual_network_properties()
        if not vn1_obj_properties:
            self.fail("VN properties are not set")
        vxlan_id = vn1_obj_properties.get_vxlan_network_identifier()
        self.assertEqual(vxlan_id, 6001)

        # Verified vxlan_id for VN1, now create VN2 with same vxlan_id
        vn2_obj = VirtualNetwork('%s-vn2' % self.id())
        vn2_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn2_obj_properties.set_vxlan_network_identifier(6001)
        vn2_obj_properties.set_forwarding_mode('l2_l3')
        vn2_obj.set_virtual_network_properties(vn2_obj_properties)

        with ExpectedException(BadRequest):
            self.api.virtual_network_create(vn2_obj)

        self.assertEqual(vn1_obj.get_fq_name_str() + "_vxlan",
                         mock_zk.get_vn_from_id(vxlan_id))
        self.assertGreaterEqual(vxlan_id, VNID_MIN_ALLOC)
        self.api.virtual_network_delete(id=vn1_obj.uuid)
        logger.debug('PASS - test_cannot_allocate_vxlan_id')

    def test_deallocate_vxlan_id(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(6002)
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if vxlan_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties = vn_obj.get_virtual_network_properties()
        if not vn_obj_properties:
            self.fail("VN properties are not set")
        vxlan_id = vn_obj_properties.get_vxlan_network_identifier()
        self.assertEqual(vxlan_id, 6002)

        self.api.virtual_network_delete(id=vn_obj.uuid)
        self.assertNotEqual(vn_obj.get_fq_name_str() + "_vxlan",
                            mock_zk.get_vn_from_id(vxlan_id))
        logger.debug('PASS - test_deallocate_vxlan_id')

    def test_update_vxlan_id(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(6003)
        vn_obj_properties.set_forwarding_mode('l2_l3')
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if vxlan_id is set
        vn_obj_read = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        vxlan_id = vn_obj_properties_read.get_vxlan_network_identifier()
        self.assertEqual(vxlan_id, 6003)

        # Created VN. Now Update it with a different vxlan_id
        vn_obj_properties.set_vxlan_network_identifier(6004)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_update(vn_obj)

        vn_obj_read = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        vxlan_id = vn_obj_properties_read.get_vxlan_network_identifier()

        self.assertEqual(vxlan_id, 6004)
        self.api.virtual_network_delete(id=vn_obj.uuid)
        logger.debug('PASS - test_update_vxlan_id')

    def test_cannot_update_vxlan_id(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        vn1_obj = VirtualNetwork('%s-vn1' % self.id())

        vn1_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn1_obj_properties.set_vxlan_network_identifier(6005)
        vn1_obj_properties.set_forwarding_mode('l2_l3')
        vn1_obj.set_virtual_network_properties(vn1_obj_properties)

        self.api.virtual_network_create(vn1_obj)

        # VN created, create second VN with different vxlan_id
        vn2_obj = VirtualNetwork('%s-vn2' % self.id())

        vn2_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn2_obj_properties.set_vxlan_network_identifier(6006)
        vn2_obj_properties.set_forwarding_mode('l2_l3')
        vn2_obj.set_virtual_network_properties(vn2_obj_properties)

        self.api.virtual_network_create(vn2_obj)

        # Created Two VNs. Now Update it second VN with 1st VNs VXLAN_ID
        vn2_obj_properties.set_vxlan_network_identifier(6005)
        vn2_obj.set_virtual_network_properties(vn2_obj_properties)

        with ExpectedException(BadRequest):
            self.api.virtual_network_update(vn2_obj)

        vn_obj_read = self.api.virtual_network_read(id=vn2_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        vxlan_id = vn_obj_properties_read.get_vxlan_network_identifier()
        self.assertEqual(vxlan_id, 6006)

        self.api.virtual_network_delete(id=vn2_obj.uuid)
        self.api.virtual_network_delete(id=vn1_obj.uuid)
        logger.debug('PASS - test_cannot_update_vxlan_id')

    def test_update_auto_vxlan_id_with_the_same_value(self):
        """
        Test case.

        1. Set VxLAN identifier mode to 'automatic'.
        2. Create new VirtualNetwork.
        3. Set VxLAN identifier mode to 'configured'.
        4. Update VirtualNetwork with vxlan network identifier equal to
           network id.
        """
        gvc_fq_name = ['default-global-system-config',
                       'default-global-vrouter-config']
        vxlan_id_mode = {'auto': 'automatic', 'user': 'configured'}

        # Set VxLAN identifier mode to 'automatic'
        gvc = self.api.global_vrouter_config_read(fq_name=gvc_fq_name)
        gvc.set_vxlan_network_identifier_mode(vxlan_id_mode['auto'])
        self.api.global_vrouter_config_update(gvc)
        gvc = self.api.global_vrouter_config_read(fq_name=gvc_fq_name)
        # verify vxlan id mode has been set
        self.assertEqual(gvc.vxlan_network_identifier_mode,
                         vxlan_id_mode['auto'])

        # Create new VirtualNetwork
        vn = VirtualNetwork('%s-vn' % self.id())
        self.api.virtual_network_create(vn)
        vn = self.api.virtual_network_read(fq_name=vn.fq_name)
        # verify vn_network_id has been set
        vn_network_id = vn.get_virtual_network_network_id()
        self.assertTrue(vn_network_id > 0)

        # Set VxLAN identifier mode to 'configured' (user defined)
        gvc.set_vxlan_network_identifier_mode(vxlan_id_mode['user'])
        self.api.global_vrouter_config_update(gvc)
        gvc = self.api.global_vrouter_config_read(fq_name=gvc_fq_name)
        # verify vxlan id mode has been set
        self.assertEqual(gvc.vxlan_network_identifier_mode,
                         vxlan_id_mode['user'])

        # Update VirtualNetwork with vxlan network identifier
        # equal to network id
        vn_properties = VirtualNetworkType()
        vn_properties.set_vxlan_network_identifier(vn_network_id)
        vn.set_virtual_network_properties(vn_properties)
        self.api.virtual_network_update(vn)
        # verify vn_network_id is the same as vxlan_network_id
        vn = self.api.virtual_network_read(fq_name=vn.fq_name)
        vxlan_id = vn.get_virtual_network_properties() \
            .get_vxlan_network_identifier()
        self.assertEqual(vn_network_id, vxlan_id)

    def test_context_undo_fail_db_create(self):
        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())
        zk_alloc_count_start = mock_zk._vn_id_allocator.get_alloc_count()

        def stub(*args, **kwargs):
            return (False, (500, "Fake error"))

        with ExpectedException(HttpError):
            with test_common.flexmocks(
                    [(self._api_server._db_conn, 'dbe_create', stub)]):
                self.api.virtual_network_create(vn_obj)

        zk_alloc_count_current = mock_zk._vn_id_allocator.get_alloc_count()
        self.assertEqual(zk_alloc_count_start, zk_alloc_count_current)

    def test_context_undo_vxlan_id_fail_db_create(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(6000)
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        def stub(*args, **kwargs):
            return (False, (500, "Fake error"))

        zk_alloc_count_start = mock_zk._vn_id_allocator.get_alloc_count()
        with ExpectedException(HttpError):
            with test_common.flexmocks(
                    [(self._api_server._db_conn, 'dbe_create', stub)]):
                self.api.virtual_network_create(vn_obj)

        # make sure allocation counter stays the same
        zk_alloc_count_current = mock_zk._vn_id_allocator.get_alloc_count()
        self.assertEqual(zk_alloc_count_start, zk_alloc_count_current)

    def test_context_undo_fail_db_delete(self):
        vn_obj = self.create_virtual_network('vn-l2-%s' % self.id())
        vn_ipam_refs = vn_obj.get_network_ipam_refs()

        mock_zk = self._api_server._db_conn._zk_db
        zk_alloc_count_start = mock_zk._vn_id_allocator.get_alloc_count()

        def stub(*args, **kwargs):
            return (False, (500, "Fake error"))

        with ExpectedException(HttpError):
            with test_common.flexmocks(
                    [(self._api_server._db_conn, 'dbe_delete', stub)]):
                self.api.virtual_network_delete(id=vn_obj.uuid)

        # Make sure ipam refs still present (undo action recreated it)
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_ipam_refs_after_delete_fail = vn_obj.get_network_ipam_refs()

        self.assertEqual(vn_ipam_refs[0]['to'],
                         vn_ipam_refs_after_delete_fail[0]['to'])
        self.assertEqual(vn_ipam_refs[0]['uuid'],
                         vn_ipam_refs_after_delete_fail[0]['uuid'])
        self.assertEqual(vn_ipam_refs[0]['attr'].ipam_subnets[0].subnet_uuid,
                         vn_ipam_refs_after_delete_fail[0][
                             'attr'].ipam_subnets[0].subnet_uuid)
        # Make sure allocation counter stays the same
        zk_alloc_count_current = mock_zk._vn_id_allocator.get_alloc_count()
        self.assertEqual(zk_alloc_count_start, zk_alloc_count_current)

    def test_context_undo_vxlan_id_fail_db_update(self):
        # enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        # Create vxlan
        vxlan_id = 6000
        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(vxlan_id)
        vn_obj_properties.set_forwarding_mode('l2_l3')
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        self.api.virtual_network_create(vn_obj)

        vxlan_fqname = mock_zk.get_vn_from_id(vxlan_id)
        # Update vxlan id (will fail)
        new_vxlan_id = 6005
        vn_obj_properties.set_vxlan_network_identifier(new_vxlan_id)
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        def stub(*args, **kwargs):
            return (False, (500, "Fake error"))

        zk_alloc_count_start = mock_zk._vn_id_allocator.get_alloc_count()
        with ExpectedException(HttpError):
            with test_common.flexmocks(
                    [(self._api_server._db_conn, 'dbe_update', stub)]):
                self.api.virtual_network_update(vn_obj)

        # Make sure vxlan_id is still allocated with same name
        new_vxlan_fqname = mock_zk.get_vn_from_id(vxlan_id)
        self.assertEqual(new_vxlan_fqname, vxlan_fqname)

        # Make sure new_vxlan_id is deallocated
        update_vxlan_fqname = mock_zk.get_vn_from_id(new_vxlan_id)
        self.assertEqual(update_vxlan_fqname, None)

        # Make sure allocation counter stays the same
        zk_alloc_count_current = mock_zk._vn_id_allocator.get_alloc_count()
        self.assertEqual(zk_alloc_count_start, zk_alloc_count_current)

    def test_context_undo_vn_to_vxlan_id_fail_db_update(self):
        # Enable vxlan routing on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        proj.set_vxlan_routing(True)
        self._vnc_lib.project_update(proj)

        mock_zk = self._api_server._db_conn._zk_db
        vn_obj = VirtualNetwork('%s-vn' % self.id())

        self.api.virtual_network_create(vn_obj)

        vn_fqname = mock_zk.get_vn_from_id(vn_obj.virtual_network_network_id)
        vn_id = vn_obj.virtual_network_network_id

        # Change vn to vxlan type
        vxlan_id = 6000
        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_vxlan_network_identifier(vxlan_id)
        vn_obj_properties.set_forwarding_mode('l2_l3')
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        def stub(*args, **kwargs):
            return (False, (500, "Fake error"))

        zk_alloc_count_start = mock_zk._vn_id_allocator.get_alloc_count()
        with ExpectedException(HttpError):
            with test_common.flexmocks(
                    [(self._api_server._db_conn, 'dbe_update', stub)]):
                self.api.virtual_network_update(vn_obj)

        # Make sure vxlan_id was dealocated
        new_vxlan_fqname = mock_zk.get_vn_from_id(vxlan_id)
        self.assertEqual(new_vxlan_fqname, None)

        # Make sure vn id is the same
        new_vn_id = vn_obj.virtual_network_network_id
        self.assertEqual(vn_id, new_vn_id)

        # Make sure fqname is the same fot vn_id
        update_vn_fqname = mock_zk.get_vn_from_id(
            vn_obj.virtual_network_network_id)
        self.assertEqual(vn_fqname, update_vn_fqname)

        # Make sure allocation counter stays the same
        zk_alloc_count_current = mock_zk._vn_id_allocator.get_alloc_count()
        self.assertEqual(zk_alloc_count_start, zk_alloc_count_current)

    def test_create_provider_vn(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 100,
                             "physical_network": "physnet1"}))
        vn_uuid = self.api.virtual_network_create(vn)

        is_provider_network = (self
                               .api.virtual_network_read(id=vn_uuid)
                               .get_is_provider_network())
        self.assertTrue(is_provider_network)
    # end test_create_provider_vn

    def test_create_provider_vn_without_provider_details(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn.set_is_provider_network(True)
        vn_uuid = self.api.virtual_network_create(vn)

        is_provider_network = (self
                               .api.virtual_network_read(id=vn_uuid)
                               .get_is_provider_network())
        self.assertTrue(is_provider_network)
    # end test_create_provider_vn_without_provider_details

    def test_update_not_in_use_non_provider_vn_to_provider(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn_uuid = self.api.virtual_network_create(vn)
        vn = self.api.virtual_network_read(id=vn_uuid)
        is_provider_network = vn.get_is_provider_network()
        self.assertFalse(is_provider_network)

        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 100,
                             "physical_network": "physnet1"}))
        self.api.virtual_network_update(vn)

        vn = self.api.virtual_network_read(id=vn_uuid)
        is_provider_network = vn.get_is_provider_network()
        self.assertTrue(is_provider_network)

        updated_provider_properties = vn.get_provider_properties()
        segmentation_id = updated_provider_properties.get_segmentation_id()
        physical_network = updated_provider_properties.get_physical_network()

        self.assertEqual((100, "physnet1"),
                         (segmentation_id, physical_network))
    # end test_update_non_provider_vn_to_provider

    def test_update_non_provider_vn_to_provider_without_provider_details(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn_uuid = self.api.virtual_network_create(vn)
        vn = self.api.virtual_network_read(id=vn_uuid)
        is_provider_network = vn.get_is_provider_network()
        self.assertFalse(is_provider_network)

        vn.set_is_provider_network(True)
        self.api.virtual_network_update(vn)

        vn = self.api.virtual_network_read(id=vn_uuid)
        is_provider_network = vn.get_is_provider_network()
        self.assertTrue(is_provider_network)
    # end test_update_non_provider_vn_to_provider_without_provider_details

    def test_update_in_use_vn_to_provider_vn(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn_uuid = self.api.virtual_network_create(vn)

        vmi = VirtualMachineInterface('%s-vmi' % self.id(), parent_obj=project)
        vmi.set_virtual_network(vn)
        self.api.virtual_machine_interface_create(vmi)

        vn = self.api.virtual_network_read(id=vn_uuid)

        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 100,
                             "physical_network": "physnet1"}))
        self.api.virtual_network_update(vn)

        updated_provider_properties = (self
                                       .api.virtual_network_read(id=vn.uuid)
                                       .get_provider_properties())
        segmentation_id = updated_provider_properties.get_segmentation_id()
        physical_network = updated_provider_properties.get_physical_network()

        self.assertEqual((100, "physnet1"),
                         (segmentation_id, physical_network))
    # end test_update_in_use_vn_to_provider_vn

    def test_update_in_use_vn_to_provider_vn_without_physnet_label(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn_uuid = self.api.virtual_network_create(vn)

        vmi = VirtualMachineInterface('%s-vmi' % self.id(), parent_obj=project)
        vmi.set_virtual_network(vn)
        self.api.virtual_machine_interface_create(vmi)

        vn = self.api.virtual_network_read(id=vn_uuid)

        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 100}))
        with ExpectedException(RefsExistError):
            self.api.virtual_network_update(vn)

        updated_provider_properties = (self
                                       .api.virtual_network_read(id=vn.uuid)
                                       .get_provider_properties())

        self.assertEqual(None, updated_provider_properties)
    # end test_update_in_use_vn_to_provider_vn_without_physnet_label

    def test_update_in_use_vn_to_provider_vn_without_segmentation(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn_uuid = self.api.virtual_network_create(vn)

        vmi = VirtualMachineInterface('%s-vmi' % self.id(), parent_obj=project)
        vmi.set_virtual_network(vn)
        self.api.virtual_machine_interface_create(vmi)

        vn = self.api.virtual_network_read(id=vn_uuid)

        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"physical_network": "physnet1"}))
        with ExpectedException(RefsExistError):
            self.api.virtual_network_update(vn)

        updated_provider_properties = (self
                                       .api.virtual_network_read(id=vn.uuid)
                                       .get_provider_properties())

        self.assertEqual(None, updated_provider_properties)
    # end test_update_in_use_vn_to_provider_vn_without_segmentation

    def test_update_in_use_provider_vn(self):
        project = Project('%s-project' % self.id())
        project_uuid = self.api.project_create(project)
        project = self.api.project_read(id=project_uuid)

        vn = VirtualNetwork('%s-vn' % self.id(), parent_obj=project)
        vn.set_is_provider_network(True)
        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 100,
                             "physical_network": "physnet1"}))
        vn_uuid = self.api.virtual_network_create(vn)

        vmi = VirtualMachineInterface('%s-vmi' % self.id(), parent_obj=project)
        vmi.set_virtual_network(vn)
        self.api.virtual_machine_interface_create(vmi)

        vn = self.api.virtual_network_read(id=vn_uuid)

        vn.set_provider_properties(
            ProviderDetails(
                params_dict={"segmentation_id": 200,
                             "physical_network": "physnet2"}))
        with ExpectedException(RefsExistError):
            self.api.virtual_network_update(vn)

        updated_provider_properties = (self
                                       .api.virtual_network_read(id=vn.uuid)
                                       .get_provider_properties())
        segmentation_id = updated_provider_properties.get_segmentation_id()
        physical_network = updated_provider_properties.get_physical_network()

        self.assertEqual((100, "physnet1"),
                         (segmentation_id, physical_network))
    # end test_update_in_use_provider_vn

    def test_allocate_mtu_value_range(self):
        # enable MTU value on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        self._vnc_lib.project_update(proj)

        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_mtu(8000)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if MTU_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties = vn_obj.get_virtual_network_properties()
        if not vn_obj_properties:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties.get_mtu()
        if mtu_id in range(64, 9216):
            self.assertEqual(mtu_id, 8000)
            logger.debug('PASS - test_allocate_mtu_range_value')
        else:
            logger.debug('FAIL -test allocate_mtu_range_value')
        self.api.virtual_network_delete(id=vn_obj.uuid)

    def test_update_mtu(self):
        # enable mtu on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        self._vnc_lib.project_update(proj)

        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_mtu(3000)
        vn_obj_properties.set_forwarding_mode('l2_l3')
        vn_obj.set_virtual_network_properties(vn_obj_properties)

        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if mtu_id is set
        vn_obj_read = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties_read.get_mtu()
        self.assertEqual(mtu_id, 3000)

        # Created VN. Now Update it with a different mtu_id
        vn_obj_properties.set_mtu(8000)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_update(vn_obj)

        vn_obj_read = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties_read.get_mtu()

        self.assertEqual(mtu_id, 8000)
        self.api.virtual_network_delete(id=vn_obj.uuid)
        logger.debug('PASS - test_update_mtu_value')

    def test_deallocate_mtu_value_to_none_range(self):
        # enable MTU value on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        self._vnc_lib.project_update(proj)

        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_mtu(2000)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if MTU_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties = vn_obj.get_virtual_network_properties()
        if not vn_obj_properties:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties.get_mtu()
        self.assertEqual(mtu_id, 2000)
        # Created VN. Now Update it with a different mtu_id
        vn_obj_properties.set_mtu(None)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_update(vn_obj)

        vn_obj_read = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties_read = vn_obj_read.get_virtual_network_properties()
        if not vn_obj_properties_read:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties_read.get_mtu()

        self.assertEqual(mtu_id, None)
        self.api.virtual_network_delete(id=vn_obj.uuid)
        logger.debug('PASS - test_update_mtu_none_value')

    def test_default_mtu_value_range(self):
        # enable MTU value on project
        proj = self._vnc_lib.project_read(
            fq_name=["default-domain", "default-project"])
        self._vnc_lib.project_update(proj)

        vn_obj = VirtualNetwork('%s-vn' % self.id())

        vn_obj_properties = VirtualNetworkType(forwarding_mode='l3')
        vn_obj_properties.set_mtu(None)
        vn_obj.set_virtual_network_properties(vn_obj_properties)
        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if MTU_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        vn_obj_properties = vn_obj.get_virtual_network_properties()
        if not vn_obj_properties:
            self.fail("VN properties are not set")
        mtu_id = vn_obj_properties.get_mtu()
        if mtu_id in range(64, 9216) or None:
            self.assertEqual(mtu_id, None)
            logger.debug('PASS - test_allocate_mtu_range_value')
        else:
            logger.debug('FAIL -test allocate_mtu_range_value')
        self.api.virtual_network_delete(id=vn_obj.uuid)

    def test_network_mtu_allocate_from_tenant(self):
        # Create Project with MTU, create VN with no MTU set
        # Test case passes if project MTU is set on VN

        proj_obj = Project('%s-project' % self.id())
        proj_obj.set_mtu(1600)
        proj_uuid = self.api.project_create(proj_obj)
        new_proj_obj = self._vnc_lib.project_read(id=proj_uuid)

        vn_obj = VirtualNetwork('%s-vn' % self.id(), parent_obj=new_proj_obj)
        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if MTU_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        mtu_id = vn_obj.get_mtu()
        self.assertIn(mtu_id, range(64, 9216))
        self.assertEqual(mtu_id, 1600)
        self.api.virtual_network_delete(id=vn_obj.uuid)
        self._vnc_lib.project_delete(id=new_proj_obj.uuid)
        # end test_network_mtu_allocate_from_tenant

    def test_network_mtu_allocate_default_mtu(self):
        # Create project and VN without MTU
        # Test case passes if VN uses deafult 1500 MTU value

        proj_obj = Project('%s-project' % self.id())
        proj_uuid = self.api.project_create(proj_obj)
        new_proj_obj = self._vnc_lib.project_read(id=proj_uuid)

        vn_obj = VirtualNetwork('%s-vn' % self.id(), parent_obj=new_proj_obj)
        self.api.virtual_network_create(vn_obj)

        # VN created, now read back the VN data to check if MTU_id is set
        vn_obj = self.api.virtual_network_read(id=vn_obj.uuid)
        mtu_id = vn_obj.get_mtu()
        self.assertIn(mtu_id, range(64, 9216))
        self.assertEqual(mtu_id, 1500)
        self.api.virtual_network_delete(id=vn_obj.uuid)
        self._vnc_lib.project_delete(id=new_proj_obj.uuid)
        # end test_network_mtu_allocate_default_mtu
