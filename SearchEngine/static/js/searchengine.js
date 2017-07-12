function openNav() {
    document.getElementById("mySidenav").style.width = "70%";
    // document.getElementById("flipkart-navbar").style.width = "50%";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.body.style.backgroundColor = "rgba(0,0,0,0)";
}

function search_result() {
	choiceform = document.getElementById('pre-selected-options')
    var listLength = choiceform.length;
    var selected = []
    for(var i=0;i<listLength;i++){
        if(choiceform[i].selected)
            selected.push(choiceform[i].value);
        }
    var search_query = $('submit_search').val()
    $.ajax({
        url : "search_result/" + search_query, // the endpoint
        type : "POST", // http method
        data : { 'search' : search_query, 'selected': selected }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //$('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};