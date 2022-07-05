const mobileScreen = window.matchMedia("(max-width: 990px )");
$(document).ready(function () {
    if (Cookies.get('hksova-menu')) {
        id=Cookies.get('hksova-menu');
        $("#"+id).addClass("show");
    };


    $(".dashboard-nav-dropdown-toggle").click(function () {
        $(this).closest(".dashboard-nav-dropdown")
            .toggleClass("show")
            .find(".dashboard-nav-dropdown")
            .removeClass("show");
        $(this).parent()
            .siblings()
            .removeClass("show");

        if ($(this).closest(".dashboard-nav-dropdown").hasClass('show')==true) {
            Cookies.set('hksova-menu', $(this).closest(".dashboard-nav-dropdown").attr('id'));
        } else {
            if (Cookies.get('hksova-menu')) {
                Cookies.remove("hksova-menu");
            }
        }
    });

    $(".dashboard-nav-item-alone").click(function () {
        Cookies.remove("hksova-menu");
    });

    $(".menu-toggle").click(function () {
        if (mobileScreen.matches) {
            $(".dashboard-nav").toggleClass("mobile-show");
        } else {
            $(".dashboard").toggleClass("dashboard-compact");
        }
    });
});