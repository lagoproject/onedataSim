@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfig

pipeline {
    agent any

    stages {
        stage('SQA baseline dynamic stages : plain code checks') {
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
        stage('SQA baseline dynamic stages: build checks for S0') {
            steps {
                script {
                    projectConfig = pipelineConfig( configFile: '.sqa/config_build_S0.yml')
                    buildStages(projectConfig)
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('SQA baseline dynamic stages: build checks for S1') {
            steps {
                script {
                    projectConfig = pipelineConfig( configFile: '.sqa/config_build_S1.yml')
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
