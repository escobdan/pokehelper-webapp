var tsp; // Declare timestamp variable

function getServerTime() {
    // Get the current client timestamp in milliseconds
    const clientTimestamp = new Date().getTime();

    return $.ajax({
        url: "/getdatetimejson", // Adjust this URL as needed
        type: "GET",
        data: { ct: clientTimestamp }
    });
}

function syncClients() {
    getServerTime().then(response => {
        const now = new Date();
        const serverTimestamp = new Date(response.serverTimestamp); // Assuming response contains serverTimestamp
        const clientTimestamp = now.getTime();
        
        // Calculate the difference between server and client time
        const timeDiff = serverTimestamp.getTime() - clientTimestamp;
        
        // Set the timestamp to server time
        tsp = new Date(now.getTime() + timeDiff); 
    }).catch(error => {
        console.error("Error fetching server time:", error);
    });
}

function fetchData() {
    $.ajax({
        url: "/_update-data/",
        type: "POST",
        success: (response) => {
            if (response.data == true) {
                console.log("already updated");
            } else {
                console.log("updating page");
                response.data.forEach(user => {
                    if (user.new) {
                        console.log("new user, creating navlink and tabpane");
                        $('ul#nav-link-player-list').append(user.navlink);
                        $('div#v-players-tabContent').append(user.tabpane);
                    } else {
                        console.log("existing user, updating tab content");
                        $('div#v-' + user.username + '-tab').html(user.tabpane);
                    }
                });
            }
        },
        error: (xhr, status, error) => {
            console.error("Error:", error);
        }
    });
}

window.onload = function() {
    syncClients(); // Sync clients on load

    // Fetch data every 5 seconds based on synchronized time
    setInterval(function() {
        tsp.setSeconds(tsp.getSeconds() + 5); // Increment timestamp by 5 seconds
        document.title = tsp.toString(); // Update document title
        
        fetchData(); // Call fetchData every 5 seconds
    }, 5000); // Update every 5 seconds
};