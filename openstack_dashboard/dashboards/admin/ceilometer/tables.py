
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.templatetags.sizeformat import filesizeformat, float_format


LOG = logging.getLogger(__name__)


class DiskUsageFilterAction(tables.FilterAction):
    def filter(self, table, tenants, filter_string):
        q = filter_string.lower()

        def comp(tenant):
            if q in tenant.name.lower():
                return True
            return False

        return filter(comp, tenants)


class  DiskUsageTable(tables.DataTable):
    tenant = tables.Column("tenant", verbose_name=_("Tenant"))
    user = tables.Column("user", verbose_name=_("User"))
    instance = tables.Column("resource", verbose_name=_("Resource"))
    disk_read_bytes = tables.Column("disk_read_bytes",
                            verbose_name=_("Disk Read Bytes"), summation="sum")
    disk_read_requests = tables.Column("disk_read_requests",
                            verbose_name=_("Disk Read Requests"), summation="sum")
    disk_write_bytes = tables.Column("disk_write_bytes",
                            verbose_name=_("Disk Write Bytes"), summation="sum")
    disk_write_requests = tables.Column("disk_write_requests",
                            verbose_name=_("Disk Write Requests"), summation="sum")

    def get_object_id(self, datum):
        return datum.tenant + datum.user + datum.resource

    class Meta:
        name = "global_disk_usage"
        verbose_name = _("Global Disk Usage")
        table_actions = (DiskUsageFilterAction,)
        multi_select = False
        template = "admin/ceilometer/table_with_date_selectors.html"


class NetworkUsageFilterAction(tables.FilterAction):
    def filter(self, table, tenants, filter_string):
        q = filter_string.lower()

        def comp(tenant):
            if q in tenant.name.lower():
                return True
            return False

        return filter(comp, tenants)


class  NetworkUsageTable(tables.DataTable):
    tenant = tables.Column("tenant", verbose_name=_("Tenant"))
    user = tables.Column("user", verbose_name=_("User"))
    instance = tables.Column("resource", verbose_name=_("Resource"))
    network_incoming_bytes = tables.Column("network_incoming_bytes",
                            verbose_name=_("Network incoming Bytes"))
    network_incoming_packets = tables.Column("network_incoming_packets",
                            verbose_name=_("Network incoming Packets"))
    network_outgoing_bytes = tables.Column("network_outgoing_bytes",
                            verbose_name=_("Network Outgoing Bytes"))
    network_outgoing_packets = tables.Column("network_outgoing_packets",
                            verbose_name=_("Network Outgoing Packets"))

    def get_object_id(self, datum):
        return datum.tenant + datum.user + datum.resource

    class Meta:
        name = "global_network_usage"
        verbose_name = _("Global Network Usage")
        table_actions = (NetworkUsageFilterAction,)
        multi_select = False
