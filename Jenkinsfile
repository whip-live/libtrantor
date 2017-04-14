node {
    stage('Init workspace') {
        step([$class: 'WsCleanup'])
    }

    stage('Checkout') {
        checkout scm
    }

    stage('Testing') {
        try {
            // Generate a random working directory for tox. This solves
            // a race condition when multiple jobs runs and tox tries to
            // create the same environment on the same workdir.
            randomwd = sh (
                script: "cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1",
                returnStdout: true
            ).trim()

            withEnv(["RANDOM_WD=${randomwd}"]) {
                sh "/opt/bin/docker-compose -f .jenkins.yml run --rm tests"
            }
        } finally {
            sh '/opt/bin/docker-compose -f .jenkins.yml down'
        }
    }

    stage('Clean workspace') {
        step([$class: 'WsCleanup'])
    }
}
