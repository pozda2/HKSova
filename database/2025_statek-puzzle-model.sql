<!DOCTYPE html>
<html lang="cs" dir="ltr">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Export: hksova - database - Adminer</title>
<link rel="stylesheet" href="?file=default.css&amp;version=5.4.0">
<link rel='stylesheet' media='(prefers-color-scheme: dark)' href='?file=dark.css&amp;version=5.4.0'>
<meta name='color-scheme' content='light dark'>
<script src='?file=functions.js&amp;version=5.4.0' nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U="></script>
<link rel='icon' href='data:image/gif;base64,R0lGODlhEAAQAJEAAAQCBPz+/PwCBAROZCH5BAEAAAAALAAAAAAQABAAAAI2hI+pGO1rmghihiUdvUBnZ3XBQA7f05mOak1RWXrNq5nQWHMKvuoJ37BhVEEfYxQzHjWQ5qIAADs='>
<link rel='apple-touch-icon' href='?file=logo.png&amp;version=5.4.0'>

<body class='ltr nojs adminer'>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">mixin(document.body, {onkeydown: bodyKeydown, onclick: bodyClick});
document.body.classList.replace('nojs', 'js');
const offlineMessage = 'Jste offline.';
const thousandsSeparator = ' ';</script>
<div id='help' class='jush-sql jsonly hidden'></div>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">mixin(qs('#help'), {onmouseover: () => { helpOpen = 1; }, onmouseout: helpMouseout});</script>
<div id='content'>
<span id='menuopen' class='jsonly'><button type='submit' name='' title='' class='icon icon-move'><span>menu</span></button></span><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">qs('#menuopen').onclick = event => { qs('#foot').classList.toggle('foot'); event.stopPropagation(); }</script>
<p id="breadcrumb"><a href="?server=database">MariaDB</a> » <a href='?server=database&amp;username=hksova' accesskey='1' title='Alt+Shift+1'>database</a> » <a href="?server=database&amp;username=hksova&amp;db=hksova">hksova</a> » Export
<h2>Export: hksova</h2>
<div id='ajaxstatus' class='jsonly hidden'></div>

<form action="" method="post">
<table class="layout">
<tr><th>Výstup<td><label><input type='radio' name='output' value='text' checked>otevřít</label><label><input type='radio' name='output' value='file'>uložit</label><label><input type='radio' name='output' value='gz'>gzip</label>
<tr><th>Formát<td><label><input type='radio' name='format' value='sql' checked>SQL</label><label><input type='radio' name='format' value='csv'>CSV,</label><label><input type='radio' name='format' value='csv;'>CSV;</label><label><input type='radio' name='format' value='tsv'>TSV</label>
<tr><th>Databáze<td><select name='db_style'><option selected><option>USE<option>DROP+CREATE<option>CREATE</select><label><input type='checkbox' name='routines' value='1'>Procedury a funkce</label><label><input type='checkbox' name='events' value='1'>Události</label><tr><th>Tabulky<td><select name='table_style'><option><option selected>DROP+CREATE<option>CREATE</select><label><input type='checkbox' name='auto_increment' value='1'>Auto Increment</label><label><input type='checkbox' name='triggers' value='1' checked>Triggery</label><tr><th>Data<td><select name='data_style'><option><option>TRUNCATE+INSERT<option selected>INSERT<option>INSERT+UPDATE</select></table>
<p><input type="submit" value="Export">
<input type='hidden' name='token' value='73184:553376'>

