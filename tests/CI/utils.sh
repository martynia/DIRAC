#!/usr/bin/env bash
#...............................................................................
#
#   Copies local source and test code to docker containers, if they are
#       directories.
#   Requires $CLIENTCONFIG and $SERVERCONFIG to be defined.
#
#...............................................................................
function copyLocalSource() {
  CONTAINER_NAME=$1
  CONFIG_PATH=$2

  # shellcheck source=tests/CI/CONFIG
  source "$CONFIG_PATH"
  if [ -n "$TESTREPO" ] && [ -d "$TESTREPO" ]; then
    docker exec "${CONTAINER_NAME}" mkdir -p "$WORKSPACE/LocalRepo/TestCode"
    docker cp "$TESTREPO" "${CONTAINER_NAME}:$WORKSPACE/LocalRepo/TestCode"

    sed -i "s@\(export TESTREPO=\).*@\1${WORKSPACE}/LocalRepo/TestCode/$(basename "$TESTREPO")@" "$CONFIG_PATH"
  fi
  if [ -n "$ALTERNATIVE_MODULES" ] && [ -d "$ALTERNATIVE_MODULES" ]; then
    docker exec "${CONTAINER_NAME}" mkdir -p "$WORKSPACE/LocalRepo/ALTERNATIVE_MODULES"
    docker cp "$ALTERNATIVE_MODULES" "${CONTAINER_NAME}:$WORKSPACE/LocalRepo/ALTERNATIVE_MODULES"

    sed -i "s@\(export ALTERNATIVE_MODULES=\).*@\1${WORKSPACE}/LocalRepo/ALTERNATIVE_MODULES/$(basename "$ALTERNATIVE_MODULES")@" "$CONFIG_PATH"
  fi
}

#...............................................................................
#
# getLogs:
#
#   getLogs is an utility function that moves logs from spawned docker containers
#   to the $PWD
#
#...............................................................................
function getLogs() {
    docker cp server:/home/dirac/serverTestOutputs.txt ./log_server_tests.txt
    docker cp client:/home/dirac/clientTestOutputs.txt ./log_client_tests.txt
}
