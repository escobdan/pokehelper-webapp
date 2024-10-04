// Counters tabs
$(function () {
    // Optional: Activate the first tab on page load
    $('#strong-against-tab').tab('show');
});

function fetchData() {
    $.ajax({
        url: "/_update-data/",
        type: "POST",
        success: (response) => {
            if(response.data == true) {
                console.log("already updated");
            }
            else {
                console.log("updating page")
                // $('div#battle-main-block').html(response.data);
                response.data.forEach( user => {
                    if (user.new) {
                        // Render new nav link and tabpanel and append them to main body
                        console.log("new user, creating navlink and tabpane")
                        $('ul#nav-link-player-list').append(user.navlink);
                        $('div#v-players-tabContent').append(user.tabpane);
                    }
                    else {
                        // only render tab panel and replace current
                        console.log("existing user, updating tab content")
                        $('div#v-'+user.username+'-tab').html(user.tabpane);
                    }
                });
            }
        },
        error: (xhr, status, error) => {
            console.error("Error:", error);
        }
    });
}

// Fetch data every 5 seconds
setInterval(fetchData, 5000);