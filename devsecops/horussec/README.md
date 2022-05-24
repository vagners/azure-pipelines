# Horusec

## O que é o Horusec?
O Horusec é uma ferramenta open source que orquestra outras ferramentas de segurança e identifica falhas de segurança ou vulnerabilidades em projetos, centralizando todos os resultados em um banco de dados para análise e geração de métricas.

## Como o Horusec funciona? 
O Horusec faz uma análise SAST do seu projeto a partir da observação de padrões no código.

## Por que usar o Horusec?[](https://docs.horusec.io/docs/pt-br/overview/#por-que-usar-o-horusec)

- **Promove a cultura do desenvolvimento seguro aplicando a lógica de “security by design”**

Ele traz para você segurança, garantindo que possíveis vulnerabilidades desconhecidas serão encontradas pela análise do Horusec.

- **Melhora a sua experiência**

Garante a segurança dos projetos no processo de CI e CD e, assim, reduz os custos de correção de uma vulnerabilidade.

Mais informações:
[https://docs.horusec.io/docs/pt-br/overview/](https://docs.horusec.io/docs/pt-br/overview/)


---


## Configurando Horus Scan Job
![config](./imgs/config_new.png)

## Exemplo Report
![report](./imgs/report.png)

### Exemplo:

```jsx
pool:
  name: Azure Pipelines
steps:
- script: |
   curl -o HorusecScanSimpleTask.py https://raw.githubusercontent.com/vagners/azure-pipelines/master/devsecops/horussec/HorusecScanSimpleTask.py
   
  displayName: 'Download Horus task'

- task: UsePythonVersion@0
  displayName: 'Use Python 3.x'

- task: PythonScript@0
  displayName: 'Run a Python script'
  inputs:
    scriptPath: HorusecScanSimpleTask.py
    arguments: '-p . -o "horusec-junit.xml"'

- task: PublishTestResults@2
  displayName: 'Publish Test Results *junit.xml'
  inputs:
    testResultsFiles: '*junit.xml'
    mergeTestResults: true
    testRunTitle: 'Horusec Scan'
```