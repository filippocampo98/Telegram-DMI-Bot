-- chat_id_list
CREATE TABLE IF NOT EXISTS `Chat_id_List` (
  `id` int(11) NOT NULL,
  `Chat_id` int(11) NOT NULL,
  `Username` text NOT NULL,
  `Nome` int(11) NOT NULL,
  `Cognome` int(11) NOT NULL,
  `E-mail` int(11) NOT NULL
);

ALTER TABLE `Chat_id_List`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `Chat_id_List`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- stat_list
CREATE TABLE IF NOT EXISTS stat_list (
	Type varchar(100),
	chat_id int(100),
	DateCommand DATE
);

-- subscriptions
CREATE TABLE IF NOT EXISTS `subscriptions` (
  `chatid` INT(11) NOT NULL,
  `mensa` INT(11) NOT NULL,
  `news` INT(11) NOT NULL
);