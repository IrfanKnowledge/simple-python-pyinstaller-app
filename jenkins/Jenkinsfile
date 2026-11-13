node {
    stage('Build') {
        checkout scm
        sh 'python3 -m py_compile sources/add2vals.py sources/calc.py'
    }
    stage('Test') {
        try {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        } finally {
            junit 'test-reports/results.xml'
        }
    }
    stage('Deliver') {
        sh 'pyinstaller --onefile sources/add2vals.py'
        archiveArtifacts 'dist/add2vals'
    }
}
