function fetchData() {
    $.ajax({
        url: "/_update-data/",
        type: "POST",
        success: (response) => {
            console.log(response.data);
            if(response.data == true) {
                console.log("already updated");
            }
            else {
                $('div#battle-main-block').html(response.data);
            }
            // $('div#main-block').html(response.data)
        },
        error: (xhr, status, error) => {
            console.error("Error:", error);
        }
    });
}

// Fetch data every 5 seconds
setInterval(fetchData, 5000);