<h1 align="center">Рекомендательная система новостей</h1>

Данный проект создан для хакатона [**MORE.Tech VTB 2022**](https://moretech.vtb.ru/)  (второе место в треке Data Science по результатам супер-финанла)

Данный WEB-API сервис позволяет получать тренды и инсайты, на основе опубликованных новостей в популярных бизнес источниках (РБК, CFO, Klerk.ru, Consultant)

Формировать дайджесты для клиентов банка ВТБ, в зависимости от их профиля, т.е. профессии клиента 

## Команда разработчиков:

   [Шестаков Михаил](https://github.com/misha1sh)
  
   [Леднев Тимофей](https://github.com/tlmon)
  
   [Пашенцев Егор](https://github.com/eapashentsev)
  
   [Ковалева Вероника](https://github.com/lverafail)
  
   [Лысенко Всеволод](https://gitlab.com/seva.lysenko19)
  
---
## How to launch

Для запуска понадобится Python3.

В корне проекта находится два файла:

- **parser.sh**
 
- **run.sh**

При запуске также будут установлены необходимые зависимости для Python
 
### parser.sh
---
parser.sh при запуске обновляет данные статей в папке ./data

Необходимо использовать следующую команду:

     bash ./parser.sh

#### Warning!

**Обновление данных статей может занимать от 10 до 30 минут, поэтому в папке data уже есть статьи актуальные на 8.10.2022**



### run.sh
---
run.sh запускает Flask-сервер на порте 8080

После запуска run.sh можно пользоваться методами REST API, описанными в документации ниже

Необходимо использовать следующую команду:

     bash ./run.sh

---


## Documentation for WEB-API

WEB-API сервис состоит из 4-ех API-методов

Данные запросы возвращают все результаты в формате json

Ниже приведены описания каждого API-метода и детальное описание json файлов


**1. localhost:8080/api/v0/digest/accounter**

Данный метод API формирует три дайджеста для профиля "Бухгалтер"

output:

- **url** `[string]`
  - Ссылка на статью, использованную для дайджеста
- **publication_date** `[date YYYY-MM-DD]`
  - Дата публикации статьи новостным источником
- **title** `string`
  - Заголовок дайджеста
- **description** `string`
  - Краткое описание новости
  
Итоговый дайджест будет реализован в следующем формате:
- **digest** `[object]`
  ```python
    digest: {
         url: 'string', 
         publication_date: 'MMMM D, YYYY', 
         title: 'string'
         description: 'string' 
    }

**2. localhost:8080/api/v0/digest/ceo**

Данный метод API формирует три дайджеста для профиля "Генеральный директор"

output:

- **url** `[string]`
  - Ссылка на статью, использованную для дайджеста
- **publication_date** `[date YYYY-MM-DD]`
  - Дата публикации статьи новостным источником
- **title** `string`
  - Заголовок дайджеста
- **description** `string`
  - Краткое описание новости
  
Итоговый дайджест будет реализован в следующем формате:
- **digest** `[object]`
  ```python
    digest: {
         url: 'string', 
         publication_date: 'MMMM D, YYYY', 
         title: 'string'
         description: 'string' 
    }


**3. localhost:8080/api/v0/trends**

Данный метод API формирует общие тренды для каждого из профилей:


output:

- **trends** `[array]`
  - Массив с трендами в виде json
  ```python
  days_array: [{ trend: string }, { trend: string }, { trend: string }, { trend: string }];
  ```


**4. localhost:8080/api/v0/insights**

Данный метод API формирует общие инсайты для каждого из профилей:

output:

- **insights** `[array]`
  - Массив с трендами в виде json
  ```python
  days_array: [{ insights: string }, { insights: string }, { insights: string }, { insights: string }];
  ```
