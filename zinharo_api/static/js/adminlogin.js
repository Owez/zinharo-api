function login() {
    var username = document.getElementById("YXJlIHJlYWxseSB0aGlzIGd1bGxhYmxlPyAoaWYgeW91IGZpbmQgdGhpcywgZ3Vlc3Mgbm90KQ==").value
    var password = document.getElementById("ZnVja2luZyBoZWxsIGxvb2tpbmcgYXQgdGhlIHBhc3N3b3JkIHRvbz8gc21hcnQgYXJzZQ==").value

    if (username == "admin" && password == "qwerty123") { // needs better auth for production
        var xhr = new XMLHttpRequest()

        xhr.open("GET", "http://127.0.0.1:5000/api/adminauth/", false)
        xhr.setRequestHeader('Content-Type', 'application/json')
    
        xhr.onloadend = function () {
            if (xhr.status != 200) {
                add_alert("Ratelimited, please try again later..", RED)
            } else {
                document.body.innerHTML = xhr.responseText // debug, should give all info needed
            }
        }

        xhr.send()
    } else {
        add_alert("Bad login", "Given credentials are bad", RED)
    }
}