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
import simplejson
from datetime import datetime

from horizon import tabs, views
from django.http import HttpResponse
from django.views.generic import View

from .tabs import CeilometerOverviewTabs
from openstack_dashboard.api import ceilometer


LOG = logging.getLogger(__name__)


class IndexView(tabs.TabbedTableView):
    tab_group_class = CeilometerOverviewTabs
    template_name = 'admin/ceilometer/index.html'


class SamplesView(View):

    # converts string to date
    def _to_iso_time(self, date_str):
        date_object = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
        return date_object.isoformat(' ')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            source = request.GET.get('sample', '')
            date_from = request.GET.get('from', '')
            date_to = request.GET.get('to', '')
            query = []

            if date_from:
                date_from = self._to_iso_time(date_from+" 00:00:00")
                query.append({"field":"timestamp", "op":"ge", "value":date_from})

            if date_to:
                date_to = self._to_iso_time(date_to+" 23:59:59")
                query.append({"field":"timestamp", "op":"le", "value":date_to})

            sample_list = ceilometer.sample_list(self.request, source, query)

            # send data to chart
            samples = {}
            resources = []
            previous = {}

            for sample_data in sample_list:
                # it's cumulative, the real value is the current minus the previous
                if sample_data.resource_id in previous:
                    prev = previous[sample_data.resource_id]
                else:
                    prev = 0
                    # add sample entry
                    samples[sample_data.resource_id] = []

                current_delta = sample_data.counter_volume - prev
                previous[sample_data.resource_id] = sample_data.counter_volume 

                sample_item = {'t': sample_data.timestamp, 'v': current_delta}
                samples[sample_data.resource_id].append(sample_item)

                if sample_data.resource_id not in resources:
                    resources.append(sample_data.resource_id)

            json_string = simplejson.dumps({"resources":resources, "samples":samples}, ensure_ascii=False)
            return HttpResponse(json_string, mimetype='text/json')
        else:
            return super(SamplesView, self).get_data(request, context, *args, **kwargs)

