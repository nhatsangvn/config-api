
# AUTO-GENERATED file from IFMapApiGenerator. Do Not Edit!

from builtins import str
from builtins import range
from contrail_heat.resources import contrail
try:
    from heat.common.i18n import _
except ImportError:
    pass
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
try:
    from heat.openstack.common import log as logging
except ImportError:
    from oslo_log import log as logging
import uuid

from vnc_api import vnc_api

LOG = logging.getLogger(__name__)


class ContrailAddressGroup(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, ADDRESS_GROUP_PREFIX, ADDRESS_GROUP_PREFIX_SUBNET, ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX, ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN, DISPLAY_NAME, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, DRAFT_MODE_STATE, ID_PERMS, ID_PERMS_PERMISSIONS, ID_PERMS_PERMISSIONS_OWNER, ID_PERMS_PERMISSIONS_OWNER_ACCESS, ID_PERMS_PERMISSIONS_GROUP, ID_PERMS_PERMISSIONS_GROUP_ACCESS, ID_PERMS_PERMISSIONS_OTHER_ACCESS, ID_PERMS_UUID, ID_PERMS_UUID_UUID_MSLONG, ID_PERMS_UUID_UUID_LSLONG, ID_PERMS_ENABLE, ID_PERMS_CREATED, ID_PERMS_LAST_MODIFIED, ID_PERMS_DESCRIPTION, ID_PERMS_USER_VISIBLE, ID_PERMS_CREATOR, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, TAG_REFS, POLICY_MANAGEMENT, PROJECT
    ) = (
        'name', 'fq_name', 'address_group_prefix', 'address_group_prefix_subnet', 'address_group_prefix_subnet_ip_prefix', 'address_group_prefix_subnet_ip_prefix_len', 'display_name', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'draft_mode_state', 'id_perms', 'id_perms_permissions', 'id_perms_permissions_owner', 'id_perms_permissions_owner_access', 'id_perms_permissions_group', 'id_perms_permissions_group_access', 'id_perms_permissions_other_access', 'id_perms_uuid', 'id_perms_uuid_uuid_mslong', 'id_perms_uuid_uuid_lslong', 'id_perms_enable', 'id_perms_created', 'id_perms_last_modified', 'id_perms_description', 'id_perms_user_visible', 'id_perms_creator', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'tag_refs', 'policy_management', 'project'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('NAME.'),
            update_allowed=True,
            required=False,
        ),
        FQ_NAME: properties.Schema(
            properties.Schema.STRING,
            _('FQ_NAME.'),
            update_allowed=True,
            required=False,
        ),
        ADDRESS_GROUP_PREFIX: properties.Schema(
            properties.Schema.MAP,
            _('ADDRESS_GROUP_PREFIX.'),
            update_allowed=True,
            required=False,
            schema={
                ADDRESS_GROUP_PREFIX_SUBNET: properties.Schema(
                    properties.Schema.LIST,
                    _('ADDRESS_GROUP_PREFIX_SUBNET.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX: properties.Schema(
                                properties.Schema.STRING,
                                _('ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX.'),
                                update_allowed=True,
                                required=False,
                            ),
                            ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN: properties.Schema(
                                properties.Schema.INTEGER,
                                _('ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
            update_allowed=True,
            required=False,
        ),
        PERMS2: properties.Schema(
            properties.Schema.MAP,
            _('PERMS2.'),
            update_allowed=True,
            required=False,
            schema={
                PERMS2_OWNER: properties.Schema(
                    properties.Schema.STRING,
                    _('PERMS2_OWNER.'),
                    update_allowed=True,
                    required=False,
                ),
                PERMS2_OWNER_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_OWNER_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_GLOBAL_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_GLOBAL_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_SHARE: properties.Schema(
                    properties.Schema.LIST,
                    _('PERMS2_SHARE.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            PERMS2_SHARE_TENANT: properties.Schema(
                                properties.Schema.STRING,
                                _('PERMS2_SHARE_TENANT.'),
                                update_allowed=True,
                                required=False,
                            ),
                            PERMS2_SHARE_TENANT_ACCESS: properties.Schema(
                                properties.Schema.INTEGER,
                                _('PERMS2_SHARE_TENANT_ACCESS.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.Range(0, 7),
                                ],
                            ),
                        }
                    )
                ),
            }
        ),
        DRAFT_MODE_STATE: properties.Schema(
            properties.Schema.STRING,
            _('DRAFT_MODE_STATE.'),
            update_allowed=True,
            required=False,
        ),
        ID_PERMS: properties.Schema(
            properties.Schema.MAP,
            _('ID_PERMS.'),
            update_allowed=True,
            required=False,
            schema={
                ID_PERMS_PERMISSIONS: properties.Schema(
                    properties.Schema.MAP,
                    _('ID_PERMS_PERMISSIONS.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        ID_PERMS_PERMISSIONS_OWNER: properties.Schema(
                            properties.Schema.STRING,
                            _('ID_PERMS_PERMISSIONS_OWNER.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_PERMISSIONS_OWNER_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_OWNER_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                        ID_PERMS_PERMISSIONS_GROUP: properties.Schema(
                            properties.Schema.STRING,
                            _('ID_PERMS_PERMISSIONS_GROUP.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_PERMISSIONS_GROUP_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_GROUP_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                        ID_PERMS_PERMISSIONS_OTHER_ACCESS: properties.Schema(
                            properties.Schema.INTEGER,
                            _('ID_PERMS_PERMISSIONS_OTHER_ACCESS.'),
                            update_allowed=True,
                            required=False,
                            constraints=[
                                constraints.Range(0, 7),
                            ],
                        ),
                    }
                ),
                ID_PERMS_UUID: properties.Schema(
                    properties.Schema.MAP,
                    _('ID_PERMS_UUID.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        ID_PERMS_UUID_UUID_MSLONG: properties.Schema(
                            properties.Schema.MAP,
                            _('ID_PERMS_UUID_UUID_MSLONG.'),
                            update_allowed=True,
                            required=False,
                        ),
                        ID_PERMS_UUID_UUID_LSLONG: properties.Schema(
                            properties.Schema.MAP,
                            _('ID_PERMS_UUID_UUID_LSLONG.'),
                            update_allowed=True,
                            required=False,
                        ),
                    }
                ),
                ID_PERMS_ENABLE: properties.Schema(
                    properties.Schema.BOOLEAN,
                    _('ID_PERMS_ENABLE.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_CREATED: properties.Schema(
                    properties.Schema.INTEGER,
                    _('ID_PERMS_CREATED.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_LAST_MODIFIED: properties.Schema(
                    properties.Schema.INTEGER,
                    _('ID_PERMS_LAST_MODIFIED.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_DESCRIPTION: properties.Schema(
                    properties.Schema.STRING,
                    _('ID_PERMS_DESCRIPTION.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_USER_VISIBLE: properties.Schema(
                    properties.Schema.BOOLEAN,
                    _('ID_PERMS_USER_VISIBLE.'),
                    update_allowed=True,
                    required=False,
                ),
                ID_PERMS_CREATOR: properties.Schema(
                    properties.Schema.STRING,
                    _('ID_PERMS_CREATOR.'),
                    update_allowed=True,
                    required=False,
                ),
            }
        ),
        ANNOTATIONS: properties.Schema(
            properties.Schema.MAP,
            _('ANNOTATIONS.'),
            update_allowed=True,
            required=False,
            schema={
                ANNOTATIONS_KEY_VALUE_PAIR: properties.Schema(
                    properties.Schema.LIST,
                    _('ANNOTATIONS_KEY_VALUE_PAIR.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            ANNOTATIONS_KEY_VALUE_PAIR_KEY: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_KEY.'),
                                update_allowed=True,
                                required=False,
                            ),
                            ANNOTATIONS_KEY_VALUE_PAIR_VALUE: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_VALUE.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        POLICY_MANAGEMENT: properties.Schema(
            properties.Schema.STRING,
            _('POLICY_MANAGEMENT.'),
            update_allowed=True,
            required=False,
        ),
        PROJECT: properties.Schema(
            properties.Schema.STRING,
            _('PROJECT.'),
            update_allowed=True,
            required=False,
        ),
    }

    attributes_schema = {
        NAME: attributes.Schema(
            _('NAME.'),
        ),
        FQ_NAME: attributes.Schema(
            _('FQ_NAME.'),
        ),
        ADDRESS_GROUP_PREFIX: attributes.Schema(
            _('ADDRESS_GROUP_PREFIX.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        DRAFT_MODE_STATE: attributes.Schema(
            _('DRAFT_MODE_STATE.'),
        ),
        ID_PERMS: attributes.Schema(
            _('ID_PERMS.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        POLICY_MANAGEMENT: attributes.Schema(
            _('POLICY_MANAGEMENT.'),
        ),
        PROJECT: attributes.Schema(
            _('PROJECT.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.POLICY_MANAGEMENT) and self.properties.get(self.POLICY_MANAGEMENT) != 'config-root':
            try:
                parent_obj = self.vnc_lib().policy_management_read(fq_name_str=self.properties.get(self.POLICY_MANAGEMENT))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().policy_management_read(id=str(uuid.UUID(self.properties.get(self.POLICY_MANAGEMENT))))
            except:
                parent_obj = None
        if parent_obj is None and self.properties.get(self.PROJECT) and self.properties.get(self.PROJECT) != 'config-root':
            try:
                parent_obj = self.vnc_lib().project_read(fq_name_str=self.properties.get(self.PROJECT))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(self.properties.get(self.PROJECT))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            tenant_id = self.stack.context.tenant_id
            parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(tenant_id)))

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.AddressGroup(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.ADDRESS_GROUP_PREFIX) is not None:
            obj_1 = vnc_api.SubnetListType()
            if self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET) is not None:
                for index_1 in range(len(self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET))):
                    obj_2 = vnc_api.SubnetType()
                    if self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX) is not None:
                        obj_2.set_ip_prefix(self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX))
                    if self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN) is not None:
                        obj_2.set_ip_prefix_len(self.properties.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN))
                    obj_1.add_subnet(obj_2)
            obj_0.set_address_group_prefix(obj_1)
        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.PERMS2) is not None:
            obj_1 = vnc_api.PermType2()
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER) is not None:
                obj_1.set_owner(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS) is not None:
                obj_1.set_owner_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS) is not None:
                obj_1.set_global_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE) is not None:
                for index_1 in range(len(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE))):
                    obj_2 = vnc_api.ShareType()
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT) is not None:
                        obj_2.set_tenant(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT))
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS) is not None:
                        obj_2.set_tenant_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS))
                    obj_1.add_share(obj_2)
            obj_0.set_perms2(obj_1)
        if self.properties.get(self.DRAFT_MODE_STATE) is not None:
            obj_0.set_draft_mode_state(self.properties.get(self.DRAFT_MODE_STATE))
        if self.properties.get(self.ID_PERMS) is not None:
            obj_1 = vnc_api.IdPermsType()
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS) is not None:
                obj_2 = vnc_api.PermType()
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER) is not None:
                    obj_2.set_owner(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS) is not None:
                    obj_2.set_owner_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP) is not None:
                    obj_2.set_group(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS) is not None:
                    obj_2.set_group_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS) is not None:
                    obj_2.set_other_access(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS))
                obj_1.set_permissions(obj_2)
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID) is not None:
                obj_2 = vnc_api.UuidType()
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG) is not None:
                    obj_2.set_uuid_mslong(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG))
                if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG) is not None:
                    obj_2.set_uuid_lslong(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG))
                obj_1.set_uuid(obj_2)
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE) is not None:
                obj_1.set_enable(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED) is not None:
                obj_1.set_created(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED) is not None:
                obj_1.set_last_modified(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION) is not None:
                obj_1.set_description(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE) is not None:
                obj_1.set_user_visible(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE))
            if self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR) is not None:
                obj_1.set_creator(self.properties.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR))
            obj_0.set_id_perms(obj_1)
        if self.properties.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)

        # reference to tag_refs
        if self.properties.get(self.TAG_REFS):
            for index_0 in range(len(self.properties.get(self.TAG_REFS))):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_tag(ref_obj)

        try:
            obj_uuid = super(ContrailAddressGroup, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().address_group_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.ADDRESS_GROUP_PREFIX) is not None:
            obj_1 = vnc_api.SubnetListType()
            if prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET) is not None:
                for index_1 in range(len(prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET))):
                    obj_2 = vnc_api.SubnetType()
                    if prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX) is not None:
                        obj_2.set_ip_prefix(prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX))
                    if prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN) is not None:
                        obj_2.set_ip_prefix_len(prop_diff.get(self.ADDRESS_GROUP_PREFIX, {}).get(self.ADDRESS_GROUP_PREFIX_SUBNET, {})[index_1].get(self.ADDRESS_GROUP_PREFIX_SUBNET_IP_PREFIX_LEN))
                    obj_1.add_subnet(obj_2)
            obj_0.set_address_group_prefix(obj_1)
        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.ID_PERMS) is not None:
            obj_1 = vnc_api.IdPermsType()
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS) is not None:
                obj_2 = vnc_api.PermType()
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER) is not None:
                    obj_2.set_owner(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER))
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS) is not None:
                    obj_2.set_owner_access(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OWNER_ACCESS))
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP) is not None:
                    obj_2.set_group(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP))
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS) is not None:
                    obj_2.set_group_access(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_GROUP_ACCESS))
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS) is not None:
                    obj_2.set_other_access(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_PERMISSIONS, {}).get(self.ID_PERMS_PERMISSIONS_OTHER_ACCESS))
                obj_1.set_permissions(obj_2)
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID) is not None:
                obj_2 = vnc_api.UuidType()
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG) is not None:
                    obj_2.set_uuid_mslong(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_MSLONG))
                if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG) is not None:
                    obj_2.set_uuid_lslong(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_UUID, {}).get(self.ID_PERMS_UUID_UUID_LSLONG))
                obj_1.set_uuid(obj_2)
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE) is not None:
                obj_1.set_enable(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_ENABLE))
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED) is not None:
                obj_1.set_created(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATED))
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED) is not None:
                obj_1.set_last_modified(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_LAST_MODIFIED))
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION) is not None:
                obj_1.set_description(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_DESCRIPTION))
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE) is not None:
                obj_1.set_user_visible(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_USER_VISIBLE))
            if prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR) is not None:
                obj_1.set_creator(prop_diff.get(self.ID_PERMS, {}).get(self.ID_PERMS_CREATOR))
            obj_0.set_id_perms(obj_1)
        if prop_diff.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)

        # reference to tag_refs
        ref_obj_list = []
        if self.TAG_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.TAG_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_tag_list(ref_obj_list)
            # End: reference to tag_refs

        try:
            self.vnc_lib().address_group_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().address_group_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('address_group %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().address_group_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::AddressGroup': ContrailAddressGroup,
    }
