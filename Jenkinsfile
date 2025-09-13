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
        MONGO_URL = "mongodb://admin:password123@localhost:27017/test_metrics?authSource=admin"
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up test environment...'
                sh '''
                    pwd
                    ls -la
                    
                    PYTHON_PATH=$(which python3)
                    echo "Python path: $PYTHON_PATH"
                    
                    $PYTHON_PATH -m venv venv
                    . venv/bin/activate
                    
                    pip install --upgrade pip
                    
                    pip install -r requirements.txt
                    
                    pip install pytest pytest-html pytest-selenium pymongo pytest-json-report
                    
                    mkdir -p screenshots
                    mkdir -p reports
                    
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
                            
                            if [ ! -d "tests" ]; then
                                echo "ERROR: 'tests' directory not found!"
                                exit 1
                            fi
                            
                            echo "Test files:"
                            ls -la tests/
                            
                            python -m pytest "tests/" \
                                --html="reports/report.html" \
                                --self-contained-html \
                                --capture=tee-sys \
                                --screenshots-dir="${SCREENSHOT_DIR}" \
                                --json-report \
                                --json-report-file="reports/test_results.json"
                        '''
                        env.TESTS_PASSED = 'true'
                    } catch (Exception e) {
                        env.TESTS_PASSED = 'false'
                        throw e
                    }
                }
            }
        }
        
        stage('Log Test Results to MongoDB') {
            steps {
                echo 'Logging test results to MongoDB...'
                sh '''
                    . venv/bin/activate
                    
                    python -c "
import json
import os
from helpers.metrics_logger import metrics_logger
from datetime import datetime

try:
    with open('reports/test_results.json', 'r') as f:
        test_data = json.load(f)
    
    for test in test_data.get('tests', []):
        test_name = test.get('nodeid', 'unknown')
        status = 'passed' if test.get('outcome') == 'passed' else 'failed'
        duration = test.get('duration', 0)
        error_message = test.get('call', {}).get('longrepr', '') if status == 'failed' else None
        
        metrics_logger.log_test_result(
            test_name=test_name,
            status=status,
            duration=duration,
            error_message=error_message
        )
    
    summary = {
        'total_tests': test_data.get('summary', {}).get('total', 0),
        'passed': test_data.get('summary', {}).get('passed', 0),
        'failed': test_data.get('summary', {}).get('failed', 0),
        'duration': test_data.get('duration', 0),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    metrics_logger.log_test_metrics(summary)
    print('Test sonuçları MongoDB\'ye kaydedildi')
    
except Exception as e:
    print(f'MongoDB kaydetme hatası: {e}')
    exit(1)
"
                '''
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

pr_number = os.environ.get('CHANGE_ID')
if not pr_number:
    print('Not a PR build, skipping GitHub status update')
    exit(0)
    
headers = {
    'Authorization': f'token {os.environ[\"GITHUB_TOKEN\"]}',
    'Accept': 'application/vnd.github.v3+json'
}

with open('reports/report.html', 'r') as f:
    report_content = f.read()
    
status = 'success' if 'passed' in report_content else 'failure'
data = {
    'state': status,
    'target_url': f'{os.environ[\"BUILD_URL\"]}',
    'description': 'UI Tests',
    'context': 'UI Tests'
}

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
