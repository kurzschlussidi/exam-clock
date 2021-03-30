remainingTime(appConfig.end_time, appConfig.show_remaining);

function remainingTime(end_time_str, show_remaining)
{
    end_times = end_time_str.split(':')
    var end_time = new Date();
    var live_time = new Date();
    end_time.setHours(end_times[0]);
    end_time.setMinutes(end_times[1]);
    end_time.setSeconds(end_times[2]);
    time_diff = (end_time - live_time) / 60000;
    if (show_remaining == 'y') {
        if (time_diff > 1) { // A lot of time left
            time_diff = Math.floor(time_diff)
            document.getElementById("time_remaining").innerHTML=time_diff + ' Minuten';
        } else if (Math.floor(time_diff) == 1) { // between 1 and 2 minutes left
            time_diff = Math.floor(time_diff)
            document.getElementById("time_remaining").innerHTML=time_diff + ' Minute';
        } else if (time_diff > 0){ //under a minute left
            time_diff = Math.floor(time_diff*60);
            document.getElementById("time_remaining").innerHTML=time_diff + ' Sekunden';
        } else { //time is over
            document.getElementById("time_remaining").innerHTML='Prüfung Vorbei';
            window.location.replace(appConfig.redirect_url);
        }
    } else {
        if (time_diff < 0) {
            window.location.replace(appConfig.redirect_url);
        }
    }
    t=setTimeout(function(){remainingTime(appConfig.end_time, appConfig.show_remaining)},500);
}