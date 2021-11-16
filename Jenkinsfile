@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfig

pipeline {
    agent any

    stages {
        stage('SQA : plain code checks') {
            steps {
                catchError {
                    script {
                        projectConfig = pipelineConfig()
                        buildStages(projectConfig)
                    }
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('SQA : build checks for S0') {
            when {
                anyOf {
                    branch 'build-S0'
                }
            }
            steps {
                script {
                    projectConfig = pipelineConfig( configFile: '.sqa/config_build-S0.yml')
                    buildStages(projectConfig)
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('SQA : build checks for S1') {
            when {
                anyOf {
                    branch 'build-S1'
                }
            }
            steps {
                script {
                    projectConfig = pipelineConfig( configFile: '.sqa/config_build-S1.yml')
                    buildStages(projectConfig)
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
    }
}
