#!/usr/bin/env bash

EXEC_WEB="docker compose exec web "
EXEC_NPM="docker compose run npm "

if [ $# -gt 0 ];then
    if [ "$1" == "manage" ]; then
        shift 1
        $EXEC_WEB python3 manage.py "$@"
        
    elif [ "$1" == "pip" ]; then
        shift 1
        $EXEC_WEB pip "$@"
        
    elif [ "$1" == "npm" ]; then
        shift 1
        $EXEC_NPM npm "$@"
        
    elif [ "$1" == "npx" ]; then
        shift 1
        $EXEC_NPM npx "$@"

    elif [ "$1" == "dev" ]; then
        $EXEC_NPM npm install
        docker compose run --rm -p 5173:5173 npm npm run dev

    elif [ "$1" == "build" ]; then
        $EXEC_NPM npm install 
        docker compose run --rm -e mode=production npm npm run build

    elif [ "$1" == "expose" ]; then
        docker compose run --rm expose

    else
        $EXEC_WEB "$@"
    fi
fi