$(document).ready(function(){

    $("#modal_trigger").leanModal({top : 200, overlay : 0.6, closeButton: ".modal_close" });
    $(function () {
        $("#register_form").click(function () {
            $(".user_login").hide();
            $(".user_register").show();
            $(".header_title").text('Register');
            return false;
        });
    })
});