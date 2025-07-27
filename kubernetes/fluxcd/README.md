# Introduction to Flux CD v2


Установка docker, kind, настройка
```
$ kind create cluster --name=flux-stage
```
2.  Установка flux в кластере. Работаем через контейнер, ставим утилиты, используем docker-in-docker  для сборки образа
```
$ docker run -it --name=bastion --privileged -v ${HOME}:/root/ -v ${PWD}:/work -v /var/run/docker.sock:/var/run/docker.sock  -w /work --net host earthly/dind:alpine  sh
# apk add curl git
# curl -sLO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl; chmod +x kubectl ; mv ./kubectl /bin/
```
3. Делаем в github форк с https://github.com/jora450000/docker-development-youtube-series.git ,  github делаем временный токен на управление репозитарием. Вставляем в переменную среды
```
# export GITHUB_TOKEN="вашг токен"
```
4. Создаем bootstap
```
# flux bootstrap github \
  --token-auth \
  --owner=<ваш репозитарий> \
  --repository=docker-development-youtube-series \
  --path=kubernetes/fluxcd/repositories/infra-repo/clusters/dev-cluster \
  --personal \
  --branch master
```
5.  Проверяем состояние flux, GitRepository, Kustomization, проверяем наличие коммитов от flux в гитхабе
```
# flux check 
# kubectl -n flux-system get GitRepository
# kubectl -n flux-system get Kustomization
# kubectl describe GitRepository
# kubectl describe Kustomization
# git clone https://github.com/jora450000/docker-development-youtube-series.git
# cd docker-development-youtube-series/
# git log6. Настраиваем CD по модели pull. 
# kubectl -n default apply -f repositories/infra-repo/apps/example-app-1/gitrepository.yaml
# kubectl -n default apply -f repositories/infra-repo/apps/example-app-1/kustomization.yaml
# kubectl -n flux-system get GitRepository
# kubectl -n flux-system get Kustomization
# kubectl get deploy
# kubectl get svc
```
7. Тестируем работу приложения через сервис и масштабирование
```
# kubectl run -ti curl --image=alpine/curl -- sh
# while true; do curl example-app-1; sleep 0.2; done
# exit
```
8. Правим приложение. В app.py  - номер версии, пересобираем образ, пушим
```
# docker build . -f dockerfile -t docker.io/<ваш проект докерхаб>/hello-app:1.0.0.<тек+1>
# docker login docker.io -u <ваш логин докерхаб>
# docker push docker.io/ docker.io/<ваш проект докерхаб>/hello-app:1.0.0.<тек+1>
```
9. Правим развертываение
```
# сd ../deploy/; vi deployment.yaml
  меняем тег образа на 1.0.0.<тек + 1> 
```
10. Коммитим изменения в гит
```
#  git commit -am "changed to version 1.0.0.<тек+1>
#  git merge; git push origin master
```
11. Наблюдаем накатку в онлайн
```
# watch kubectl get po
```
12. Проверяем версию
```
# kubectl exec -ti curl -- sh
# while true; do curl example-app-1; sleep 0.2; done
```
13. Смотрим логи flux
```
# kubectl exec -ti curl -- sh
```
 
