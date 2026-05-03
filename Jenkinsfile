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
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production server...'
                sh '''
                    . venv/bin/activate
                    # Add deployment steps here, e.g.:
                    # ssh user@server "cd /var/www/mapps_cars && git pull && pip install -r requirements.txt && python manage.py migrate && sudo systemctl restart gunicorn"
                    echo "Deploy step — configure for your server."
                '''
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
