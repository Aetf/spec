ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

test: site.yml deps/.dirstamp
	ansible-playbook $< --skip-tags pull

playbook: site.yml deps/.dirstamp
	systemd-inhibit --who="Ansible Playbook" --why="Updating system configuration" ansible-playbook $<

stop:
	systemctl stop ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

start:
	systemctl start ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

status:
	systemctl status ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

log:
	journalctl -f -u ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))


# Ansible playbook depenencies handling
# TODO: Revisit this after ansible 2.10 is released with PR 67843,
# which should enable `ansible-galaxy install -r requirements.yml`
# to install both roles and collections to default path (as configured
# in ansible.cfg?)

deps/roles/.dirstamp: requirements.yml
	ansible-galaxy role install -r $< -f -p deps/roles
	@touch $@

deps/ansible_collections/.dirstamp: requirements.yml
	ansible-galaxy collection install -r $< -p deps
	@touch $@

deps/.dirstamp: deps/roles/.dirstamp deps/ansible_collections/.dirstamp
	@touch $@

.PHONY: playbook stop start status test
