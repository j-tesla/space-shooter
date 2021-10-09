#!/usr/bin/env sh

pipenv install --dev

pipenv run pyinstaller --noconfirm --onefile --clean space-shooter.spec
