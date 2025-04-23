pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    triggers {
        githubPush()
    }
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        PATH = "/opt/homebrew/bin:/usr/local/bin:$PATH"
        SCREENSHOT_DIR = "${WORKSPACE}/screenshots"
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up test environment...'
                sh '''
                    # Çalışma dizinini kontrol et
                    pwd
                    ls -la
                    
                    # Python'u bul
                    PYTHON_PATH=$(which python3)
                    echo "Python path: $PYTHON_PATH"
                    
                    # Python'u yükle
                    $PYTHON_PATH -m venv venv
                    . venv/bin/activate
                    
                    # pip'i yükselt
                    pip install --upgrade pip
                    
                    # Gereksinimleri yükle
                    pip install -r requirements.txt
                    
                    # Pytest ve gerekli eklentileri yükle
                    pip install pytest pytest-html pytest-selenium
                    
                    # Screenshots ve reports dizinlerini oluştur
                    mkdir -p screenshots
                    mkdir -p reports
                    
                    # Test dizinini kontrol et
                    ls -la tests/
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running Selenium tests...'
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            
                            # Test dizininin varlığını kontrol et
                            if [ ! -d "tests" ]; then
                                echo "ERROR: 'tests' directory not found!"
                                exit 1
                            fi
                            
                            # Dizindeki test dosyalarını listele
                            echo "Test files:"
                            ls -la tests/
                            
                            # Tırnak içinde path kullanarak testleri çalıştır
                            python -m pytest "tests/" \
                                --html="reports/report.html" \
                                --self-contained-html \
                                --capture=tee-sys \
                                --screenshots-dir="${SCREENSHOT_DIR}"
                        '''
                        env.TESTS_PASSED = 'true'
                    } catch (Exception e) {
                        env.TESTS_PASSED = 'false'
                        throw e
                    }
                }
            }
        }
        
        stage('Upload Results') {
            steps {
                echo 'Uploading test results to GitHub...'
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                    sh '''
                        . venv/bin/activate
                        python -c "import requests
import os
import json

# Get PR number from environment
pr_number = os.environ.get('CHANGE_ID')
if not pr_number:
    print('Not a PR build, skipping GitHub status update')
    exit(0)
    
# Set GitHub status
headers = {
    'Authorization': f'token {os.environ[\"GITHUB_TOKEN\"]}',
    'Accept': 'application/vnd.github.v3+json'
}

# Read test results
with open('reports/report.html', 'r') as f:
    report_content = f.read()
    
# Create status check
status = 'success' if 'passed' in report_content else 'failure'
data = {
    'state': status,
    'target_url': f'{os.environ[\"BUILD_URL\"]}',
    'description': 'UI Tests',
    'context': 'UI Tests'
}

# Send status update
response = requests.post(
    f'https://api.github.com/repos/{os.environ[\"GITHUB_REPOSITORY\"]}/statuses/{os.environ[\"GIT_COMMIT\"]}',
    headers=headers,
    data=json.dumps(data)
)
response.raise_for_status()"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Archiving test reports and screenshots...'
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
            
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'All tests passed successfully!'
        }
        unstable {
            echo 'Tests completed with unstable status.'
        }
        failure {
            script {
                if (env.TESTS_PASSED == 'true') {
                    echo 'Tests passed, but pipeline failed at a later stage.'
                } else {
                    echo 'Tests failed! Check the reports for details.'
                }
            }
        }
    }
}