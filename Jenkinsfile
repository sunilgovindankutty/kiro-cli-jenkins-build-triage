pipeline {
    agent any

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                    apt-get update && apt-get install -y python3 python3-pip python3-venv
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
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
                echo "# Build Failure Context" > /tmp/kiro-input.md
                echo "## Build Log" >> /tmp/kiro-input.md
                cat test-output.log >> /tmp/kiro-input.md 2>/dev/null || echo "No test output" >> /tmp/kiro-input.md
                echo "## Recent Code Changes" >> /tmp/kiro-input.md
                git diff HEAD~1 >> /tmp/kiro-input.md 2>/dev/null || echo "No diff available" >> /tmp/kiro-input.md

                echo "=== Kiro triage would run here ==="
                cat /tmp/kiro-input.md
            '''
        }
    }
}
