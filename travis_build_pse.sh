#!/bin/bash
# Get last child project build number
BUILD_NUM=$(curl -s 'https://api.travis-ci.org/repos/ITCase/pyramid_sacrud_example/builds' | grep -o '^\[{"id":[0-9]*,' | grep -o '[0-9]' | tr -d '\n')
# Restart last child project build
echo BUILD_NUM
echo $(curl -X POST https://api.travis-ci.org/builds/$BUILD_NUM/restart --header "Authorization: token "$AUTH_TOKEN)
