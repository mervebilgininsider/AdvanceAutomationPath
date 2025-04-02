pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up test environment...'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running Selenium tests...'
                sh 'python -m pytest tests/ --html=reports/report.html'
            }
        }
    }
    
    post {
        always {
            echo 'Archiving test reports and screenshots...'
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Tests failed! Check the reports for details.'
        }
    }
}