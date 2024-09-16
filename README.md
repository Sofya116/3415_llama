# 3415_llama
Правила игры:

•Перемешать колоду и раздать по 6 карт каждому игроку;

•Оставшиеся карты положить в центр стола, чтобы сформировать стопку лицом вниз;

•Перевернуть верхнюю карту из стопки розыгрыша, чтобы начать начать стопку «бито»;

•Положить все маркеры на стол;

•Игра проводится раундами: самый молодой игрок начинает первый раунд;

•Сыграть пасы слева.

Возможные действия:

•Разыграть карту из вашей руки на стопке «бито»;

•Вытащить карту, чтобы взять её;

•Выйти из раунда(положить карточки перед собой лицом вниз). Верхняя карта на сброшенной стопке определяет, какую карту вы можете разыграть: то же значение, что и верхняя карта или значение +1; лама на 6 или на другую ламу; 1 на ламу.

Примечание: Вы не можете разыграть карту в тот же ход, когда вы её разыграете, поэтому разыграйте пасы слева от вас.

Конец раунда: •Один игрок разыгрывает свою последнюю карту •Все игроки покинули раунд

Подсчет очков: Каждая карта, которую вы не разыграли, дает вам отрицательные очки, независимо от того, находится ли она в вашей руке или лицом вниз перед вами, потому что вы покинули раунд. Каждая карта стоит своей стоимости в баллах. Ламы стоят 10 баллов. Тем не менее, вы считаете значение каждой карты только один раз за раунд, поэтому, если у вас есть две 4, например, вы получаете только четыре очка, а все ваши ламы дают вам только 10 очков.

Комплектность: •56 карт (8 каждый со значениями 1-6 и 8 лам) •70 маркеров (20 чёрных 10, 50 белых 1)

Раздача: •2-6 игроков •возраст: 8+ •время игры: ~20 минут

Условие победы: Иметь наименьшее количество очков, когда счёт одного игрока достигнет 40.

Пример текстового интерфейса игры:

Бито: 2 Ника: 3 5 4 1 Л Ника: введите какую карту играем из руки: 8 Ника: такой карты нет в руке Ника: введите какую карту играем из руки: 3 Ника: играет 3
Бито: 3 Соня: 6 2 8 5 Л Соня: берёт карту Соня : 6 2 8 5 Л 4 Соня: Играет 4
Бито: 4 Ника: 5 4 1 Л Ника: играет 5
Бито: 5 Соня: 6 2 8 5 Л Соня: играет 6
Бито: 6 Ника: 4 1 Л ....
Ника WIN!

Формат save-файла:
{ "top": "2", "deck": "7 3 1 8 4", "current_player_index": 0, "players": [ { "name": "Alex", "hand": "5 6 4 2", "is_human": true }, { "name": "Bob", "hand": "6 2 4", "is_human": false } ] }
