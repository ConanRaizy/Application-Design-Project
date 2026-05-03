pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'mapps_cars.settings'
        PYTHONUNBUFFERED = '1'
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

       stage('Deploy') {
    steps {
        sshagent(credentials: ['ec2-ssh-private-key']) {
            sh """
                ssh -o StrictHostKeyChecking=no ubuntu@18.217.31.192 '
                    set -e
                    cd /home/ubuntu/pythonprojects/Application-Design-Project
                    git pull origin main
                    source venv/bin/activate
                    pip install -r requirements.txt --quiet
                    python manage.py migrate --noinput
                    fuser -k 8000/tcp || true
                    sleep 1
                    nohup bash -c "source /home/ubuntu/pythonprojects/Application-Design-Project/venv/bin/activate && python manage.py runserver 0.0.0.0:8000" > /tmp/django.log 2>&1 &
                    echo "Mapps Cars deployed!"
                '
            """
        }
    }
}

    post {
        success {
            echo 'Pipeline passed. Mapps Cars is good to go!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
        always {
            cleanWs()
        }
    }
}
