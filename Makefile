ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

test: site.yml deps/.dirstamp
	ansible-playbook $< --skip-tags start_pulling -vvv

diff: site.yml deps/.dirstamp
	env ANSIBLE_DISPLAY_OK_HOSTS=no ANSIBLE_DISPLAY_SKIPPED_HOSTS=no ansible-playbook $< --skip-tags start_pulling --check --diff

playbook: site.yml deps/.dirstamp
	systemd-inhibit \
		--who="Ansible Playbook" \
		--why="Updating system configuration" \
		ansible-playbook $< -vvv

stop:
	systemctl stop ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

start:
	systemctl start ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

status:
	systemctl status ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

disable:
	systemctl disable --now ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))

log:
	journalctl -f -u ansible-playbook-apply@$$(systemd-escape -p $(ROOT_DIR))


# Ansible playbook depenencies handling
# the target path is set in ansible.cfg collections_path and roles_path
deps/.dirstamp: requirements.yml
	ansible-galaxy install -r $<
	@touch $@

.PHONY: playbook stop start status test
