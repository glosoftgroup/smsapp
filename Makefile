env=development
process=all
group=all

ANSIBLE = ansible $(group) -i devops/ansible_devops/inventory/$(env)
ANSIBLE_PLAYBOOK = ansible-playbook -i devops/ansible_devops/inventory/$(env)

# Match any playbook in the devops directory
% :: devops/ansible_devops/%.yml
	$(ANSIBLE_PLAYBOOK) $< -l $(group)
ifdef tags
	$(ANSIBLE_PLAYBOOK) $< -l $(group) -t $(tags)
else ifdef commit
	$(ANSIBLE_PLAYBOOK) $< -l $(group) -e 'APP_VERSION=$(commit)'
else ifdef limit
	$(ANSIBLE_PLAYBOOK) $< -l $(group) --limit $(limit)
else ifdef config
    % :: devops/eb_devops/%.yml
	$(ANSIBLE_PLAYBOOK) $< -l $(group) -e 'EB_CONFIG=$(config) SETTINGS=$(settings)'
else ifdef settings
    % :: devops/eb_devops/%.yml
	$(ANSIBLE_PLAYBOOK) $< -l $(group) -e 'EB_CONFIG=$(config) SETTINGS=$(settings)'
else
	$(ANSIBLE_PLAYBOOK) $< -l $(group)
endif

staging :
	$(eval env = staging )
	$(ANSIBLE_PLAYBOOK) devops/ansible_devops/deploy.yml

status :
	$(ANSIBLE) -s -a "supervisorctl status"


restart start stop :
	$(ANSIBLE) -s -a "supervisorctl $(@) $(process)"

restart-supervisor :
	ansible app_servers -i devops/ansible_devops/inventory/$(env) -m shell -s \
	-a "service supervisor stop && sleep 5 && service supervisor start"

help:
	@echo ''
	@echo 'Usage: '
	@echo ' make <command> [option=<option_value>]...'
	@echo ''
	@echo 'Setup & Deployment:'
	@echo ' make configure		Prepare servers'
	@echo ' make deploy 		Deploy app'
	@echo ''
	@echo 'Options:  '
	@echo ' env			Inventory file (Default: development)'
	@echo ' group			Inventory subgroup (Default: all)'
	@echo ''
	@echo 'Example:'
	@echo ' make configure env=staging group=app_servers'
	@echo ''
	@echo 'Application Management:'
	@echo ' make status 		Display process states'
	@echo ' make start		Start processes'
	@echo ' make restart		Restart processes'
	@echo ' make restart-supervisor	Restart supervisord'
	@echo 'Options: '
	@echo ' process		A supervisor program name or group (Default: all)'
	@echo ''
	@echo 'EB Management'
	@echo ''
	@echo 'Please note to be able to use this commands you need to be in VPN'
	@echo 'and your ssh-key should be added to the eb instances'
	@echo ''
	@echo 'eb_create_env	Creates a eb environment for hermes status. '
	@echo '		[config=staging|production] [settings=staging|production]'
	@echo '		e.g. make eb_create_env config=staging settings=staging'
	@echo 'eb_deploy	Deploys hermes status to the eb. '
	@echo '		[config=staging|production] [settings=staging|production]'
	@echo '		e.g make eb_deploy config=staging settings=staging'


shell:
	@python manage.py shell_plus --settings=configuration.settings.development


# use sqlite for tests, its faster.
test:
	ansible app_servers -i devops/ansible_devops/inventory/$(env) -m shell -a \
	". ~/.virtualenvs/smsapp/bin/activate && \
	cd /vagrant && \
	python manage.py test --settings=configuration.settings.test --noinput"
flush:
	@python manage.py flush --no-initial-data --settings=configuration.settings.development

#ssh:
#	@ssh -o ServerAliveInterval=20 root@41.242.2.68

run2:
	@sudo killall -9 supervisord &
	@sudo killall -9 gunicorn &
	@python manage.py check --settings=configuration.settings.development &
	@python manage.py collectstatic --noinput --settings=configuration.settings.development  &
	@python manage.py migrate smsapp --settings=configuration.settings.development --verbosity 3
	@python manage.py runserver 0.0.0.0:3000 --settings=configuration.settings.development

mk:
	@python manage.py makemigrations --settings=configuration.settings.development core

migrate:
	@python manage.py migrate --settings=configuration.settings.development