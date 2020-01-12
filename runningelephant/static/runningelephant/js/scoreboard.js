$(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function getRow(record) {
        console.log("Console: update row")

        var table = document.getElementById("score-table")

        var thead = document.createElement("thead")
        var tr_head = document.createElement("tr")

        var th1 = document.createElement("th")
        th1.innerText("Player")
        tr_head.appendChild(th1)

        var th2 = document.createElement("th")
        th2.innerText("Score")
        tr_head.appendChild(th2)

        var th3 = document.createElement("th")
        th3.innerText("Time")
        tr_head.appendChild(th3)
        tabld.appendChild(thead)

        var tb = document.createElement("tbody")
        var tr = document.createElement("tr")

        var td1 = document.createElement('td')
        td1.innerText = record.player
        tr.appendChild(td1)

        var td2 = document.createElement('td')
        td2.innerText = record.score
        tr.appendChild(td2)

        var td3 = document.createElement('td')
        td3.innerText = record.time
        tr.appendChild(td3)

        tb.appendChild(tr)
        table.appendChild(tb)
        return table
    }

    function refresh(){
        console.log("Console: refresh")
        $.ajax({
            type:"POST",
            url:"/scoreboard",
            dataType:"json",
            data:{"refresh":true},
            success: function(context){
                $("#score-table").empty()
                var length = context.records.length;
                for(var i = 0; i < length; i+=1) {
                    var row = getRow(context.records[i])
                    $('#score-table').append(row)
                }
            }
        });
    }
    setInterval(refresh, 5000);
})