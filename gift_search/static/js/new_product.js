$(document).ready(function(){


    $().on("click", function(){
        $.ajax({
            url: '/new_pokemon/',
            type: 'POST',
            dataType: 'json',
            data: pokemonData,
            success: function(response) {
                console.log(JSON.stringify(response));
                getPokemonTeam();
                console.log('complete savePokemon')
            },
            error: function(response) {
                console.log(response.body);
            }
        });
    });
});