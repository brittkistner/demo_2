


//$(document).ready(function(){
//
//    (function () {
//        var po = document.createElement('script');
//        po.type = 'text/javascript';
//        po.async = true;
//        po.src = 'https://plus.google.com/js/client:plusone.js?onload=start';
//        var s = document.getElementsByTagName('script')[0];
//        s.parentNode.insertBefore(po, s);
//    })();
//
//    window.signInCallback = function (result) {
//        if (result['error']) {
//            if (result['error'] != "immediate_failed"){
//                alert('An error happened:', result['error']);
//                console.log(result);
//            }
//        } else {
//            $('#code').attr('value', result['code']);
//            $('#at').attr('value', result['access_token']);
//            $('#google-plus').submit();
//        }
//    };
//});