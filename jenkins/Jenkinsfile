node {
    stage('Build') {
        checkout scm
        sh 'python3 -m py_compile sources/add2vals.py sources/calc.py sources/web_app.py'
        sh 'pyinstaller --onefile sources/add2vals.py'
        archiveArtifacts 'dist/add2vals'
    }
    stage('Test') {
        try {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        } finally {
            junit 'test-reports/results.xml'
        }
    }
    stage('Manual Approval') {
        input message: 'Lanjutkan ke tahap Deploy?'
    }
    stage('Deploy') {
        sh 'chmod +x ./jenkins/scripts/deploy.sh ./jenkins/scripts/kill.sh'
        sh './jenkins/scripts/deploy.sh'
        sleep 60
        sh './jenkins/scripts/kill.sh'
    }
}
