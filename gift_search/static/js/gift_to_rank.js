$(document).ready(function(){
var receiverID;


    $(".ranking").on("click", function(){
        console.log('click')
        var rank = $(this).attr("id");
        console.log(rank);
        receiverId = location.pathname.split('/')[2]; //string
        console.log(receiverId);
//        var product= $('giftToRank');
//        console.log(product);
//        var product_id = product.attr('id');
//        console.log(product_id);
        var product_id = '1423146735';
        $.ajax({
            url:'/receiver_page/' + window.receiverId + '/' + rank + '/' + product_id + '/',
            type: 'POST',
            success: function(response){
                console.log('success');
//                //update history
//                updateHistory();
//                //update topRecommendations
//                updateRecommendations();
            },
            error: function(response){
                console.log(response.body);
            }
        });
    });

    var updateHistory = function(){
        $.ajax({
                url: '/update_history/' + receiverId + '/',
                type: 'GET',
                success: function(response) {
                    console.log('success');
                    $('#history').html(response); //add this
                },
                error: function(response) {
                    console.log(response.body);
                }
            });

    };

    var updateRecommendations = function(){
        $.ajax({
                url: '//',
                type: 'GET',
                success: function(response) {
                    console.log('success');
                },
                error: function(response) {
                    console.log(response.body);
                }
            });

    }
});
