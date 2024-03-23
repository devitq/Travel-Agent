#!/bin/bash

GREEN='\033[1;32m'
NC='\033[0m'

sort-requirements requirements/dev.txt
sort-requirements requirements/prod.txt
sort-requirements requirements/test.txt
sort-requirements requirements/lint.txt
printf "${GREEN}Requirements sorted${NC}\n"

black .
flake8 .
mypy .
printf "${GREEN}Linters runned${NC}\n"

# alembic -c app/alembic.ini upgrade head
printf "${GREEN}Tests runned${NC}\n"
