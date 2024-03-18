# CityGuide

**CityGuide** - это голосовой помощник на основе ИИ для города, который был разработан с целью помогать горожанам и туристам, отвечать на их вопросы, рассказывать про историю города, а также про мероприятия и достопримечательности, которые стоит посетить.

# Описание

Голосовой ассистент **CityGuide** был разработан в рамках кейса по разработке интерактивного голосового помощника с использованием анимированного аватара в рамках хакатона Городские Легенды 2024. **CityGuide** способен выполнять множество функций, например:

*  Подсказать маршрут от точки А до точки Б по городу
*  Рассказать про историю и культуру города
*  Подсказать информацию по поводу транспорта внутри города
*  Отвечать на вопросы, не связанные напрямую с городом (в режиме диалога)
*  Говорить на английском языке и помогать не только горожанам, но и туристам
*  При необходимости снабжать свой ответ субтитрами для людей с проблемами со слухом


Также подробности можно найти в нашей [презентации](presentation.pdf).

Пример [результата](https://drive.google.com/file/d/1BTqY3Tc9OZEplMusiilhykBEDd11Cvab/view?usp=sharing).

# Аватары

Аватар - анимированный персонаж, который с помощью голосовой озвучки способен отвечать на запрос пользователя. В рамках нашего проекта мы постарались поддержать различных аватаров, которых сгенерировали при помощи нейросети [Kandinsky v3](https://github.com/ai-forever/Kandinsky-3). 


<p float="left">
	<img src="avatars/0.png" width=22% height=22%>
	<img src="avatars/1.png" width=22% height=22%>
	<img src="avatars/2.png" width=22% height=22%>
	<img src="avatars/3.png" width=22% height=22%>
</p>


Статичные изображения можно анимировать под аудио голоса с помощью ML моделей, которые решают задачи Talking Head Animation и Lip Sync.

# Использование продукта

Использование продукта:

* Выбор аватара:

  * Пользователь открывает веб-сайт и видит первый экран, на котором представлен выбор из нескольких аватаров.
  * Пользователь выбирает аватар, с которым он хочет взаимодействовать, нажимая на изображение.

* Начало взаимодействия:
  * После выбора аватара пользователь нажимает кнопку "Старт" или "Начать".
  * Веб-сайт запускает голосовой помощник и начинает запись голосового ввода вопроса.
* Отправка вопроса:
    * Пользователь произносит вопрос вслух, используя микрофон своего устройства.
    * После завершения речи пользователь нажимает кнопку "Отправить".
* Обработка запроса:
    * Веб-сайт отправляет введенный вопрос на сервер для обработки.
    * Сервер использует алгоритмы обработки естественного языка для понимания запроса пользователя.
* Ответ голосом аватара:
  * После обработки запроса сервер отправляет данные обратно на веб-сайт.
  * Веб-сайт воспроизводит ответ голосом/субтитрами через выбранного пользователем аватара.
  * Ответ может быть сопровожден анимацией мимики и жестов аватара.

* Завершение сеанса:
  * Пользователь может продолжать взаимодействие с аватаром, задавая новые вопросы, либо завершить сеанс, закрыв окно браузера или нажав на соответствующую кнопку.
  * При завершении сеанса веб-сайт закрывает подключение к голосовому помощнику и завершает работу.
  * Данные сессии не сохраняются.


# Решение

Ниже изображена схема решения:

![схема](scheme.jpg)

Для начала пользователю предоставляется выбор аватара для взаимодействия. Далее он может обращаться к нему голосом, который через веб-браузер и Web Speech API преобразуется в текст. Текст предобрабатывается и подается на вход вместе с системным промптом большой языковой модели - [GigaChat](https://developers.sber.ru/gigachat/login). При необходимости добавляется промпт для перевода на английский язык. После чего сгенрированный ответ LLM с помощью [Yandex SpeechKit](https://cloud.yandex.com/en/services/speechkit) преобразуется в аудио WAV файл. Для хранения медиа файлов используется облачное хранилище S3.



Анимация аватара происходит с помощью ML модели [SadTalker](https://github.com/OpenTalker/SadTalker), которая объединяет в себе сразу несколько генеративных моделей для рендеринга видео-потока на основе VAE и GAN. На вход модели подается аудио файл, который сохраняется в облачном хранилище (data storage) в формате wav, и референс изображения для анимации. Результат работы модели отправляется с сервера в облачное хранилище для дальнейшего показа пользователю в браузере.

# Деплой 

Сайт решения - https://site-hack-2024.website.yandexcloud.net/. Из-за множества запросов и все же не online взаимодействия (генерация 1 секунды в среднем занимает около 8-10 секунд на сервере) ответ может задерживаться. 

Для того чтобы развернуть сайт понадобится Yandex Cloud и добавление cloud functions, которые выполняются на Python. Сайт обменивается запросами с YandexGPT по API и также с удаленным сервером с GPU, на котором развернута ML модель для анимации аватаров для ускорения ее работы.


# Команда

* Вадим Шабашов | ИТМО
* Евсеев Елисей | ИТМО
* Иванцов Илья | ИТМО
* Илькин Галоев | ИТМО
* Анвар Тлямов | ИТМО
* Ольга Фахразиева | Авито

