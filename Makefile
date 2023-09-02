install: .venv
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install --upgrade -r requirements.txt
	-@rm /usr/local/bin/say
	@ln -s "$$(pwd)/say.sh" /usr/local/bin/say

.venv:
	@python3 -m venv .venv

uninstall:
	-@rm /usr/local/bin/say
