pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'mapps_cars.settings'
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE = 'conanraizy/application_mapps_cars'
        EC2_USER = 'ubuntu'
        EC2_HOST = '18.217.31.192'
        DOCKER_CREDS = 'docker-hub-credentials'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py migrate --noinput
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test cars --verbosity=2
                '''
            }
        }

        stage('Collect Static Files') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py collectstatic --noinput || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDS) {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                        echo "Image pushed to Docker Hub"
                    }
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                script {
                    sshagent(credentials: ['ec2-ssh-private-key']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                                docker pull ${DOCKER_IMAGE}:latest
                                docker ps -a -q -f name=django-container | grep -q . && docker stop django-container || true
                                docker ps -a -q -f name=django-container | grep -q . && docker rm django-container || true
                                docker run -d --name django-container -p 80:80 ${DOCKER_IMAGE}:latest
                                sleep 5
                                docker ps -a
                                docker logs django-container || true
                            '
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed.'
        }
        always {
            cleanWs()
        }
    }
}
