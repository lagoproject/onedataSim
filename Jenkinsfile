@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfigPlain
def projectConfigS0
def projectConfigS1


pipeline {
    agent any

    stages {
        stage('SQA : plain code checks') {
            steps {
                catchError {
                    script {
                        projectConfig = pipelineConfig(configFile: '.sqa/config.yml')
                        buildStages(projectConfigPlain)
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
                    projectConfig = pipelineConfig(configFile: '.sqa/config_build_S0.yml')
                    buildStages(projectConfigS0)
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
                    projectConfig = pipelineConfig(configFile: '.sqa/config_build_S1.yml')
                    buildStages(projectConfigS1)
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
