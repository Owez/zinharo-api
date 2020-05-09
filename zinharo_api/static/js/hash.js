function get_cap() {
    var id = Number(document.getElementById("hidden-id").textContent)

    const target = new URL('http://127.0.0.1:5000/api/hash/');
    const params = new URLSearchParams();
    params.set("id", id);
    target.search = params.toString();

    var xhr = new XMLHttpRequest()

    xhr.open("GET", target, false)

    xhr.onloadend = function () {
        console.log("Hash GET:\n\n" + xhr.responseText)

        var hashinfo = document.getElementById("hashinfo")

        hashinfo.innerHTML = ""

        var title = document.createElement("h1")
        var content = document.createElement("p")

        if (xhr.status == 404) {
            title.innerHTML = "Given cap was not found!"
            content.innerHTML = "The cap given (#" + id + ") was not found! Please try a different cap id or submitting your cap again."
        }
        else if (xhr.status == 200) {
            var hash = JSON.parse(xhr.responseText).body.hash

            var content_created = "<h3>Added</h3><p>This cap was added on the date " + hash.created.split("T")[0].split("-").join("/") + "</p>"

            if (hash.jobs.length == 0) {
                var content_jobs = "<h3>Cracks</h3><p>There are currently no cracks for this cap</p>"
            }
            else {
                var job_desc = "<h3>Cracks</h3><p>There have been " + hash.jobs.length + " crack(s) for this cap file:</p>"
                var joblist = "<ul>"

                hash.jobs.forEach(job => {
                    joblist += "<li>Cracked by client " + job.client_id + " with the password: <b>" + job.password + "</b></li>"
                })

                joblist += "</ul>"

                var content_jobs = job_desc + joblist
            }

            if (hash.reports.length == 0) {
                var content_reports = "<h3>Reports</h3><p>Nobody has reported this cap file yet. If there are completed cracks, it means that this is most likely a valid cap file!</p>"
            }
            else {
                var report_desc = "<h3>Reports</h3><p>This cap file has been reported " + hash.reports.length + " time(s), here are the reports:</p>"
                var reportlist = "<ul>"

                hash.reports.forEach(report => {
                    if (report.info) {
                        reportlist += "<li>Client " + report.client_id + " reported this cap file with the following infomation: \"" + report.info + "\".</li>"
                    } else {
                        reportlist += "<li>Client " + report.client_id + " reported this cap file but provided no infomation.</li>"
                    }
                })

                reportlist += "</ul>"

                var content_reports = report_desc + reportlist
            }

            var content_cap_body = "<h3>Body of cap</h3><p>Below is the body of this cap in base64 form. This can be up to 2.5mb so it may be long!</p><p class=\"cap-body\">" + hash.cap + "</p>"

            title.innerHTML = "About cap " + id
            content.innerHTML = content_created + content_jobs + content_reports + content_cap_body
        }
        else if (xhr.status == 429) {
            title.innerHTML = "Rate limited"
            content.innerHTML = "You have been requesting too many cap files at once! Please slow down or if you think this is a mistake, <a href=\"https://zinharo.com/contact\">contact me</a>."
        }
        else {
            title.innerHTML = "Unknown error " + xhr.status + " when retreiving cap " + id
            content.innerHTML = "There was an unknown error: `" + xhr.statusText + "` when retriving cap " + id + "!"
        }

        hashinfo.appendChild(title)
        hashinfo.appendChild(content)
    }

    xhr.send()
}

console.log("`hash.js` loaded!")
get_cap()
