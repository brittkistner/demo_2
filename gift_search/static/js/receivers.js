$(document).ready(function(){

    $(".receiver_page").on("click", function(){
        console.log('click');
        window.receiverId = $(this).attr("id");
        console.log(receiverId);
        $.ajax({
            url:'/receiver_page/' + receiverId + '/',
            type: 'GET',
            success: function(response){
                console.log('success');
            },
            error: function(response){
                console.log(response.body);
            }
        });
    });
});