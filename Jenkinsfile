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
        SCREENSHOT_DIR = "${WORKSPACE}/screenshots"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up test environment...'
                sh '''
                    echo "Detecting OS..."
                    UNAME=$(uname)
                    echo "Running on: $UNAME"

                    if [ "$UNAME" = "Darwin" ]; then
                        export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
                    fi

                    if [ "$UNAME" = "Linux" ]; then
                        echo "Checking Python..."
                        which python3 || (echo "Missing python3" && exit 1)
                        
                        echo "Starting virtual display for Linux..."
                        which Xvfb || (sudo apt-get update && sudo apt-get install -y xvfb)
                        Xvfb :99 -ac &
                        export DISPLAY=:99
                    fi

                    PYTHON_PATH=$(which python3)
                    echo "Python path: $PYTHON_PATH"

                    $PYTHON_PATH -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-html pytest-selenium

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
