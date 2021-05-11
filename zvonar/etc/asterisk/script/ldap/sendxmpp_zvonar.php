#!/usr/bin/php
<?php

/* Переменные для получения параметров */
$phoneto = $argv[1];
$phonefrom = $argv[2];
$username = "";
$userdep = "";
$usertitle = "";
$userlogin="";
$xmppmessage="";

/* Вытягиваем по номеру телефона инфу из AD */
$LDAP_BINDDN = "ldap@домен.local";
$LDAP_PASS = "пароль";
$LDAP_BASE_DN = "DC=домен,DC=local";

function ConnectToServer()
{
  $LDAP_SERVER = "ip-address";
  $LDAP_PORT = "389";
  $ds=ldap_connect($LDAP_SERVER, $LDAP_PORT);
  ldap_set_option($ds, LDAP_OPT_PROTOCOL_VERSION, 3);
  ldap_set_option($ds, LDAP_OPT_REFERRALS, 0);
  return $ds;
}

/* Ищем по первому аргументу пользователя которому отправить сообщение */

if ($phoneto != "") {

$ds=ConnectToServer();
$ldapbind = ldap_bind($ds, $LDAP_BINDDN , $LDAP_PASS);

if ($ldapbind) {

    $filter = "(&(telephonenumber=$phoneto)(objectClass=top)(objectCategory=person)(objectClass=user)(objectClass=person)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))";
    $sr=ldap_search($ds, $LDAP_BASE_DN, $filter, array("telephonenumber","samaccountname"));
    ldap_sort( $ds, $sr, "telephonenumber");
    $info = ldap_get_entries($ds, $sr);

    for($i=0; $i<$info["count"]; $i++) {
        $userlogin = $info[$i]["samaccountname"][0];
    }
}

/* ldap_close($ds); */
} else {echo "Первая переменная пустая"."\n";}

/* Ищем по второму аргументу пользователя от которого был звонок */

if ($phonefrom != "") {

/* $ds=ConnectToServer(); */
$ldapbind = ldap_bind($ds, $LDAP_BINDDN , $LDAP_PASS);

if ($ldapbind) {

   $filter = "(&(telephonenumber=$phonefrom)(objectClass=top)(objectCategory=person)(objectClass=user)(objectClass=person)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))";
   $sr=ldap_search($ds, $LDAP_BASE_DN, $filter, array("displayname", "department", "title",  "mail", "telephonenumber","samaccountname"));
   ldap_sort( $ds, $sr, "displayname");
   $info = ldap_get_entries($ds, $sr);

   for($i=0; $i<$info["count"]; $i++) {
       $username = $info[$i]["displayname"][0];
       $userdep = $info[$i]["department"][0];
       $usertitle = $info[$i]["title"][0];
    }
}

ldap_close($ds);
} else {echo "Вторая переменная пустая"."\n";}

/* Формируем сообщение для xmpp */
/* Если у сотрудника не задано имя, должность или отдел, то не отображаем соотв. заголовки */

 if ($username == "") $xmppmessage = 'Входящий звонок от автообзвона '.$phonefrom;
 if ($username !== "")
 {
   if ($userdep == "" && $usertitle == "") $xmppmessage = 'Входящий звонок от '.$phonefrom."\n".'Имя: '.$username;
   elseif ($userdep == "" && $usertitle !== "") $xmppmessage = 'Входящий звонок от '.$phonefrom."\n".'Имя: '.$username."\n".'Должность: '.$usertitle;
   elseif ($usertitle == "" && $userdep !== "") $xmppmessage = 'Входящий звонок от '.$phonefrom."\n".'Имя: '.$username."\n".'Отдел: '.$userdep;
   else $xmppmessage = 'Входящий звонок от '.$phonefrom."\n".'Имя: '.$username."\n".'Должность: '.$usertitle."\n".'Отдел: '.$userdep;
 }


/* Способ короче */
/*
$xmppmessage = 'Входящий звонок от '.
$phonefrom."\n".
($username?'Имя '.$username."\n":'').
($usertitle?'Должность: '.$usertitle."\n":'').
($userdep?'Отдел: '.$userdep."\n":'');
*/

/* Отправляем сообщение xmpp пользователю */
$sendmessage="echo '".$xmppmessage."' | sendxmpp -t -n -j servername:5222 -u jabberuser -p пароль ".$userlogin."@домен.local";
//echo $sendmessage;
shell_exec($sendmessage);
?>
