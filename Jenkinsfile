pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'nitesh789docker/nimap_pyapp'
        DOCKERFILE_PATH = 'dockerized_app/Dockerfile'  // Path to your Dockerfile
        BUILD_CONTEXT = 'dockerized_app'  // Path to the build context
        REGISTRY_CREDENTIALS = credentials('docker_id')
        DOCKER_REGISTRY = 'nitesh789docker'
        DOCKERR_IMAGE = 'nimap_pyapp'
        SERVER_USER = 'ubuntu'  // or 'ubuntu', depending on your EC2 instance
        SERVER_IP = '13.233.71.102'
       
    }

    stages {
        stage('checkout') {
            steps {
               checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/nss55/docker-fastapi-test.git']])
        }
    }
         stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:latest", "-f ${DOCKERFILE_PATH} ${BUILD_CONTEXT}")
                }
            }
        }
           stage('push to hub'){
            steps{
                script{
                    docker.withRegistry('https://index.docker.io/v1/', 'docker_id') {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                }
                        
            }
                        
        }                      
    }
        stage('Deploy to EC2') {
            steps {
                echo 'Deploying application to EC2...'
                sshagent(['ec2-ssh-credentials-id']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} '
                        docker pull ${DOCKER_REGISTRY}/${DOCKERR_IMAGE}:latest
                        docker run -d --name ${DOCKERR_IMAGE} -p 8000:8000 ${DOCKER_REGISTRY}/${DOCKERR_IMAGE}:latest
                        '
                    """
                }
            }
        }


}
}
