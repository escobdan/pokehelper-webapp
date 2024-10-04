// Syncronize timers
var tsp = new Date('Sun June 06 2024 17:55:15 GMT+0100 (CST)'); // "Timestamp"

window.onload = function() {
    // Get navigation timing entries
    const entries = performance.getEntriesByType("navigation");
    
    if (entries.length > 0) {
        const navigationTiming = entries[0]; // Get the first navigation entry
        
        // Synchronize the timestamp with the server
        tsp.setTime(tsp.getTime() + navigationTiming.loadEventStart - navigationTiming.navigationStart);
    }
};

// Counters tabs
$(function () {
    // Optional: Activate the first tab on page load
    $('#strong-against-tab').tab('show');
});

// function getSyncedServerTime() {
//     // Get current timestamp in milliseconds
//     var clientTimestamp = new Date().getTime();

//     $.ajax({
//         url: "getdatetimejson/?ct="+clientTimestamp, 
//         type: "GET",
//         success: (response) => {
//             // Get current timestamp in milliseconds
//             var nowTimeStamp = new Date().getTime();
    
//             // Parse server-client difference time and server timestamp from response
//             var serverClientRequestDiffTime = data.diff;
//             var serverTimestamp = data.serverTimestamp;
    
//             // Calculate server-client difference time on response and response time
//             var serverClientResponseDiffTime = nowTimeStamp - serverTimestamp;
//             var responseTime = (serverClientRequestDiffTime - nowTimeStamp + clientTimestamp - serverClientResponseDiffTime ) / 2
    
//             // Calculate the synced server time
//             var syncedServerTime = new Date(nowTimeStamp + (serverClientResponseDiffTime - responseTime));
        
//             // You may want to do something with syncedServerTime here. For this example, we'll just alert.
//             alert(syncedServerTime);
//         },
//         error: (xhr, status, error) => {
//             console.error("Error:", error);
//         }
//     });
// }

// getSyncedServerTime();

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
// setInterval(fetchData, 5000);

setInterval(function() {
    tsp.setSeconds(tsp.getSeconds() + 5);
    document.title = tsp.toString();
    fetchData();
}, 5000); // Update every 5 seconds