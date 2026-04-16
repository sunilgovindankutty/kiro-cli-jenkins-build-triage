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

        stage('Install Kiro CLI') {
            steps {
                sh 'curl -fsSL https://cli.kiro.dev/install | bash'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_tools.py -v --tb=long 2>&1 | tee test-output.log
                '''
            }
        }
    }

    post {
        failure {
            sh '''
                export PATH="$HOME/.local/bin:$PATH"
                git diff HEAD~1 > /tmp/diff.txt 2>/dev/null || true
                kiro-cli chat --no-interactive --trust-tools=read,grep \
                  "The build failed. Here is the test output from test-output.log and the code diff in /tmp/diff.txt. Analyze the failure, identify the root cause, map it to the code change, and suggest a fix."
            '''
        }
    }
}
