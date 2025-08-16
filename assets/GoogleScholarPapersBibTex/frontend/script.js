document.getElementById("runSpider").addEventListener("click", function() {
    const papers = document.getElementById("papers").value;
    if (papers.trim() === "") {
        alert("Please enter at least one paper!");
        return;
    }
    const formData = new URLSearchParams();
    formData.append("papers", papers);
    const runButton = document.getElementById("runSpider");
    runButton.disabled = true;
    runButton.textContent = "Processing...";
    runButton.style.backgroundColor = "#ff9800";
    fetch("http://127.0.0.1:5000/spider", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log("Spider Success: ", data.message);
                alert(`Spider Success: ${data.message}`);
            } else {
                console.error("Spider Error: ", data.message);
                alert(`Spider Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("Error: ", error);
            alert(`Failed to run spider. ${error}`);
        })
        .finally(() => {
            document.getElementById("downloadZip").style.display = "inline";
            runButton.disabled = false;
            runButton.textContent = "Run";
            runButton.style.backgroundColor = "#4CAF50";
        });
});

document.getElementById("fileInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const fileContent = e.target.result;
            document.getElementById("papers").value = fileContent;
        };
        reader.readAsText(file);
    } else {
        alert("No file selected.");
    }
});

document.getElementById("downloadZip").addEventListener("click", function() {
    fetch('http://127.0.0.1:5000/compress', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
        } else {
            alert("Compress Error: " + data.message);
        }
    })
    .catch(error => {
        console.error('Compress Error: ', error);
        alert(`Compress Error: ${error}`);
    });

    var a = document.createElement("a");
    a.href = "/output.zip";
    a.download = "output.zip";
    a.click();
    document.getElementById("downloadZip").style.display = "none";
});
