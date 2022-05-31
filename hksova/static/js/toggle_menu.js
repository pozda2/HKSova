function toggleMenu() {
	var x = document.getElementById("collapsiblemenu");
	if (x.className === "") {
		x.className += "collapsed";
	} else {
		x.className = "";
	}
}
