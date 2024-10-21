#
# Copyright (c) 2019 Juniper Networks, Inc. All rights reserved.
#

from cfgm_common import CANNOT_MODIFY_MSG
from vnc_api.gen.resource_common import RoutingInstance

from vnc_cfg_api_server.context import is_internal_request
from vnc_cfg_api_server.resources._resource_base import ResourceMixin


class RoutingInstanceServer(ResourceMixin, RoutingInstance):
    @staticmethod
    def _check_default_routing_instance(obj_dict, db_obj_dict=None):
        """Prevent to update/delete default routing instance.

        Forbidden an external call to delete a default routing instance and
        also prevent an external call to change the default flag.
        """
        if is_internal_request():
            return True, ''
        if 'routing_instance_is_default' not in obj_dict:
            return True, ''
        if not db_obj_dict and not obj_dict['routing_instance_is_default']:
            # create and delete allowed if not default RI
            return True, ''
        elif (db_obj_dict and obj_dict['routing_instance_is_default'] ==
                db_obj_dict.get('routing_instance_is_default', False)):
            # update allowed if same as before
            return True, ''

        if not db_obj_dict:
            db_obj_dict = obj_dict
        msg = CANNOT_MODIFY_MSG % {
            'resource_type':
                RoutingInstance.object_type.replace('_', ' ').title(),
            'fq_name': ':'.join(db_obj_dict['fq_name']),
            'uuid': db_obj_dict['uuid'],
        }
        return False, (409, msg)

    @classmethod
    def pre_dbe_create(cls, tenant_name, obj_dict, db_conn):
        # Does not authorize to set the routing instance ID as it's allocated
        # by the vnc server
        if obj_dict.get('routing_instance_id') is not None:
            return False, (403, "Cannot set the Routing Instance ID")

        # Allocate Routing Instance ID
        ri_id = cls.vnc_zk_client.alloc_ri_id(
            ':'.join(obj_dict['fq_name']))
        obj_dict['routing_instance_id'] = ri_id

        return cls._check_default_routing_instance(obj_dict)

    @classmethod
    def pre_dbe_update(cls, id, fq_name, obj_dict, db_conn,
                       prop_collection_updates=None, ref_update=None):
        ok, result = cls.locate(uuid=id, create_it=False, fields=[
            'parent_type', 'parent_uuid', 'routing_instance_is_default'])
        if not ok:
            return False, result
        db_obj_dict = result

        ok, read_result = cls.dbe_read(db_conn, 'routing_instance', id)
        if not ok:
            return ok, read_result

        new_ri_id = obj_dict.get('routing_instance_id')
        # Does not authorize to update the routing instance ID as it's
        # allocated by the vnc server
        if (new_ri_id is not None and
                new_ri_id != read_result.get('routing_instance_id')):
            return (False, (403, "Cannot update the routing instance ID"))

        return cls._check_default_routing_instance(obj_dict, db_obj_dict)

    @classmethod
    def pre_dbe_delete(cls, id, obj_dict, db_conn):
        # Deallocate Routing Instance ID
        cls.vnc_zk_client.free_ri_id(
            obj_dict.get('routing_instance_id'),
            ':'.join(obj_dict['fq_name']))

        return cls._check_default_routing_instance(obj_dict) + (None,)
