pipeline {
    agent any

    environment {
        KIRO_API_KEY = credentials('kiro-api-key')
    }

    stages {
        stage('Install Python Deps') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''#!/bin/bash
                    set -o pipefail
                    . venv/bin/activate
                    pytest test_tools.py -v --tb=long 2>&1 | tee test-output.log
                '''
            }
        }
    }

    post {
        failure {
            withCredentials([string(credentialsId: 'github-token', variable: 'GH_TOKEN')]) {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    git diff HEAD~1 > /tmp/diff.txt 2>/dev/null || true

                    git checkout -b fix/kiro-auto-fix-${BUILD_NUMBER}

                    kiro-cli chat --no-interactive --trust-tools=read,grep,write \
                      "The build failed. Read test-output.log and /tmp/diff.txt. Fix the bug by editing the source files directly. Do not ask for confirmation, just apply the fix."

                    if [ -n "$(git diff)" ]; then
                        git config user.email "kiro-bot@demo.local"
                        git config user.name "Kiro Bot"
                        git add -A
                        git commit -m "fix: auto-fix from Kiro build triage (build #${BUILD_NUMBER})"
                        REPO_URL=$(git config --get remote.origin.url | sed "s|https://|https://${GH_TOKEN}@|")
                        git push ${REPO_URL} fix/kiro-auto-fix-${BUILD_NUMBER}
                    fi
                '''
            }
        }
    }
}