<table>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">qsl('table').onclick = dumpClick;</script>
<thead><tr><th style='text-align: left;'><label class='block'><input type='checkbox' id='check-tables'>Tabulky</label><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">qs('#check-tables').onclick = partial(formCheck, /^tables\[/);</script><th style='text-align: right;'><label class='block'>Data<input type='checkbox' id='check-data'></label><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">qs('#check-data').onclick = partial(formCheck, /^data\[/);</script></thead>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='forum'>forum</label><td align='right'><label class='block'><span id='Rows-forum'></span><input type='checkbox' name='data[]' value='forum'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='forum_section'>forum_section</label><td align='right'><label class='block'><span id='Rows-forum_section'></span><input type='checkbox' name='data[]' value='forum_section'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='mascot'>mascot</label><td align='right'><label class='block'><span id='Rows-mascot'></span><input type='checkbox' name='data[]' value='mascot'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='menu'>menu</label><td align='right'><label class='block'><span id='Rows-menu'></span><input type='checkbox' name='data[]' value='menu'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='page'>page</label><td align='right'><label class='block'><span id='Rows-page'></span><input type='checkbox' name='data[]' value='page'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='place'>place</label><td align='right'><label class='block'><span id='Rows-place'></span><input type='checkbox' name='data[]' value='place'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='player'>player</label><td align='right'><label class='block'><span id='Rows-player'></span><input type='checkbox' name='data[]' value='player'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='puzzle' checked>puzzle</label><td align='right'><label class='block'><span id='Rows-puzzle'></span><input type='checkbox' name='data[]' value='puzzle' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='setting'>setting</label><td align='right'><label class='block'><span id='Rows-setting'></span><input type='checkbox' name='data[]' value='setting'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='team'>team</label><td align='right'><label class='block'><span id='Rows-team'></span><input type='checkbox' name='data[]' value='team'></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='year'>year</label><td align='right'><label class='block'><span id='Rows-year'></span><input type='checkbox' name='data[]' value='year'></label>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">ajaxSetHtml('?server=database&username=hksova&db=hksova&script=db');</script>
</table>
</form>
<p><a href='?server=database&amp;username=hksova&amp;db=hksova&amp;dump=forum%25'>forum</a></div>

<div id='foot' class='foot'>
<div id='menu'>
<h1><a href='https://www.adminer.org/' target="_blank" rel="noreferrer noopener" id='h1'><img src='?file=logo.png&amp;version=5.4.0' width='24' height='24' alt='' id='logo'>Adminer</a> <span class='version'>5.4.0 <a href='https://www.adminer.org/#download' target="_blank" rel="noreferrer noopener" id='version'></a></span></h1>
<form action='' method='post'>
<div id='lang'><label>Jazyk: <select name='lang'><option value="en">English<option value="ar">العربية<option value="bg">Български<option value="bn">বাংলা<option value="bs">Bosanski<option value="ca">Català<option value="cs" selected>Čeština<option value="da">Dansk<option value="de">Deutsch<option value="el">Ελληνικά<option value="es">Español<option value="et">Eesti<option value="fa">فارسی<option value="fi">Suomi<option value="fr">Français<option value="gl">Galego<option value="he">עברית<option value="hi">हिन्दी<option value="hu">Magyar<option value="id">Bahasa Indonesia<option value="it">Italiano<option value="ja">日本語<option value="ka">ქართული<option value="ko">한국어<option value="lt">Lietuvių<option value="lv">Latviešu<option value="ms">Bahasa Melayu<option value="nl">Nederlands<option value="no">Norsk<option value="pl">Polski<option value="pt">Português<option value="pt-br">Português (Brazil)<option value="ro">Limba Română<option value="ru">Русский<option value="sk">Slovenčina<option value="sl">Slovenski<option value="sr">Српски<option value="sv">Svenska<option value="ta">த‌மிழ்<option value="th">ภาษาไทย<option value="tr">Türkçe<option value="uk">Українська<option value="uz">Oʻzbekcha<option value="vi">Tiếng Việt<option value="zh">简体中文<option value="zh-tw">繁體中文</select><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">qsl('select').onchange = function () { this.form.submit(); };</script></label> <input type='submit' value='Vybrat' class='hidden'>
<input type='hidden' name='token' value='246413:700109'>
</div>
</form>
<script src='?file=jush.js&amp;version=5.4.0' nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=" defer></script>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">
var jushLinks = { sql:{
	"?server=database&username=hksova&db=hksova&table=$&": /\b(forum|forum_section|mascot|menu|page|place|player|puzzle|setting|team|year)\b/g
}
};
jushLinks.bac = jushLinks.sql;
jushLinks.bra = jushLinks.sql;
jushLinks.sqlite_quo = jushLinks.sql;
jushLinks.mssql_bra = jushLinks.sql;
</script>
<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">syntaxHighlighting('12', 'maria');</script>
<form action=''>
<p id='dbs'>
<input type='hidden' name='server' value='database'>
<input type='hidden' name='username' value='hksova'>
<label title='Databáze'>DB: <select name='db'><option value=""><option selected>hksova<option>information_schema</select><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">mixin(qsl('select'), {onmousedown: dbMouseDown, onchange: dbChange});</script>
</label><input type='submit' value='Vybrat' class='hidden'>
<input type='hidden' name='dump' value=''>
</p></form>
<p class='links'>
<a href='?server=database&amp;username=hksova&amp;db=hksova&amp;sql='>SQL příkaz</a>
<a href='?server=database&amp;username=hksova&amp;db=hksova&amp;import='>Import</a>
<a href='?server=database&amp;username=hksova&amp;db=hksova&amp;dump=' id='dump' class='active '>Export</a>
<a href="?server=database&amp;username=hksova&amp;db=hksova&amp;create=">Vytvořit tabulku</a>
<ul id='tables'><script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">mixin(qs('#tables'), {onmouseover: menuOver, onmouseout: menuOut});</script>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=forum" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=forum" class='structure' title='Zobrazit strukturu'>forum</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=forum_section" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=forum_section" class='structure' title='Zobrazit strukturu'>forum_section</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=mascot" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=mascot" class='structure' title='Zobrazit strukturu'>mascot</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=menu" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=menu" class='structure' title='Zobrazit strukturu'>menu</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=page" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=page" class='structure' title='Zobrazit strukturu'>page</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=place" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=place" class='structure' title='Zobrazit strukturu'>place</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=player" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=player" class='structure' title='Zobrazit strukturu'>player</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=puzzle" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=puzzle" class='structure' title='Zobrazit strukturu'>puzzle</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=setting" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=setting" class='structure' title='Zobrazit strukturu'>setting</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=team" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=team" class='structure' title='Zobrazit strukturu'>team</a>
<li><a href="?server=database&amp;username=hksova&amp;db=hksova&amp;select=year" class='select' title='Vypsat data'>vypsat</a> <a href="?server=database&amp;username=hksova&amp;db=hksova&amp;table=year" class='structure' title='Zobrazit strukturu'>year</a>
</ul>
</div>
<form action="" method="post">
<p class="logout">
<span>hksova
</span>
<input type="submit" name="logout" value="Odhlásit" id="logout">
<input type='hidden' name='token' value='568117:116597'>
</form>
</div>

<script nonce="ZDc4NmJhMWIzMGJlNTU4ZGRlYjZjMWRhMThlNDdmM2U=">setupSubmitHighlight(document);</script>
