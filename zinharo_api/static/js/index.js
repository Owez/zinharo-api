const RED = "bd3e3e"
const YELLOW = "ff9933"
const GREEN = "009933"

function new_hash(pcap) {
    var xhr = new XMLHttpRequest()

    xhr.open("POST", "http://127.0.0.1:5000/api/hash/", false)
    xhr.setRequestHeader('Content-Type', 'application/json')

    xhr.onloadend = function () {
        console.log("Hash POST:\n\n" + xhr.responseText)

        if (xhr.status == 200) {
            var resp_json = JSON.parse(xhr.responseText)

            if (resp_json.status == "completed") {
                add_alert("Already processed", "Visit <a class=\"alertlink\" href=\"https://zinharo.com/pcap/" + resp_json.body.hash.id + "\">zinharo.com/pcap/" + resp_json.body.hash.id + "/</a> to view the outcome(s) of this job", GREEN)
            }
            else {
                add_alert("Added .pcap to queue", "Visit <a class=\"alertlink\" href=\"https://zinharo.com/pcap/" + resp_json.body.hash.id + "\">zinharo.com/pcap/" + resp_json.body.hash.id + "/</a> to view progress", GREEN)
            }
        }
        else if (xhr.status == 202) {
            var resp_json = JSON.parse(xhr.responseText)

            add_alert("Already queued", "Visit <a class=\"alertlink\" href=\"https://zinharo.com/pcap/" + resp_json.body.hash.id + "\">zinharo.com/pcap/" + resp_json.body.hash.id + "/</a> to view progress of this already-queued job", GREEN)
        }
        else if (xhr.status == 429) {
            add_alert("Rate limited", "You have uploaded too many pcap files in too short of a time. The limits are 2 uploads per minute with 10 max uploads per day!", RED)
        }
        else {
            add_alert("Error #" + xhr.status + "", "There was an error when uploading the hash `" + xhr.statusText + "`!", RED)
        }
    };

    var payload = JSON.stringify({ "pcap": pcap })
    xhr.send(payload)
}


function upload_hash() {
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        add_alert("Upload Error", "Uploading files is not supported in your browser", RED)
        return
    }

    var input = document.getElementById('hashinput')

    if (!input.files) {
        add_alert("Upload Error", "Uploading files is not supported in your browser (can't read `files` of `input.files`)", RED)
    }
    else if (!input.files[0]) {
        add_alert("Upload Warning", "You have to upload a pcap file before you can crack it!", YELLOW)
    }
    else {
        var file = input.files[0]

        if (file.size >= 2500000) {
            add_alert("File too large!", "Zinharo only supports files up to 2.5 megabytes in size due to bandwidth limitations. Please try to make your pcap file smaller", RED)
            return
        }
        else if (file.name.split(".").pop() != "pcap") {
            add_alert("Invalid file format", "Zinharo does not support other files than `.pcap`, please enter a valid pcap file!", RED)
            return
        }

        var fr = new FileReader()
        fr.readAsDataURL(file)

        fr.onload = function () {
            new_hash(fr.result.split(",")[1])
        }
    }
}

console.log("`index.js` loaded!")
