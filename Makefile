install: .env .venv
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install --upgrade -r requirements.txt
	-@sudo rm /usr/local/bin/say  &> /dev/null || :
	@sudo ln -s "$$(pwd)/say.sh" /usr/local/bin/say

.env:
	@cp .env.example .env

.venv:
	@python3 -m venv .venv

uninstall:
	-@sudo rm /usr/local/bin/say
	-@rm -rf .venv
