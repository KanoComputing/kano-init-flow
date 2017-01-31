#!/usr/bin/env groovy

@Library('kanolib')
import build_deb_pkg


stage ('Build') {
    build_deb_pkg 'kano-init-flow', env.BRANCH_NAME, 'scratch'
}
