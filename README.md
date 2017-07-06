cloud-cdn
=========

[![Project Status: Concept - initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

Ansible role to manage Cloud CDN with different providers.

Roadmap for Cloud Providers:
* AWS CloudFront
* Azion Content Delivery

Main roles to manage:
* Facts
* Distributions
* Cache settings
* Origins
* Behaviors


Requirements
------------

* AWS Cloud Front

For instance, if the role uses the EC2 module, boto package is required.

* [Azion](https://www.azion.com.br/developers/api/)

For instance, AWS Python SDK.

> TODO

Role Variables
--------------

> TODO. Could be:

```YAML
cdn_aws_region: <aws region>
cdn_aws_access: <aws access key>
cdn_aws_secret: <aws secret key>

cdn_azion_auth_pass: <base64 token>
cdn_azion_auth_token: <session token>

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

> DEV TODO AZION:

```
Creation order to dev:
- Check CDN is created
-- YES: get ID
--- check each config has in compliance
-- NOT:
--- create new CDN with basic cfg, get ID
--- create origins
--- create cache settings
--- create WAF
--- create rule sets
--- check/change main config with default origins
```



Dependencies
------------

* boto3
* azion-sdk

Example Playbook
----------------

> TODO

License
-------

Apache-2

Author Information
------------------

[Marco Tulio R Braga](https://github.com/mtulio)
