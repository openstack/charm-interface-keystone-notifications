#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneNotifications(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:keystone-notifications}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{requires:keystone-notifications}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.available.updated')
        hookenv.atexit(self._clear_updated)

    @hook('{requires:keystone-notifications}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')

    def _clear_updated(self):
        self.remove_state('{relation_name}.available.updated')
