cloud-cdn
=========

[![Project Status: Concept - initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

Ansible role to manage Cloud CDN with different providers.

Roadmap for Cloud Providers:
* Azion Content Delivery
* AWS CloudFront

Main roles to manage:
* Facts
* Distributions
* Cache settings
* Origins
* Behaviors


Requirements
------------

* [Azion](https://www.azion.com.br/developers/api/) account

Export your session token into variable `AZION_TOKEN`

```bash
export AZION_TOKEN="$(curl -s -X POST -H \"Accept: application/json; version=1\" \
                -H \"Authorization: Basic $(echo ${AZION_USER}:${AZION_PASS}|base64)\" \
                https://api.azion.net/tokens  |jq .token)
```

* AWS account to use Cloud Front

For instance, if the role uses the EC2 module, boto package is required.

Role Variables
--------------

> Could be [roadmap]:

```YAML
cdn_aws_region: <aws region>
cdn_aws_access: <aws access key>
cdn_aws_secret: <aws secret key>

cdn_azion_auth_token: <session token>
cdn_azion_auth_token_type: session

cdn_distributions:
  - name: example.com-azion
    provider: azion
    origin_address: origin.example.com
    origin_host_header: www.example.com
    cname_access_only: true
    cname:
        - "www.example.com"
    delivery_protocol: "http,https"
    digital_certificate: <ID>
    origin_protocol_policy: "preserve"
    browser_cache_settings: true
    browser_cache_settings_minimum_ttl: 10
    cdn_cache_settings: "override|honor|bypass"
    cdn_cache_settings_minimum_ttl: 30
    origins:
        - name: website
          origin_type: load_balancer
          method: <ip_hash|least_connections|round_robin>
          host_header: <www.myorigin.com>
          origin_protocol_policy: <preserve|http|https>
          adresses:
            - address: origin1.example.com
              weight: 10
              server_role: primary
              is_active: true
            - address: origin2.example.com
              weight: 1
              server_role: backup
              is_active: true
        - name: static
          origin_type: single
          host_header: <static.myorigin.com>
          origin_protocol_policy: <preserve|http|https>
          connection_timeout: <number>
          timeout_between_bytes: <number>
          adresses:
            - address: static.example.com
              server_role: primary
              is_active: true
    cache_settings:
        - name:
          browser_cache_settings: <true|false>
          cdn_cache_settings: <honor|override|override>
          cache_by_query_string: <ignore|whitelist|blacklist|all>
          cache_by_cookies: <ignore|whitelist|blacklist|all>
          browser_cache_settings_maximum_ttl: <number>
          cdn_cache_settings_maximum_ttl: <number>
          query_string_fields: [array]
          enable_query_string_sort: <true|false>
          cookie_names:  [array]
    rules_engine:
        - path: /static:
          regex: <true|false>
          protocol_policy: <http|http,https|redirect_to_https>
          behavior: <delivery|redirect|access_denied|acceleration|image_optimization>
          path_origin_name: <strign> (get name from origins and set path_origin_id)
          redirect_to: ""
          waf_rule_set_name: <strign> (get name from Firewalls and set waf_rule_set_id)
          cache_settings_name: <strign> (get name from cache_settings and set cache_settings_id)

```

Dependencies
------------

* boto3
* azion

Example Playbook
----------------

* Basic - create default template based on SDK sample config

```YAML
- name: Keep CDNs using Azion provider
  hosts: localhost
  connection: local
  become: no

  roles:
    - mtulio-ansible-role-cloud-cdn

  vars:
    cdn_distributions:
      - name: teste-ansible-default
        provider: azion
        state: present
```

* Advanced - sent your own payload

> We are working to validate the support of hashes unless of payload

```YAML
- name: Keep CDNs using Azion provider
  hosts: localhost
  connection: local
  become: no

  roles:
    - mtulio-ansible-role-cloud-cdn

  vars:
    cdn_distributions:
      - name: teste-ansible-default
        provider: azion
        state: present

      - name: teste-ansible
        provider: azion
        state: present
        payload: |
           {
                 "name": "teste-ansible",
                 "origin_address": "domain.teste-ansible.com",
                 "cname_access_only": true,
                 "cname": ["www1.teste-ansible.com"],
                 "delivery_protocol": "http",
                 "cdn_cache_settings": "override",
                 "cdn_cache_settings_minimum_ttl": 2592000,
                 "origin_protocol_policy": "preserve",
                 "origins": [
                           {
                               "name": "origin-default",
                               "origin_type": "single_origin",
                               "host_header": "www..teste-ansible.com",
                               "origin_protocol_policy": "https",
                               "addresses": [
                                   {
                                    "address": "origin-www.teste-ansible.com"
                                   }
                               ],
                               "connection_timeout": 10,
                               "timeout_between_bytes": 30
                           },
                           {
                               "name": "origin-balanced",
                               "origin_type": "load_balancer",
                               "method": "ip_hash",
                               "host_header": "www-lb.teste-ansible.com",
                               "origin_protocol_policy": "preserve",
                               "addresses": [
                                   {
                                    "address": "www-lb1.teste-ansible.com",
                                    "weight": 10,
                                    "server_role": "primary",
                                    "is_active": true
                                   },
                                   {
                                    "address": "origin-lb2.teste-ansible.com",
                                    "weight": 1,
                                    "server_role": "backup",
                                    "is_active": true
                                   }
                               ],
                               "connection_timeout": 10,
                               "timeout_between_bytes": 30
                           },
                           {
                               "name": "origin-static",
                               "origin_type": "single_origin",
                               "host_header": "static..teste-ansible.com",
                               "origin_protocol_policy": "http",
                               "addresses": [
                                   {
                                    "address": "origin-static.teste-ansible.com"
                                   }
                               ],
                               "connection_timeout": 10,
                               "timeout_between_bytes": 20
                           },
                           {
                               "name": "origin-proxy",
                               "origin_type": "single_origin",
                               "host_header": "proxy.teste-ansible.com",
                               "origin_protocol_policy": "preserve",
                               "addresses": [
                                   {
                                    "address": "origin-proxy.teste-ansible.com"
                                   }
                               ],
                               "connection_timeout": 10,
                               "timeout_between_bytes": 20
                           }
                       ],
                 "cache_settings": [
                     {
                       "name": "cache-1-hour-ignore-qs-cookies",
                       "browser_cache_settings": false,
                       "cdn_cache_settings": "override",
                       "cdn_cache_settings_maximum_ttl": 3600,
                       "cache_by_query_string": "ignore",
                       "enable_query_string_sort": false,
                       "cache_by_cookies": "ignore"
                     },
                     {
                       "name": "cache-bypass",
                       "browser_cache_settings": false,
                       "cdn_cache_settings": "bypass",
                       "cache_by_query_string": "ignore",
                       "cache_by_cookies": "ignore"
                     }
                   ],
                 "rules_engine": [
                       {
                         "path": "/images/",
                         "regex": false,
                         "protocol_policy": "http,https",
                         "gzip": false,
                         "behavior": "delivery",
                         "path_origin_name": "origin-static",
                         "cache_settings_name": "cache-1-hour-ignore-qs-cookies"
                       },
                       {
                         "path": "/proxy",
                         "regex": false,
                         "protocol_policy": "http",
                         "gzip": false,
                         "behavior": "acceleration",
                         "path_origin_name": "origin-proxy",
                         "cache_settings_name": "cache-bypass",
                         "forward_cookies": "all"
                       }
                 ]
           }

```
License
-------

Apache-2

Author Information
------------------

[Marco Tulio R Braga](https://github.com/mtulio)
