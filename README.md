# Starknet-2FA_remove_-check 

Проверяет кошельки на сайте https://starkscan.co/ по адресу (Работаем через прокси).Проверяет последнюю транзакцию на запрос отзыва 2FA с кошельков Argent и Braavos. Если вы решили не менять приватник через скрипты к кошельку, а поставили 2FA. 

Если найдет транзакцию такого типа то значит ваши привтники утекли и кто то пытается снять 2 FA. У вас есть в случае Argent X 7 дней и 4 дня в случае Braavos на отмену отзыва 2FA ключа через Расширение или напрямую через контракт.

Заполняем файлы

wallets.txt - адреса кошельков. НИ В КОЕМ СЛУЧАЕ ПРИВАТНИК НЕЛЬЗЯ!

proxy.txt - прокси в формате login:pass@IP:port 

Можно изменить в строке 83. control_date ='2023-12-07' # контрольная датаю Если последняя дата транзакции на отзыв 2FA, установку 2FA или произошла смена приватника то выделит строчку с кошельком красным цветом

В строке 88  прописаны  частичное название функции при обнаружении которых выделять  красным при условии того что транзакция сделана после или в контрольную дату.

if 'setPublicKey' in selector_identifier or 'change_owner' in selector_identifier or 'remove_signer' in selector_identifier or 'escape' in selector_identifier:

setPublicKey - В Braavos сменили приватный ключ (печаль)

change_owner - В Argent X сменили приватный ключ 

remove_signer - В Braavos сделан запрос на отзыв привязки 2Fa (к мобиле) Есть 4 дня с даты запроса на отмену

escape - В Argent X Запрос на отзыв привязки 2Fa (к почте) Есть 7 дней с даты запроса на отмену

