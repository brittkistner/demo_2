$(document).ready(function(){
var receiverID;


    $(".ranking").on("click", function(){
        console.log("click")
        var rank = $(this).attr("id");
        console.log(rank);
        receiverId = location.pathname.split('/')[2]; //string
        console.log(receiverId);
        var product_id = $(".giftToRank").data('id');
        console.log(product_id);
        console.log(rank);
        $.ajax({
            url:'/receiver_page/' + window.receiverId + '/' + rank + '/' + product_id + '/',
            type: 'POST',
            success: function(response){
                console.log(response);
                //update history
                updateHistory();
                //update topRecommendations
                updateRecommendations();
                //get the next product to rank
                getNextProduct();
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
                    $('#history').html(response);
                },
                error: function(response) {
                    console.log(response.body);
                }
        });
    };

    var updateRecommendations = function(){
        $.ajax({
                url: '/top_recommendations/' + receiverId +'/',
                type: 'GET',
                success: function(response) {
                    console.log('top');
                    $('#top_recommendations').html(response);
                },
                error: function(response) {
                    console.log(response.body);
                }
        });
    };

    var getNextProduct = function(){
        $.ajax({
                url: '/get_next_product/',
                type: 'GET',
                success: function(response) {
                    console.log('rank_product');
                    $('#product_rank').html(response);
                },
                error: function(response) {
                    console.log(response.body);
                }
         });
    };
});
