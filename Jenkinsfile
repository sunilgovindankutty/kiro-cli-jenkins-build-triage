pipeline {
    agent any

    environment {
        ECR_REPO   = 'strands-weather-agent'
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest test_tools.py -v --tb=long 2>&1 | tee test-output.log'
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${ECR_REPO}:${BUILD_NUMBER} ."
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin \
                    \${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    docker tag ${ECR_REPO}:${BUILD_NUMBER} \
                    \${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${BUILD_NUMBER}

                    docker push \
                    \${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${BUILD_NUMBER}
                """
            }
        }
    }

    post {
        failure {
            sh '''
                echo "# Build Failure Context" > /tmp/kiro-input.md
                echo "## Build Log (last 100 lines)" >> /tmp/kiro-input.md
                tail -100 test-output.log >> /tmp/kiro-input.md 2>/dev/null
                echo "## Recent Code Changes" >> /tmp/kiro-input.md
                git diff HEAD~1 >> /tmp/kiro-input.md 2>/dev/null

                kiro-cli chat --headless \
                  --prompt "Analyze this build failure. Identify the root cause, map it to the code change, and suggest a fix. Be concise." \
                  --input /tmp/kiro-input.md \
                  --output /tmp/kiro-triage.md
            '''
            // Post triage to Slack or as PR comment
            echo "=== Kiro Build Triage ==="
            sh 'cat /tmp/kiro-triage.md'
        }
    }
}
