$(document).ready(function(){


    $(".ranking").on("click", function(){
        console.log('click')
        var rank = $(this).attr("id");
        console.log(rank);
        console.log(window.receiverId);
        var product_id = getElementsByClassName('giftToRank');
        console.log(product_id);
        $.ajax({
            url:'/receiver_page/' + window.receiverId + '/' + rank + '/' + product_id + '/',
            type: 'POST',
            success: function(response){
                console.log('success');
            },
            error: function(response){
                console.log(response.body);
            }
        });
    });
});
