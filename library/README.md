# library

Custom library to be used in modules


## AZION api

```
ansible-playbook tests/test.yml  -vvv
```

## Testing the module

* [Install it](http://docs.ansible.com/ansible/dev_guide/developing_modules_general.html#testing-your-module)

* Get ansible hacking script and test module:

> Since the dependencies of module aren't an public module, yet, we can export
> the module path.

```
SCRIPT_PATH=https://raw.githubusercontent.com/ansible/ansible/devel/hacking/test-module
wget $SCRIPT_PATH -O tests/test-module
export PYTHONPATH=${PYTHONPATH}:${PWD}/library/azion;
```

* Query by ID:

`python ./tests/test-module -m ./library/azion_cdn_facts.py -a 'name=test-ansible'`

* Query by name:

`python ./tests/test-module -m ./library/azion_cdn_facts.py -a 'id=1486490960'`
