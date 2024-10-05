// Counters tabs
$(function () {
    // Optional: Activate the first tab on page load
    $('#strong-against-tab').tab('show');
});

const socket = io();

socket.on("newData", function(data) {
    if (data.new) {
        // Render new nav link and tabpanel and append them to main body
        console.log("new user, creating navlink and tabpane")
        $('ul#nav-link-player-list').append(data.navlink);
        $('div#v-players-tabContent').append(data.tabpane);
    }
    else {
        // only render tab panel and replace current
        console.log("existing user, updating tab content")
        $('div#v-'+data.username+'-tab').html(data.tabpane);
    }
});