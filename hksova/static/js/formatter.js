function teamFormatter(value, row) {
    str="";
    if (row["team-web"]) {
        str+="<a href=\""+row["team-web"]+'"';
        str+=">";
        str+=row["team-name"]+"</A>";
    } else {
        str+=row["team-name"];
    }
    return str;
}

function teamsActionFormatter(value, row) {
    return row['team-action'];
}

function settingsActionFormatter(value, row) {
    return row['setting-action'];
}

function pagesActionFormatter(value, row) {
    return row['page-action'];
}

function menuActionFormatter(value, row) {
    return row['menu-action'];
}

function forumsActionFormatter(value, row) {
    return row['forum-action'];
}

function forumFormatter(value, row) {
    str="";
    if (row["section-url"]) {
        str+="<a href=\""+row["section-url"]+'"';
        str+=">";
        str+=row["section-name"]+"</A>";
    } else {
        str+=row["section-name"];
    }
    return str;
}
