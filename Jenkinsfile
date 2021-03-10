pipeline {
    agent none
    stages {

        stage('Main') {
            agent {
                docker {
                    label 'suzhuji'
                    image 'perfdog'
                    args  '-v /var/jenkins_home:/var/jenkins_home'
                }
            }
            steps {
                sh 'python3 -u  /var/jenkins_home/AutoPerfDog/Main.py $TestAPKName'
            }
        }

}
}
