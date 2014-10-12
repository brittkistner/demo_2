$(document).ready(function(){
var receiverID;


    $(".ranking").on("click", function(){
        console.log('click')
        var rank = $(this).attr("id");
        console.log(rank);
        receiverId = location.pathname.split('/')[2]; //string
        console.log(receiverId);
        var product_id = $(".giftToRank").data('id');
        console.log(product_id);
        $.ajax({
            url:'/receiver_page/' + window.receiverId + '/' + rank + '/' + product_id + '/',
            type: 'POST',
            success: function(response){
                console.log(response);
                console.log('success');
                //update history
                updateHistory();
                //update topRecommendations
                updateRecommendations();
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
                    console.log('success');
                    $('#top_recommendations').html(response);
                },
                error: function(response) {
                    console.log(response.body);
                }
            });

    }
});
