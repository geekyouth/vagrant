# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.8 (default, Nov 16 2020, 16:55:22) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: /__init__.py
# Compiled at: 2020-09-28 19:57:08
# Size of source mod 2**32: 15610 bytes
MAX_INSTANCES = 9999999
try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    ImproperlyConfigured = Exception

try:
    from django.utils.encoding import smart_bytes
except ImportError:
    smart_bytes = lambda x: str(x).encode()

try:
    from awx.main.models import Host
except (ImportError, ImproperlyConfigured):
    Host = None

try:
    from django.conf import settings
except (ImportError, ImproperlyConfigured):
    settings = None

from datetime import datetime, timedelta
import os, collections, copy, hashlib, time, logging, subprocess, re
logger = logging.getLogger(__name__)

class TowerLicense(object):
    ENHANCEMENT_TIMEOUT = 2592000
    ENHANCEMENT_TYPES = {'basic':{'features':{'activity_streams':False, 
       'ha':False, 
       'ldap':False, 
       'multiple_organizations':False, 
       'surveys':False, 
       'system_tracking':False, 
       'rebranding':False, 
       'enterprise_auth':False, 
       'workflows':False}, 
      'license_name':'Basic'}, 
     'enterprise':{'features':{'activity_streams':True, 
       'ha':True, 
       'ldap':True, 
       'multiple_organizations':True, 
       'surveys':True, 
       'system_tracking':True, 
       'rebranding':True, 
       'enterprise_auth':True, 
       'workflows':True}, 
      'license_name':'Enterprise'}, 
     'legacy':{'features':{'activity_streams':True, 
       'ha':True, 
       'ldap':True, 
       'multiple_organizations':True, 
       'surveys':True, 
       'system_tracking':False, 
       'rebranding':False, 
       'enterprise_auth':False, 
       'workflows':False}, 
      'license_name':'Legacy'}}

    def __init__(self, **kwargs):
        self._attrs = dict(company_name='',
          instance_count=0,
          license_date=0,
          license_key='UNLICENSED')
        if not kwargs:
            kwargs = getattr(settings, 'LICENSE', None) or {}
        self._attrs.update(kwargs)
        self._attrs['license_date'] = int(self._attrs['license_date'])
        if not self._attrs.get('subscription_name', None):
            self._attrs['subscription_name'] = self._generate_subscription_name()
        if self._check_cloudforms_subscription():
            self._generate_cloudforms_subscription()

    def _generate_cloudforms_subscription(self):
        self._attrs.update(dict(company_name='Red Hat CloudForms License', instance_count=MAX_INSTANCES,
          license_date=253370764800,
          license_key='xxxx',
          license_type='enterprise',
          subscription_name='Red Hat CloudForms License'))

    def _check_cloudforms_subscription(self):
        return True
        if os.path.exists('/var/lib/awx/i18n.db'):
            return True
        else:
            if os.path.isdir('/opt/rh/cfme-appliance'):
                if os.path.isdir('/opt/rh/cfme-gemset'):
                    try:
                        has_rpms = subprocess.call(['rpm', '--quiet', '-q', 'cfme', 'cfme-appliance', 'cfme-gemset'])
                        if has_rpms == 0:
                            return True
                    except OSError:
                        pass

            return False

    def _generate_subscription_name(self):
        name_parts = ['Ansible Tower by Red Hat', ' (%d Managed Nodes)' % int(self._attrs['instance_count'])]
        license_type = self._attrs.get('license_type', 'legacy')
        if license_type == 'legacy':
            name_parts.insert(1, ', Legacy')
        else:
            if license_type == 'basic':
                name_parts.insert(1, ', Self-Support')
            else:
                if license_type == 'enterprise':
                    name_parts.insert(1, ', Standard')
        if self._attrs.get('trial', False):
            name_parts.append(' Trial')
        return ''.join(name_parts)

    def _generate_key(self):
        sha = hashlib.sha256()
        sha.update(smart_bytes('ansibleworks.license.000'))
        sha.update(smart_bytes(self._attrs['company_name']))
        sha.update(smart_bytes(self._attrs['instance_count']))
        sha.update(smart_bytes(self._attrs['license_date']))
        license_type = self._attrs.get('license_type', 'legacy')
        if license_type != 'legacy':
            sha.update(smart_bytes('{license_type:%s}' % self._attrs['license_type']))
        if self._attrs.get('trial', False):
            sha.update(smart_bytes(self._attrs['trial']))
        default_features = self.ENHANCEMENT_TYPES[license_type]['features']
        features = self._attrs.get('features', {})
        for feature in sorted(default_features.keys()):
            if feature not in features:
                pass
            else:
                if features[feature] == default_features[feature]:
                    pass
                else:
                    feature_str = smart_bytes('{%s:%r}' % (feature, features[feature]))
                    sha.update(feature_str)

        return sha.hexdigest()

    def update(self, **kwargs):
        if 'instance_count' in kwargs:
            kwargs['instance_count'] = int(kwargs['instance_count'])
        if 'license_date' in kwargs:
            kwargs['license_date'] = int(kwargs['license_date'])
        self._attrs.update(kwargs)

    def generate(self):
        key = self._attrs.get('license_key', 'UNLICENSED')
        if key == 'UNLICENSED':
            self.update(license_key=(self._generate_key()))
        return copy.deepcopy(self._attrs)

    def validate_rh(self, user, pw):
        host = getattr(settings, 'REDHAT_CANDLEPIN_HOST', None)
        if not user:
            raise ValueError('rh_username is required')
        if not pw:
            raise ValueError('rh_password is required')
        if host and user and pw:
            import requests
            verify = getattr(settings, 'REDHAT_CANDLEPIN_VERIFY', False)
            json = []
            try:
                subs = requests.get(('/'.join([host, 'subscription/users/{}/owners'.format(user)])),
                  verify=verify,
                  auth=(
                 user, pw))
            except requests.exceptions.ConnectionError as error:
                raise error
            except OSError as error:
                raise OSError('Unable to open certificate bundle {}. Check that Ansible Tower is running on Red Hat Enterprise Linux.'.format(verify)) from error

            subs.raise_for_status()
            for sub in subs.json():
                resp = requests.get(('/'.join([
                 host,
                 'subscription/owners/{}/pools/?match=*tower*'.format(sub['key'])])),
                  verify=verify,
                  auth=(
                 user, pw))
                resp.raise_for_status()
                json.extend(resp.json())

            return self.generate_license_options_from_entitlements(json)
        else:
            return []

    def is_appropriate_sub(self, sub):
        if sub['activeSubscription'] is False:
            return False
        else:
            products = sub.get('providedProducts', [])
            if any(map(lambda product: product.get('productId', None) == '480', products)):
                return True
            attributes = sub.get('productAttributes', [])
            if any(map(lambda attr: attr.get('name') == 'ph_product_name' and attr.get('value').startswith('Ansible Tower'), attributes)):
                return True
            return False

    def generate_license_options_from_entitlements(self, json):
        from dateutil.parser import parse
        ValidSub = collections.namedtuple('ValidSub', 'sku name end_date trial quantity')
        valid_subs = collections.OrderedDict()
        for sub in json:
            if self.is_appropriate_sub(sub):
                try:
                    end_date = parse(sub.get('endDate'))
                except Exception:
                    continue

                now = datetime.utcnow()
                now = now.replace(tzinfo=(end_date.tzinfo))
                if end_date < now:
                    pass
                else:
                    try:
                        quantity = int(sub['quantity'])
                        if quantity == -1:
                            quantity = MAX_INSTANCES
                    except Exception:
                        continue

                    sku = sub['productId']
                    trial = sku.startswith('S')
                    support_level = ''
                    for attr in sub.get('productAttributes', []):
                        if attr.get('name') == 'support_level':
                            support_level = attr.get('value')

                    sub_key = (
                     end_date.date(), support_level)
                    valid_subs.setdefault(sub_key, []).append(ValidSub(sku, sub['productName'], end_date, trial, quantity))

        if valid_subs:
            licenses = []
            for key, subs in valid_subs.items():
                license = self.__class__(subscription_name='Ansible Tower by Red Hat')
                for sub in subs:
                    license._attrs['instance_count'] += sub.quantity
                    license._attrs['license_type'] = 'enterprise'
                    if sub.trial:
                        license._attrs['trial'] = True

                license._attrs['instance_count'] = min(MAX_INSTANCES, license._attrs['instance_count'])
                human_instances = license._attrs['instance_count']
                if human_instances == MAX_INSTANCES:
                    human_instances = 'Unlimited'
                subscription_name = re.sub(' \\([\\d]+ Managed Nodes', ' ({} Managed Nodes'.format(human_instances), sub.name)
                license._attrs['subscription_name'] = subscription_name
                license.update(license_date=(sub.end_date.strftime('%s')))
                license._attrs['license_key'] = license._generate_key()
                licenses.append(license._attrs.copy())

            return licenses
        raise ValueError('No valid Red Hat Ansible Automation subscription could be found for this account.')

    def validate(self):
        attrs = copy.deepcopy(self._attrs)
        key = attrs.get('license_key', 'UNLICENSED')
        if not self._check_cloudforms_subscription() and (key == 'UNLICENSED' or key != self._generate_key()):
            attrs.update(dict(valid_key=False, compliant=False))
            return attrs
        else:
            attrs['valid_key'] = True
            attrs['deployment_id'] = hashlib.sha1(smart_bytes(key)).hexdigest()
            if Host:
                current_instances = Host.objects.active_count()
            else:
                current_instances = 0
            available_instances = int(attrs.get('instance_count', None) or 0)
            attrs['current_instances'] = current_instances
            attrs['available_instances'] = available_instances
            attrs['free_instances'] = available_instances - current_instances
            license_date = int(attrs.get('license_date', None) or 0)
            current_date = int(time.time())
            time_remaining = license_date - current_date
            attrs['time_remaining'] = time_remaining
            if attrs.setdefault('trial', False):
                attrs['grace_period_remaining'] = time_remaining
            else:
                attrs['grace_period_remaining'] = license_date + 2592000 - current_date
            attrs['compliant'] = bool(time_remaining > 0 and attrs['free_instances'] >= 0)
            attrs['date_warning'] = bool(time_remaining < self.ENHANCEMENT_TIMEOUT)
            attrs['date_expired'] = bool(time_remaining <= 0)
            attrs.setdefault('license_type', 'legacy')
            attrs['features'] = dict(
             (self.ENHANCEMENT_TYPES[attrs['license_type']]['features']), **attrs.get('features', None) or {})
            return attrs
# okay decompiling __init__.pyc
